import click

from zhixin.registry.access.commands.grant import access_grant_cmd
from zhixin.registry.access.commands.list import access_list_cmd
from zhixin.registry.access.commands.private import access_private_cmd
from zhixin.registry.access.commands.public import access_public_cmd
from zhixin.registry.access.commands.revoke import access_revoke_cmd


@click.group(
    "access",
    commands=[
        access_grant_cmd,
        access_list_cmd,
        access_private_cmd,
        access_public_cmd,
        access_revoke_cmd,
    ],
    short_help="Manage resource access",
)
def cli():
    pass
