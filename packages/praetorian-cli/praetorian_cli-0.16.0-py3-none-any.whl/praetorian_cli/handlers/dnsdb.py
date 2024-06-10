import csv
import ipaddress
import json
from getpass import getpass

import click
import requests

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler


@chariot.command('dnsdb')
@cli_handler
@click.option('-tld', '--tld', required=True)
def dnsdb(controller, tld):
    """ Retrieve CNAME and A records from DNSDB for a TLD """
    # Establish DNSDB connection
    token = getpass("Enter your DNSDB API key: ")
    dnsdb = DNSDB(token)

    # Ensure user is ok using API credits
    calls = dnsdb.get_remaining_usages()
    print(f'[!] You have {calls} API requests remaining.')
    cont = input("Continue? (y/N): ").strip().lower()
    if cont == 'n':
        return

    # Collect assets Chariot already knows about
    print('Contacting Chariot for existing assets...')
    my_assets = {}
    result = controller.my(dict(key=f'#asset#{tld}'))
    for hit in result.get('assets', []):
        my_assets[hit['key']] = hit
    print(f'..... Found {len(my_assets)} existing assets under {tld}')

    # Retrieve assets from DNSDB
    print('Contacting DNSDB for records...')
    discovered = []
    for asset in dnsdb.fetch_records(tld):
        key = f'#asset#{tld}#{asset["dns"]}#{asset["name"]}'
        if key not in my_assets:
            discovered.append(asset)
            print(f'..... {asset["dns"]} ({asset["name"]})')

    # Write the new assets to a CSV
    with open('assets.csv', 'w', newline='') as file:
        fields = ['seed', 'dns', 'name']
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        for asset in discovered:
            writer.writerow(asset)

    # Upload new assets to Chariot
    print(f'{len(discovered)} new assets were written to assets.csv. Please review/edit.')

    if discovered:
        input('Press ENTER to upload to Chariot')
        with open('assets.csv', newline='') as file:
            reader = csv.DictReader(file)
            for asset in reader:
                print(f'..... Uploading {asset["dns"]} ({asset["name"]})')
                controller.add("asset", asset)


class DNSDB:
    def __init__(self, api_key: str):
        self.base_url = "https://api.dnsdb.info"
        self.headers = {
            "X-API-Key": api_key,
            "Accept": "*/*"
        }

    def get_remaining_usages(self):
        """ Retrieves the remaining query quota for the day. """
        url = f"{self.base_url}/lookup/rate_limit"
        response = requests.get(url, headers=self.headers)
        if response.ok:
            data = response.json()
            return data['rate']['remaining']
        response.raise_for_status()

    def fetch_records(self, tld, record_types=['A', 'CNAME']) -> dict:
        """ Fetch specified types of DNS records for a given TLD """
        for record_type in record_types:
            last_after = int(-2678400 * .25)  # 7.5 days
            url = f"{self.base_url}/dnsdb/v2/lookup/rrset/name/*.{tld}/{record_type}?limit=0&time_last_after={last_after}"
            response = requests.get(url, headers=self.headers)

            if response.ok:
                for asset in self._parse(tld, response.text):
                    yield asset

    def _parse(self, tld, record_data) -> dict:
        """ Convert a text response into a list of CSV-friendly assets """
        for result in record_data.split('\n'):
            try:
                record = json.loads(result)
                rrname = record.get('obj', {}).get('rrname', '')
                rrtype = record.get('obj', {}).get('rrtype', '')

                if rrname and not rrname.startswith('*.'):
                    for rdata in record.get('obj', {}).get('rdata', []):
                        if rrtype == "A":
                            ip = ipaddress.ip_address(rdata)
                            if ip.is_private or ip.is_loopback:
                                continue

                            yield dict(seed=tld, dns=rrname.rstrip('.'), name=rdata.rstrip('.'))

            except json.JSONDecodeError as e:
                continue
