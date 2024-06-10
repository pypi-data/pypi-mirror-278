import json
from enum import Enum
from functools import wraps

import click


class Asset(Enum):
    ACTIVE = "A"
    ACTIVE_HIGH = "AH"
    FROZEN = "F"
    FROZEN_HIGH = "FH"
    UNKNOWN = "U"


class Job(Enum):
    QUEUED = "JQ"
    RUNNING = "JR"
    FAIL = "JF"
    PASS = "JP"


class Risk(Enum):
    TRIAGE_INFO = "TI"
    TRIAGE_LOW = "TL"
    TRIAGE_MEDIUM = "TM"
    TRIAGE_HIGH = "TH"
    TRIAGE_CRITICAL = "TC"
    OPEN_INFO = "OI"
    OPEN_LOW = "OL"
    OPEN_MEDIUM = "OM"
    OPEN_HIGH = "OH"
    OPEN_CRITICAL = "OC"
    OPEN_INFO_PROGRESS = "OIP"
    OPEN_LOW_PROGRESS = "OLP"
    OPEN_MEDIUM_PROGRESS = "OMP"
    OPEN_HIGH_PROGRESS = "OHP"
    OPEN_CRITICAL_PROGRESS = "OCP"
    OPEN_INFO_FIXED = "OIF"
    OPEN_LOW_FIXED = "OLF"
    OPEN_MEDIUM_FIXED = "OMF"
    OPEN_HIGH_FIXED = "OHF"
    OPEN_CRITICAL_FIXED = "OCF"
    CLOSED_INFO = "CI"
    CLOSED_LOW = "CL"
    CLOSED_MEDIUM = "CM"
    CLOSED_HIGH = "CH"
    CLOSED_CRITICAL = "CC"
    CLOSED_INFO_ACCEPTED = "CIA"
    CLOSED_LOW_ACCEPTED = "CLA"
    CLOSED_MEDIUM_ACCEPTED = "CMA"
    CLOSED_HIGH_ACCEPTED = "CHA"
    CLOSED_CRITICAL_ACCEPTED = "CCA"
    CLOSED_INFO_REJECTED = "CIR"
    CLOSED_LOW_REJECTED = "CLR"
    CLOSED_MEDIUM_REJECTED = "CMR"
    CLOSED_HIGH_REJECTED = "CHR"
    CLOSED_CRITICAL_REJECTED = "CCR"


Status = {'asset': Asset, 'seed': Asset, 'job': Job, 'risk': Risk}

key_set = {'assets': '#asset#', 'seeds': '#seed#', 'jobs': '#job#', 'risks': '#risk#', 'accounts': '#account#',
           'definitions': '#file#definitions/', 'integrations': '#account#', 'attributes': '#attribute#',
           'references': '#ref#', 'files': '#file#', 'threats': '#threat#'}


def handle_api_error(func):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            click.secho(e.args[0], fg='red')

    return handler


def cli_handler(func):
    func = click.pass_obj(func)
    func = handle_api_error(func)
    return func


def list_options(filter_name):
    def decorator(func):
        func = cli_handler(func)
        func = click.option('-filter', '--filter', default="", help=f"Filter by {filter_name}")(func)
        func = click.option('-details', '--details', is_flag=True, default=False, help="Show detailed information")(
            func)
        return func

    return decorator


def status_options(status_choices):
    def decorator(func):
        func = cli_handler(func)
        func = click.option('-status', '--status', type=click.Choice([s.value for s in status_choices]), required=False,
                            help="Status of the object")(func)
        func = click.option('-comment', '--comment', default="", help="Add a comment")(func)
        return func

    return decorator


def page_options(func):
    func = click.option('-offset', '--offset', default="", help="List results from an offset")(func)
    func = click.option('-page', '--page', type=click.Choice(('no', 'interactive', 'all')), default="interactive",
                        help="Pagination mode. 'all' pages up to 100 pages. Default: 'interactive'")(func)

    return func


def my_result(controller, key, filter="", offset=""):
    resp = controller.my(dict(key=key, offset=offset))
    result = {'data': []}
    for key, value in resp.items():
        if isinstance(value, list):
            result['data'] += value
    if filter != "":  # filter by name or member only for accounts
        result['data'] = [item for item in resp['accounts'] if filter == item['name'] or filter == item['member']]
    if resp.get('offset'):
        result['offset'] = json.dumps(resp['offset'])
    return result


def paginate(controller, key, item_type="", filter="", offset="", details=False, page="interactive"):
    pages = 0
    while pages < 100:
        result = my_result(controller, key, filter, offset)
        result = handle_results(result, item_type)
        display_list(result, details)
        if page == 'no' or not result.get('offset'):
            if 'offset' in result:
                print(f"Next offset: {result['offset']}")
            break
        elif page == 'interactive':
            print("Press any key to view next or 'q' to quit")
            user_input = click.getchar()
            if user_input == 'q':
                break
        offset = result['offset']
        pages += 1


def handle_results(result, item_type):
    if item_type == 'integrations':
        result['data'] = [item for item in result['data'] if '@' not in item['member'] and item['member'] != 'settings']
    elif item_type == 'accounts':
        result['data'] = [item for item in result['data'] if '@' in item['member']]
    elif item_type == 'definitions':
        for hit in result.get('data', []):
            hit['key'] = hit['key'].split("definitions/")[-1]
    return result


def display_list(result, details):
    if details:
        print(json.dumps(result, indent=4))
    else:
        for hit in result.get('data', []):
            print(f"{hit['key']}")


def get_data_key(result):
    keys = list(result.keys())
    return keys[1] if keys[0] == 'offset' else keys[0]
