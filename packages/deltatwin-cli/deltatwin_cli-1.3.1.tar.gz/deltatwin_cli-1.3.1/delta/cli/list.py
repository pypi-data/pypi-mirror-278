import json
import sys

import click
from rich.table import Table
from rich.console import Console

from delta.cli import Utils
from delta.cli.utils import API, ReturnCode

DELTA_TWIN_NAME = "Name"
DELTA_TWIN_DESCRIPTION = "Description"
DELTA_TWIN_CREATION_DATE = "Creation Date"
DELTA_TWIN_TOPICS = "Topics"
DELTA_TWIN_LICENSE = "License"
DELTA_TWIN_AUTHOR = "Author"


@click.command('list', short_help='List of the Delta components of the user.')
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
@click.help_option("--help", "-h")
def list_deltatwins(
        conf,
        format_output

):
    """List the DeltaTwins components available to the user.
    The user can view his Delta component details, all the
    Delta components from the Starter Kit and those
    created with the visibility public.

    This command will list the DeltaTwins components of the user.
    Before using this command the user must be logged in.
    """

    starter_kits = API.get_stater_kit(conf)
    deltatwins = API.get_dts(conf)

    data = []
    for dt in deltatwins + starter_kits:
        if dt['name'] not in [e['name'] for e in data]:
            data.append(
                {
                    'name': dt['name'],
                    'description': dt['description'],
                    'creation_date': dt['publication_date'],
                    'license': dt['license']['name'],
                    'topics': dt['topics'],
                    'author': dt.get('owner', 'unknown')
                }
            )

    if len(data) == 0:
        click.echo(f"{Utils.log_info} No DeltaTwin found.")
        sys.exit(ReturnCode.SUCCESS)

    if format_output is not None and format_output.lower() == 'json':
        click.echo(json.dumps(data, indent=4))
    else:
        if isinstance(data, list):
            table = Table()
            table.add_column(DELTA_TWIN_NAME)
            table.add_column(DELTA_TWIN_DESCRIPTION)
            table.add_column(DELTA_TWIN_CREATION_DATE)
            table.add_column(DELTA_TWIN_LICENSE)
            table.add_column(DELTA_TWIN_TOPICS)
            table.add_column(DELTA_TWIN_AUTHOR)

            for dt in data:
                table.add_row(
                    dt['name'],
                    dt['description'],
                    dt['creation_date'],
                    dt['license'],
                    str(dt['topics']),
                    dt['author'])

            console = Console()
            console.print(table)
