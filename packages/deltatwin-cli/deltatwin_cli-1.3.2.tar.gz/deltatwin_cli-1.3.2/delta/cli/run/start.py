import json

import click

from delta.cli.utils import Utils, API

from delta.cli.run.get import display_run_detailed


@click.help_option("--help", "-h")
@click.command(
    'start',
    short_help='Start the DeltaTwin component execution')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--input-file',
    '-I',
    type=str,
    default=None,
    help='Inputs of run in json format, example: /mypath/inputs.json '
         'the json is defined like [{"name": "angle", "value": "45"},'
         '{"name": "image", "value": "http/myimg/$value"}]')
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='format of the output json/text default is text')
@click.option(
    '--input_run',
    '-i',
    type=(str, str),
    default=None,
    multiple=True,
    help='Define each input of a run, example: bandName B1')
@click.argument('twin_name')
def start(conf, twin_name, input_file, format_output, input_run):
    """Start the DeltaTwin component execution with the expected inputs.
    TWIN_NAME : Name of the DeltaTwin component [MANDATORY]
    """

    run = API.start_run(conf, twin_name, input_file, input_run)

    if Utils.output_as_json(format_output, run):
        click.echo(json.dumps(run, indent=4))
    else:
        display_run_detailed(run)
