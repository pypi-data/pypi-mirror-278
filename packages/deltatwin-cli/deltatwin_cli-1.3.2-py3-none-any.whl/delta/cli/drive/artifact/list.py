import json
import sys

import click

from delta.cli.utils import Utils, API, ReturnCode
from rich.console import Console
from rich.table import Table


@click.help_option("--help", "-h")
@click.command(
    'list',
    short_help='List the artifacts for a DeltaTwin component')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--short',
    '-s',
    flag_value=True,
    default=False,
    help='Shows only the most significant columns in table')
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='Format of the output json/text default is text')
def list_artifact(conf, short: bool, format_output: str) -> None:
    """List the artifacts of a DeltaTwin component

    **Example:** deltatwin drive artifact list
    """

    artifacts = API.list_artifact(conf)

    data = []
    for art in artifacts:
        if short:
            data.append(
                {
                    'artefact_id': art['artefact_id'],
                    'name': art['name'],
                    'publication_date': art['publication_date'],
                    'author': art['author'],
                    'size': art['size'],
                    'description': art['description'],
                    'topics': art['topics'],
                    'twin_name': art['twin_name']
                }
            )
        else:
            data.append(
                {
                    'artefact_id': art['artefact_id'],
                    'name': art['name'],
                    'publication_date': art['publication_date'],
                    'author': art['author'],
                    'size': art['size'],
                    'description': art['description'],
                    'topics': art['topics'],
                    'twin_name': art['twin_name'],
                    'twin_version': art['twin_version'],
                    'run_id': art['run_id'],
                    'additional_information': art['additional_information'],
                    'content': art['content'],
                    'content_type': art['content_type'],
                    'license': art['license']
                }
            )

    if format_output is not None and format_output.lower() == 'json':
        click.echo(json.dumps(data, indent=4))
        return

    if isinstance(data, list):
        if len(data) == 0:
            click.echo(f"{Utils.log_info} No artifact found")

        table = Table()
        table.add_column("Id", no_wrap=True)
        table.add_column('Name')
        table.add_column('Publication Date')
        table.add_column('Author')
        table.add_column('Size')
        table.add_column('Description')
        table.add_column('Topics')
        table.add_column('Twin Name')
        if not short:
            table.add_column('Twin version')
            table.add_column('Run id')
            table.add_column('Additional_information')
            table.add_column('Content')
            table.add_column('Content type')
            table.add_column('License')

        for artifact in data:
            rows = (artifact['artefact_id'],
                    artifact['name'],
                    str(artifact['publication_date']),
                    str(artifact['author']),

                    str(artifact['size']),
                    str(artifact['description']),
                    str(artifact['topics']),
                    str(artifact['twin_name'])
                    )
            if not short:
                row_long = (artifact['twin_version'],
                            str(artifact['run_id']),
                            str(artifact['additional_information']),
                            str(artifact['content']),
                            str(artifact['content_type']),
                            str(artifact['license'])
                            )
                rows += row_long

            table.add_row(*rows)
        console = Console()
        console.print(table)
