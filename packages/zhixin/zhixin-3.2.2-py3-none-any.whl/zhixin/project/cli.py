import click

from zhixin.project.commands.config import project_config_cmd
from zhixin.project.commands.init import project_init_cmd
from zhixin.project.commands.metadata import project_metadata_cmd


@click.group(
    "project",
    commands=[
        project_config_cmd,
        project_init_cmd,
        project_metadata_cmd,
    ],
    short_help="Project Manager",
)
def cli():
    pass
