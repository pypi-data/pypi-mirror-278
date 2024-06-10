import base64
import json
import os
from base64 import b64encode
from random import randint

import requests

from praetorian_cli.sdk.keychain import verify_credentials, Keychain


class Chariot:

    def __init__(self, keychain: Keychain):
        self.keychain = keychain

    @verify_credentials
    def my(self, params: dict) -> {}:
        resp = requests.get(f"{self.keychain.api}/my", params=params, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def count(self, params: dict) -> {}:
        resp = requests.get(f"{self.keychain.api}/my/count", params=params, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def add(self, type, payload: dict) -> {}:
        resp = requests.post(f"{self.keychain.api}/{type}", json=payload, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def delete(self, type, key: str) -> {}:
        resp = requests.delete(f"{self.keychain.api}/{type}", json={'key': key},
                               headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def update(self, resource: str, data: dict) -> {}:
        resp = requests.put(f"{self.keychain.api}/{resource}", json=data, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def report(self, name: str) -> {}:
        resp = requests.get(f"{self.keychain.api}/report/risk", {'name': name}, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.text

    @verify_credentials
    def link_account(self, username: str, config: dict, id: str = ""):
        resp = requests.post(f"{self.keychain.api}/account/{username}", json={'config': config, 'value': id},
                             headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def unlink(self, username: str, id: str = ""):
        resp = requests.delete(f"{self.keychain.api}/account/{username}", headers=self.keychain.headers,
                               json={'value': id})
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def upload(self, name: str, upload_path: str = ""):
        with open(name, 'rb') as file:
            path = name
            if upload_path != "":
                path = upload_path

            resp = requests.put(f"{self.keychain.api}/file", params={"name": path}, data=file, allow_redirects=True,
                                headers=self.keychain.headers)
            if not resp.ok:
                raise Exception(f'[{resp.status_code}] Request failed')

    def sanitize_filename(self, filename: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    @verify_credentials
    def download(self, name: str, download_path: str) -> bool:
        resp = requests.get(f"{self.keychain.api}/file", params={"name": name}, allow_redirects=True,
                            headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')

        name = self.sanitize_filename(name)
        directory = os.path.expanduser(download_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        download_path = os.path.join(directory, name)
        with open(download_path, 'wb') as file:
            file.write(resp.content)

        return download_path

    @verify_credentials
    def add_webhook(self):
        pin = str(randint(10000, 99999))
        self.link_account(username="hook", config={'pin': pin})
        username = b64encode(self.keychain.username.encode('utf8'))
        encoded_string = username.decode('utf8')
        encoded_username = encoded_string.rstrip('=')
        return f'{self.keychain.api}/hook/{encoded_username}/{pin}'

    def get_risk_details(self, key: str):
        resp = self.my(dict(key=key))['risks'][0]
        poe = f"{resp['dns']}/{resp['name']}"
        downloaded_path = self.download(poe, "")
        with open(downloaded_path, 'r') as file:
            poe_content = file.read()
        os.remove(poe)  # remove the file after reading
        poe_json = json.loads(poe_content)
        resp["url"] = poe_json.get("url", "")
        resp["ip"] = poe_json.get("ip", "")
        resp["port"] = poe_json.get("port", "")
        resp["proof of exploit"] = base64.b64encode(poe_content.encode('utf-8')).decode('utf-8')
        return resp
