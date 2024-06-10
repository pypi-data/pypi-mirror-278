import click
import tabulate

from modulos_client import config as config_utils


@click.group(
    help="Manage configurations for an organization.",
)
def config_organizations():
    pass


@config_organizations.command(
    "get",
    help="Get configurations for an organization.",
)
@click.option(
    "-o",
    "--organization-id",
    type=str,
    default=None,
)
def get_organization_configurations(organization_id: str | None = None):
    client = config_utils.ModulosClient.from_conf_file()
    if organization_id is None:
        org_id = client.get("/users/me", {}).json().get("organization")["id"]
    else:
        org_id = organization_id
    response = client.get(f"/v1/config/organizations/{org_id}", {})
    if response.ok:
        click.echo(tabulate.tabulate(response.json().items(), headers=["Key", "Value"]))

    else:
        click.echo(f"Could not get configurations: {response.text}")


@config_organizations.command(
    "update",
    help="Update configurations for an organization.",
)
@click.option(
    "-o",
    "--organization-id",
    type=str,
    prompt=True,
)
@click.option(
    "--quota-projects",
    type=int,
    prompt=True,
    help="Number of projects allowed for the organization.",
)
def update_organization_configurations(organization_id: str, quota_projects: int):
    client = config_utils.ModulosClient.from_conf_file()
    org_id = organization_id
    payload = {"plan_quota": {"projects": quota_projects}}
    response = client.patch(f"/v1/config/organizations/{org_id}", payload)
    if response.ok:
        click.echo(tabulate.tabulate(response.json().items(), headers=["Key", "Value"]))

    else:
        click.echo(f"Could not get configurations: {response.text}")
