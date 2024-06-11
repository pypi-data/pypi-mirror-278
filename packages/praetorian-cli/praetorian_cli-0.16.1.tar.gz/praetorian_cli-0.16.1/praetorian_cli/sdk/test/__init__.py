import configparser
import os

from pathlib import Path
from praetorian_cli.sdk.keychain import Keychain
from praetorian_cli.sdk.chariot import Chariot


class BaseTest:

    def setup_chariot(self):
        location = os.path.join(Path.home(), '.praetorian', 'keychain.ini')
        config = configparser.ConfigParser()
        config.read(location)
        profile = os.environ.get('CHARIOT_PROFILE') or 'United States'
        return Chariot(Keychain(location=location, profile=profile)), config[profile]['username']
