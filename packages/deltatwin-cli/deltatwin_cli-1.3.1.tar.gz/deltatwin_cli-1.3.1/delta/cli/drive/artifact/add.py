import click
from delta.cli.utils import API, Utils

DEFAULT_LIMIT = 15


@click.help_option("--help", "-h")
@click.command(
    name='add',
    short_help='Convert an output of a run into artifact')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--artifact-name',
    '-a',
    type=str,
    required=True,
    help='Name of the artifact')
@click.option(
    '--description',
    '-d',
    type=str,
    required=True,
    help='Description of the artifact')
@click.option(
    '--topic',
    '-t',
    type=str,
    required=True,
    multiple=True,
    help='Define each topic of the artifact '
         '(multiple topics can be defined)')
@click.argument('run_id')
@click.argument('output_name')
def add_artifact(conf, run_id, output_name: str, artifact_name: str,
                 description: str = None, topic: list = None) -> None:
    """
    Create an artifact from an output of a DeltaTwin component execution.

    RUN_ID: Id of the run Execution [MANDATORY]

    OUTPUT_NAME: Name of the output [MANDATORY]

    Example:
    deltatwin drive artifact add b8810ff1-16c7-4269-b784-0c5ce392ff25 out
    --artifact-name artifact_1 --description description
    --topic topic1 --topic topic2

    """
    topics = []
    for tag_name in topic:
        topics.append(tag_name)

    if artifact_name is None:
        artifact_name = output_name

    API.create_artifact(conf, run_id, output_name,
                        artifact_name, description, topics)

    click.echo(f"{Utils.log_info} Artifact \"{artifact_name}\" "
               f"successfully created")
