import click

from zhixin.registry.access.validate import validate_client, validate_urn
from zhixin.registry.client import RegistryClient


@click.command("grant", short_help="Grant access")
@click.argument("level", type=click.Choice(["admin", "maintainer", "guest"]))
@click.argument(
    "client",
    metavar="[<ORGNAME:TEAMNAME>|<USERNAME>]",
    callback=lambda _, __, value: validate_client(value),
)
@click.argument(
    "urn",
    callback=lambda _, __, value: validate_urn(value),
)
@click.option("--urn-type", type=click.Choice(["prn:reg:pkg"]), default="prn:reg:pkg")
def access_grant_cmd(level, client, urn, urn_type):  # pylint: disable=unused-argument
    reg_client = RegistryClient()
    reg_client.grant_access_for_resource(urn=urn, client=client, level=level)
    return click.secho(
        "Access for resource %s has been granted for %s" % (urn, client),
        fg="green",
    )
