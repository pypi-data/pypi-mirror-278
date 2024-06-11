import sys

import click
from delta.core import DeltaCore

from delta.cli import ReturnCode


@click.command(
    'sync',
    short_help='Reload the manifest file')
@click.help_option("--help", "-h")
def sync():
    """
    Reload the manifest file content to refresh project resources section
    """
    with DeltaCore() as core:
        core.drive_sync()
