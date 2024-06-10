import click
import tabulate

from modulos_client import config as config_utils


@click.group(
    help="Manage projects.",
)
def projects():
    pass


@projects.command(
    "list",
    help="List all projects.",
)
@click.option(
    "--page",
    type=int,
    default=1,
)
@click.option(
    "-o",
    "--organization-id",
    type=str,
    default=None,
)
def list_projects(page: int, organization_id: str | None = None):
    client = config_utils.ModulosClient.from_conf_file()
    if organization_id is None:
        org_id = client.get("/users/me", {}).json().get("organization")["id"]
    else:
        org_id = organization_id
    response = client.get(f"/organizations/{org_id}/projects", data={"page": page})
    if response.ok:
        results = response.json().get("items")
        click.echo("Number of projects: " + str(response.json().get("total")))
        click.echo("Page: " + str(response.json().get("page")))
        results = [
            {
                "id": result["id"],
                "name": result["name"],
                "description": result["description"],
            }
            for result in results
        ]
        click.echo(tabulate.tabulate(results, headers="keys"))
    else:
        click.echo(f"Could not list projects: {response.text}")


@projects.command(
    "delete",
    help="Delete a project.",
)
@click.option(
    "--id",
    type=str,
    prompt=True,
)
def delete_projects(id: str):
    client = config_utils.ModulosClient.from_conf_file()
    response = client.delete(f"/projects/{id}")
    if response.ok:
        click.echo(f"Project '{id}' deleted.")
    else:
        click.echo(f"Could not delete project: {response.json().get('detail')}")
