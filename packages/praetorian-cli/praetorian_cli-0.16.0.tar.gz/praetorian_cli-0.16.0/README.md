# Praetorian CLI

The CLI is a fully-featured companion to the Chariot UI, which is hosted at chaos.praetorian.com.

## Install

Python 3.8+ and PIP are required.

```zsh
pip install praetorian-cli
```

## Usage

To use the CLI:

1. Register for an account at http://preview.chariot.praetorian.com.
2. Log in and download [your keychain file](https://preview.chariot.praetorian.com/keychain.ini)
   to ``~/.praetorian/keychain.ini``.

View help for all available commands:

```zsh
praetorian chariot --help
```

The CLI is configured as a simple command + option utility. For example, to retrieve a list of all assets in your
account simply run:

```zsh
praetorian chariot list assets
```

To get detailed information about a specific asset:

```zsh
praetorian chariot get asset <ASSET_KEY>
```

## Developers

Integrate the CLI into your own application:

1. Include the dependency ``praetorian-cli`` in your project
2. Import the Chariot class ``from praetorian_cli.sdk.chariot import Chariot``
3. Import the Keychain class ``from praetorian_cli.sdk.keychain import Keychain``
4. Call any function (example below)

### Example

```python
from praetorian_cli.sdk.chariot import Chariot
from praetorian_cli.sdk.keychain import Keychain

chariot = Chariot(Keychain(profile='United States'))
chariot.add('seed', {'dns': 'example.com'})
```
