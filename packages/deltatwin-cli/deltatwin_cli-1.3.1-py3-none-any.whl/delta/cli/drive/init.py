import sys

import click
from delta.core.delta_core import DeltaCore

from delta.cli import Utils, ReturnCode


@click.command(
    'init',
    short_help='Create an empty DeltaTwin repository')
@click.argument('directory',
                type=str)
@click.help_option("--help", "-h")
def init(directory):
    """Create an empty DeltaTwin repository.

    The DIRECTORY automatically contains subdirectories and files
    used to manage a DeltaTwin.

    Typically, there are resources, artifacts, sources and models folders.
    It also contains the manifest file which synchronizes all resources,
    dependencies and sources used by the DeltaTwin

    DIRECTORY : path to the folder containing
    the DeltaTwin components [MANDATORY]

    """
    with DeltaCore() as core:
        core.drive_init(directory)
    click.echo(f"{Utils.log_info} DeltaTwin {directory} created")
