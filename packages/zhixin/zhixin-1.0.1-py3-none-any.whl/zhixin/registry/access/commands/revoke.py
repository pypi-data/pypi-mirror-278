import click

from zhixin.registry.access.validate import validate_client, validate_urn
from zhixin.registry.client import RegistryClient


@click.command("revoke", short_help="Revoke access")
@click.argument(
    "client",
    metavar="[ORGNAME:TEAMNAME|USERNAME]",
    callback=lambda _, __, value: validate_client(value),
)
@click.argument(
    "urn",
    callback=lambda _, __, value: validate_urn(value),
)
@click.option("--urn-type", type=click.Choice(["prn:reg:pkg"]), default="prn:reg:pkg")
def access_revoke_cmd(client, urn, urn_type):  # pylint: disable=unused-argument
    reg_client = RegistryClient()
    reg_client.revoke_access_from_resource(urn=urn, client=client)
    return click.secho(
        "Access for resource %s has been revoked for %s" % (urn, client),
        fg="green",
    )
