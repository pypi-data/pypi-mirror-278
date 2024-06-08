"""
Adapters bridge the CLI frameworks and the application services by creating the
service inputs and handling the output for printing.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pastperfect
from gogotable import gogotable
from turbofan.database import Database, Session

from profitpulse.data.assets import Assets
from profitpulse.data.assets_view import AssetsView
from profitpulse.data.categories import Categories
from profitpulse.data.expenses_view import ExpensesView
from profitpulse.data.pulse_view import PulseView
from profitpulse.data.sellers import Sellers
from profitpulse.gateways.cgdfile import GatewayCGDFile  # type: ignore
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.lib.seller import Category, Seller
from profitpulse.services.acquire_asset import (
    AcquireAssetService,
    AssetAlreadyExistsError,
    OpenAssetRequester,
)
from profitpulse.services.assign_category import (
    AssignCategoryRequester,
    AssignCategoryService,
)
from profitpulse.services.delete_asset import DeleteAssetRequester, DeleteAssetService
from profitpulse.services.deposit_into_asset import (
    DepositIntoAssetRequester,
    DepositIntoAssetService,
)
from profitpulse.services.divest_asset import DivestAssetRequester, DivestAssetService
from profitpulse.services.import_transactions import ImportTransactionsService
from profitpulse.services.revalue_asset import (
    RevalueAssetRequester,
    RevalueAssetService,
)

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

database_path = Path.home() / Path("Library/Application Support/Profitpulse")


def report(
    seller: Optional[str] = None,
    group_seller: Optional[bool] = False,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
) -> None:
    """
    Shows a report of all transactions in all assets given the provided
     parameters:
     - seller: The provider or recipient of the value
     - since: The data from which the transactions should be shown
     - on: A specific date for which transactions should be shown
    """

    db = Database(database_path)
    with Session(db.engine) as session:

        view = ExpensesView(
            session, seller=seller, group_seller=group_seller, since=since, until=until
        )
        data = view.data

        table_data = []
        for item in data:
            d = item
            d[0] = f"{int(item[0]) / 100:.2f}"
            table_data.append(d)

        headers = ["Value", "Description", "Category", "Date"]
        if group_seller:
            headers = ["Value", "Description"]
        for line in gogotable(headers, data):
            print(line)


def pulse() -> None:
    """
    Shows the current wealth status.
    """

    headers = ["Asset Name", "Status", "Invested", "Current", "Performance"]

    db = Database(database_path)
    with Session(db.engine) as session:
        view = PulseView(session)
        data = view.data
        lines = gogotable(headers, data["assets"])  # {'assets': [], 'total': '0.00'}
        for line in lines:
            print(line)
        print(f"Total: {data['total']}")


class RevalueAssetRequest(RevalueAssetRequester):
    def __init__(self, asset_name: str, value: int) -> None:
        self._asset_name = asset_name
        self._value = value

    @property
    def asset_name(self) -> AssetName:
        return AssetName(self._asset_name)

    @property
    def value(self) -> Money:
        return Money(self._value)


def revalue(cent_amount: int, asset_name: str) -> None:
    """
    Revalues an asset to reflect it's current worth.
    """
    db = Database(database_path)
    with Session(db.engine) as session:
        request = RevalueAssetRequest(asset_name, cent_amount)
        assets = Assets(session)
        service = RevalueAssetService(assets, event_log=pastperfect.Events(session))
        service.execute(request)
        session.commit()


def reset() -> None:
    """
    Resets the application by removing the database.
    """
    db = Database(database_path)
    db.remove()


def import_file(file_path: Path) -> None:
    """
    Imports a file with all the transactions for a specific asset.
    """
    db = Database(database_path)
    with Session(db.engine) as session:
        gateway_cgd = GatewayCGDFile(file_path)

        service = ImportTransactionsService(
            gateway_cgd,
            Sellers(session),
            event_log=pastperfect.Events(session),
        )
        service.execute()
        session.commit()


class DepositRequest(DepositIntoAssetRequester):
    def __init__(self, cent_amount: int, asset_name: str) -> None:
        self._cent_amount = cent_amount
        self._asset_name = asset_name

    @property
    def amount(self) -> Money:
        return Money(self._cent_amount)

    @property
    def asset_name(self) -> AssetName:
        return AssetName(self._asset_name)


def deposit(cent_amount: int, asset_name: str) -> None:
    """
    Appreciate an asset by increasing it's value.
    """
    with Session(Database(database_path).engine) as session:
        assets = Assets(session)
        request = DepositRequest(cent_amount, asset_name)
        service = DepositIntoAssetService(assets, event_log=pastperfect.Events(session))
        service.execute(request)

        session.commit()


def transfer(cent_amount: int, from_asset_name: str, to_asset_name: str) -> None:
    """
    Transfers value from an asset to another asset.
    """
    with Session(Database(database_path).engine) as session:
        assets = Assets(session)
        request = DepositRequest(cent_amount, from_asset_name)
        service = DepositIntoAssetService(assets, event_log=pastperfect.Events(session))
        service.execute(request)

        request = DepositRequest(-cent_amount, to_asset_name)
        service = DepositIntoAssetService(assets, event_log=pastperfect.Events(session))
        service.execute(request)

        session.commit()


def show_assets() -> None:
    """
    Shows all assets and their current value.
    """
    with Session(Database(database_path).engine) as session:
        data = AssetsView(session).data
        if not data:
            return

        headers = ["Name", "Balance", "Status", "Comment"]
        lines = gogotable(headers, data)
        for line in lines:
            print(line)


class OpenAssetRequest(OpenAssetRequester):
    def __init__(self, name: str) -> None:
        self._name = AssetName(name)

    @property
    def asset_name(self) -> AssetName:
        return self._name


def open_asset(name: str) -> None:
    """
    Creates a new asset.
    """
    with Session(Database(database_path).engine) as session:
        assets = Assets(session)
        request = OpenAssetRequest(name)
        try:
            AcquireAssetService(assets, event_log=pastperfect.Events(session)).execute(
                request
            )
        except AssetAlreadyExistsError as e:
            print(str(e))
            return

        session.commit()


class DivestAssetRequest(DivestAssetRequester):
    def __init__(self, asset_name: str) -> None:
        self._asset_name = asset_name

    @property
    def asset_name(self) -> AssetName:
        return AssetName(self._asset_name)


def divest_asset(name: str) -> None:
    """
    Divests an asset from your wealth but the keeping it's history.
    """
    with Session(Database(database_path).engine) as session:
        assets = Assets(session)
        request = DivestAssetRequest(name)
        DivestAssetService(assets, event_log=pastperfect.Events(session)).execute(
            request
        )
        session.commit()


class DeleteAssetRequest(DeleteAssetRequester):
    def __init__(self, asset_name: str) -> None:
        self._asset_name = asset_name

    @property
    def asset_name(self) -> AssetName:
        return AssetName(self._asset_name)


def delete_asset(name: str) -> None:
    """
    Completely deletes an asset.
    """
    with Session(Database(database_path).engine) as session:
        assets = Assets(session)
        request = DeleteAssetRequest(name)
        DeleteAssetService(assets, event_log=pastperfect.Events(session)).execute(
            request
        )
        session.commit()


class AssignCategoryRequest(AssignCategoryRequester):
    def __init__(self, seller: str, category: str) -> None:
        self._seller = seller
        self._category = category

    @property
    def category(self) -> Category:
        return Category(self._category)

    @property
    def seller(self) -> Seller:
        return Seller(self._seller)


def assign_category(seller: str, category: str) -> None:
    """
    Assigns a category to a seller.
    """
    with Session(Database(database_path).engine) as session:
        sellers = Sellers(session)
        categories = Categories(session)
        request = AssignCategoryRequest(seller, category)
        service = AssignCategoryService(sellers, categories)
        service.execute(request)
        session.commit()
