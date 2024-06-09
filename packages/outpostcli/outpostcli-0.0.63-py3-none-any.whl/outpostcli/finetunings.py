import click
from outpostkit import Client, Finetunings
from outpostkit.utils import convert_outpost_date_str_to_date
from rich.table import Table

from outpostcli.utils import (
    add_options,
    api_token_opt,
    click_group,
    console,
    entity_opt,
)


@click_group()
def finetunings():
    """
    Manage Endpoints
    """
    pass


@finetunings.command(name="list")
@add_options([api_token_opt, entity_opt])
def list_endpoints(api_token, entity):
    client = Client(api_token=api_token)
    fntun_resp = Finetunings(client=client, entity=entity).list()
    fntun_table = Table(
        title=f"Endpoints ({fntun_resp.total})",
    )
    # "primary_endpoint",
    fntun_table.add_column("name")
    fntun_table.add_column("task")
    # inf_table.add_column("status")
    # fntun_table.add_column("hardware_instance")
    # fntun_table.add_column("visibility")
    fntun_table.add_column("updated_at", justify="right")
    for fntun in fntun_resp.endpoints:
        fntun_table.add_row(
            fntun.name,
            fntun.taskType,
            convert_outpost_date_str_to_date(fntun.updatedAt).isoformat(),
        )

    console.print(fntun_table)


@finetunings.command(name="create")
@click.option(
    "--name",
    "-n",
    type=str,
    default=None,
    required=False,
    help="name of the endpoint to create.",
)
@click.option(
    "--name",
    "-n",
    type=str,
    default=None,
    required=False,
    help="name of the endpoint to create.",
)
@add_options([api_token_opt, entity_opt])
def create_finetuning(api_token: str, entity: str, name: str):
    client = Client(api_token=api_token)
    fntun_resp = Finetunings(client=client, entity=entity).list()
    fntun_table = Table(
        title=f"Endpoints ({fntun_resp.total})",
    )
    # "primary_endpoint",
    fntun_table.add_column("name")
    fntun_table.add_column("task")
    # inf_table.add_column("status")
    # fntun_table.add_column("hardware_instance")
    # fntun_table.add_column("visibility")
    fntun_table.add_column("updated_at", justify="right")
    for fntun in fntun_resp.endpoints:
        fntun_table.add_row(
            fntun.name,
            fntun.taskType,
            convert_outpost_date_str_to_date(fntun.updatedAt).isoformat(),
        )

    console.print(fntun_table)
