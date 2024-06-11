import json
import sys

import click
from rich.table import Table
from rich.console import Console

from delta.cli import Utils
from delta.cli.utils import API, ReturnCode

# TODO Add the option to specify the version of the DeltaTwin to be retrieved
DELTA_TWIN_NAME = "Name"
DELTA_TWIN_DESCRIPTION = "Description"
DELTA_TWIN_TOPICS = "Topics"
DELTA_TWIN_VERSION = "Version"
DELTA_TWIN__AVAILABLE_VERSION = "Available Version"
DELTA_TWIN_AUTHOR = "Author"
DELTA_TWIN_INPUTS = "Inputs"
DELTA_TWIN_OUTPUTS = "Outputs"


@click.command('get',
               short_help='Get the information of a DeltaTwin component.')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='Format of the output json/text default is text')
@click.argument('dt_name')
@click.option('--version', '-v', type=str, default=None)
@click.help_option("--help", "-h")
def get_deltatwin_info(
        conf,
        format_output,
        dt_name,
        version):
    """Get information about a DeltaTwin component by
    specifying its name. By default, the command returns information
    for the latest version of the Delta component. To get information about a
    previous version, you must specify it with the --version option
    'delta get [deltatwin_name] --version x.y.z'.
    To get the list of all available versions you can either use
    'deltatwin list --version' or 'deltatwin get [deltatwin_name] --version'.
    DT_NAME : DeltaTwin component name [MANDATORY]

    This command will show the DeltaTwin component information,
    before using this command the user must be logged in.
    """

    param = {}

    if version is not None:
        param = {'version': version}

    version_info = API.get_dt_version(conf, dt_name)
    version = [e['name'] for e in version_info]
    dt_info = API.get_dt(conf, dt_name, param)

    if len(dt_info) == 0 and len(version) == 0:
        click.echo(f"{Utils.log_info} No DeltaTwin found.")
        return

    try:
        data = {
            'name': dt_info['name'],
            'description': dt_info['description'],
            'topics': dt_info['topics'],
            'version': dt_info['version'],
            'available_version': version,
            'author': dt_info.get('owner'),
            'inputs': dt_info.get('inputs'),
            'outputs': dt_info.get('outputs')
        }
    except KeyError:
        click.echo(f"{Utils.log_error} The response "
                   f"does not respect the DeltaTwin format.")
        sys.exit(ReturnCode.SERVICE_ERROR)

    if format_output is not None and format_output.lower() == 'json':
        click.echo(json.dumps(data, indent=4))
    else:
        table = Table()
        table.add_column(DELTA_TWIN_NAME)
        table.add_column(DELTA_TWIN_DESCRIPTION)
        table.add_column(DELTA_TWIN_TOPICS)
        table.add_column(DELTA_TWIN_VERSION)
        table.add_column(DELTA_TWIN__AVAILABLE_VERSION)
        table.add_column(DELTA_TWIN_AUTHOR)
        table.add_column(DELTA_TWIN_INPUTS)
        table.add_column(DELTA_TWIN_OUTPUTS)

        table.add_row(data['name'],
                      data['description'],
                      str(data['topics']),
                      data['version'],
                      str(data['available_version']),
                      data['author'],
                      str(data['inputs']),
                      str(data['outputs']))

        console = Console()
        console.print(table)
