import json

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler


@chariot.group()
@cli_handler
def link(ctx):
    """Link an account or integration to Chariot"""
    pass


@link.command('chariot')
@cli_handler
@click.argument('username')
def link_account(controller, username):
    """ Link another Chariot account to yours """
    controller.link_account(username, config={})


@link.command('slack')
@cli_handler
@click.argument('webhook')
def link_slack(controller, webhook):
    """ Send all new risks to Slack """
    controller.link_account('slack', {'webhook': webhook})


@link.command('jira')
@cli_handler
@click.argument('url')
@click.argument('user_email')
@click.argument('access_token')
@click.argument('project_key')
@click.argument('issue_type')
def link_jira(controller, url, user_email, access_token, project_key, issue_type):
    """ Create JIRA when a risk is opened """
    config = {'url': url, 'userEmail': user_email, 'accessToken': access_token, 'projectKey': project_key,
              'issueType': issue_type}
    controller.link_account('jira', config)


@link.command('amazon')
@cli_handler
@click.argument('account')
def link_amazon(controller, account):
    """ Enumerate AWS for Assets"""
    controller.link_account('amazon', {}, account)
    print('Account added. Please refer to the instructions in the UI for adding CloudFormation templates to your AWS account.')


@link.command('azure')
@cli_handler
@click.argument('appid')
@click.argument('secret')
@click.argument('tenant')
@click.argument('subscription')
def link_azure(controller, appid, secret, tenant, subscription):
    """ Enumerate Azure for Assets """
    config = {'name': appid, 'secret': secret, 'tenant': tenant, 'subscription': subscription}
    controller.link_account('azure', config)


@link.command('gcp')
@cli_handler
@click.argument('keyfile')
def link_gcp(controller, keyfile):
    """ Enumerate GCP for Assets """
    config = {}
    with open(keyfile, "r") as f:
        config['default'] = json.loads(f.read())
    controller.link_account('gcp', config)


@link.command('github')
@cli_handler
@click.argument('pat')
def link_github(controller, pat):
    """ Allow Chariot to scan your private repos """
    controller.link_account('github', {'pat': pat})


@link.command('ns1')
@cli_handler
@click.argument('ns1_api_key')
def link_ns1(controller, ns1_api_key):
    """ Allow Chariot to retrieve zone information from NS1 """
    controller.link_account('ns1', {'ns1_api_key': ns1_api_key})


@link.command('crowdstrike')
@cli_handler
@click.argument('client')
@click.argument('secret')
@click.argument('url')
def link_crowdstrike(controller, client, secret, url):
    """ Enumerate Crowdstrike for Assets and Risks """
    config = {'clientID': client, 'secret': secret, 'baseURL': url}
    controller.link_account('crowdstrike', config)
