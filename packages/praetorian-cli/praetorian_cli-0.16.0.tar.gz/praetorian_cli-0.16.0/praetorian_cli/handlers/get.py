import base64
import json

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler, get_data_key


@chariot.group()
@cli_handler
def get(ctx):
    """Get resource details from Chariot"""
    pass


@get.command('file')
@cli_handler
@click.argument('name')
@click.option('-path', '--path', default="", help="Download path. Default: save to current directory")
def download_file(controller, name, path):
    """ Download a file using key or name."""
    if name.startswith('#'):
        downloaded_path = controller.download(name.split('#')[-1], path)
    else:
        downloaded_path = controller.download(name, path)
    print(f'Saved file at {downloaded_path}')


@get.command('definition')
@cli_handler
@click.argument('name')
@click.option('-path', '--path', default="", help="Download path. Default: save to current directory")
def download_definition(controller, name, path):
    """ Download a definition using the risk name. """
    downloaded_path = controller.download(f"definitions/{name}", path)
    print(f'Saved definition at {downloaded_path}')


@get.command('report')
@cli_handler
@click.option('-name', '--name', help="Enter a risk name", required=True)
def report(controller, name):
    """ Generate definition for an existing risk """
    resp = controller.report(name=name)
    resp = base64.b64decode(resp).decode('utf-8')
    print(resp)


@get.command('risk')
@cli_handler
@click.argument('key', required=True)
@click.option('-details', '--details', is_flag=True, help='Get additional details')
@click.option('-history', '--history', is_flag=True, help='Include risk history')
def risk(controller, key, details, history):
    """ Get risk details """
    if details:
        resp = controller.get_risk_details(key)
    else:
        resp = controller.my(dict(key=f'#risk#{key}'))
    if not history:
        del resp['history']
    print(json.dumps(resp, indent=4))


get_list = ['seeds', 'assets', 'references', 'attributes', 'jobs', 'threats', 'accounts', 'integrations']


def create_get_command(item):
    @get.command(item[:-1], help=f"Get {item[:-1]} details")
    @click.argument('key', required=True)
    @cli_handler
    def command(controller, key):
        resp = controller.my(dict(key=key))
        print(json.dumps(resp[get_data_key(resp)][0], indent=4))


for item in get_list:
    create_get_command(item)
