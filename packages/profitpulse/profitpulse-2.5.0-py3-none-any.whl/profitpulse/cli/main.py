"""
CLI entry points for Typer (https://typer.tiangolo.com/) made CLI.
"""

from datetime import datetime
from importlib.metadata import version as get_version
from pathlib import Path
from typing import Optional

import typer

from profitpulse.cli.adapters import (  # delete_asset,; show_assets,; transfer,
    assign_category,
    database_path,
    deposit,
    divest_asset,
    import_file,
    open_asset,
    pulse,
    report,
    reset,
    revalue,
)
from profitpulse.gui.main import start_server
from profitpulse.infrastructure.migrations import migrate_database  # type: ignore

cli = typer.Typer(
    add_completion=False,
    help="Profitpulse helps you manage your personal finances.",
)

assets = typer.Typer()
cli.add_typer(
    assets,
    name="assets",
    help="Handles assets",
)

categories = typer.Typer()
cli.add_typer(
    categories,
    name="categories",
    help="Handles expense categories",
)


@cli.command(name="version", help="Shows the current profitpulse version")
def version() -> None:
    migrate_database(database_path)
    typer.echo(get_version("profitpulse"))


@cli.command(help="Opens the browser GUI of profitpulse")
def gui() -> None:
    start_server()


@cli.command(name="pulse", help="Show's the health of your wealth")
def pulse_() -> None:
    migrate_database(database_path)
    pulse()


@cli.command(name="revalue", help="Revalues an asset to reflect it's current worth")
def revalue_(
    cent_amount: int = typer.Argument(
        0, help="Amount to deposit in cents", metavar="AMOUNT"
    ),
    asset_name: str = typer.Argument(
        "", help="Name of the asset", metavar='"ASSET NAME"'
    ),
) -> None:
    migrate_database(database_path)
    revalue(cent_amount, asset_name)


@cli.command(name="import", help="Import transactions for expense tracking")
def import_(file_path: Path) -> None:
    migrate_database(database_path)
    import_file(file_path)


@cli.command(name="report", help="Builds reports according to filter")
def report_(
    seller: Optional[str] = typer.Option(
        default="", help="Filters report by Seller in description"
    ),
    group_seller: Optional[bool] = typer.Option(
        default=False, help="Groups report by the Seller description"
    ),
    since: Optional[datetime] = typer.Option(
        default=None,
        help="Date since when the report must be shown (inclusive)",
    ),
    until: Optional[datetime] = typer.Option(
        default=None,
        help="Date until when the report must be shown (inclusive)",
    ),
) -> None:
    migrate_database(database_path)
    report(seller=seller, group_seller=group_seller, since=since, until=until)


@cli.command(name="reset", help="Deletes all information in profitpulse")
def reset_() -> None:
    delete_information = typer.confirm(
        "Are you sure you want to delete all financial information ?"
    )
    migrate_database(database_path)
    if not delete_information:
        raise typer.Abort()

    reset()


@cli.command(name="deposit", help="Deposits money into an asset")
def deposit_(
    cent_amount: int = typer.Argument(
        0, help="Amount to deposit in cents", metavar="AMOUNT"
    ),
    asset_name: str = typer.Argument(
        "", help="Name of the asset", metavar='"ASSET NAME"'
    ),
) -> None:
    migrate_database(database_path)
    deposit(cent_amount, asset_name)


# @profitpulse_app.command(name="withdraw", help="Withdraws money from an asset")
# def withdraw_(
#     cent_amount: int = typer.Argument(
#         0, help="Amount to withdraw in cents", metavar="AMOUNT"
#     ),
#     asset_name: str = typer.Argument(
#         "", help="Name of the asset", metavar='"ASSET NAME"'
#     ),
# ) -> None:
#     migrate_database(database_path)
#     deposit(-cent_amount, asset_name)


# @profitpulse_app.command(name="transfer", help="Transfers money between assets")
# def transfer_(
#     cent_amount: int = typer.Argument(
#         0, help="Amount to transfer in cents", metavar="AMOUNT"
#     ),
#     from_asset_name: str = typer.Argument(
#         "", help="Name of the asset to transfer from", metavar='"ASSET NAME"'
#     ),
#     to_asset_name: str = typer.Argument(
#         "", help="Name of the asset to transfer to", metavar='"ASSET NAME"'
#     ),
# ) -> None:
#     migrate_database(database_path)
#     transfer(cent_amount, from_asset_name, to_asset_name)


# @profitpulse_assets_app.command(name="show", help="Shows existing assets")
# def show() -> None:
#     migrate_database(database_path)
#     show_assets()


@assets.command(name="open", help="Opens a new asset")
def open_(
    name: str = typer.Argument("", help="Name of the asset", metavar='"ASSET NAME"'),
) -> None:
    migrate_database(database_path)
    open_asset(name)


@assets.command(name="divest", help="Divests an asset")
def divest_(
    name: str = typer.Argument("", help="Name of the asset", metavar='"ASSET NAME"'),
) -> None:
    migrate_database(database_path)
    divest_asset(name)


# @profitpulse_assets_app.command(name="delete", help="Deletes an asset")
# def delete_(
#     name: str = typer.Argument("", help="Name of the asset", metavar='"ASSET NAME"'),
# ) -> None:
#     migrate_database(database_path)
#     delete_asset(name)


@categories.command(help="Assign a seller to a category")
def assign(
    seller: str = typer.Argument("", help="The Seller to assign a category to"),
    category: str = typer.Argument("", help="The Category to assign to the select"),
) -> None:
    migrate_database(database_path)
    assign_category(seller, category)
