import click

from zhixin.registry.access.validate import validate_urn
from zhixin.registry.client import RegistryClient


@click.command("public", short_help="Make resource public")
@click.argument(
    "urn",
    callback=lambda _, __, value: validate_urn(value),
)
@click.option("--urn-type", type=click.Choice(["prn:reg:pkg"]), default="prn:reg:pkg")
def access_public_cmd(urn, urn_type):  # pylint: disable=unused-argument
    client = RegistryClient()
    client.update_resource(urn=urn, private=0)
    return click.secho(
        "The resource %s has been successfully updated." % urn,
        fg="green",
    )
