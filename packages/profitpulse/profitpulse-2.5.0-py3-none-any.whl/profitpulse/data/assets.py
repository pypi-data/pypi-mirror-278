import typing

import pastperfect
from turbofan.database import text

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.acquire_asset import OpenAssetAssetCollector
from profitpulse.services.delete_asset import DeleteAssetAssetCollector
from profitpulse.services.deposit_into_asset import (
    ASSET_DEPOSITED,
    DepositIntoAssetAssetCollector,
)
from profitpulse.services.divest_asset import DivestAssetAssetCollector
from profitpulse.services.import_transactions import ImportTransactionsAssetCollector
from profitpulse.services.revalue_asset import (
    ASSET_REVALUED,
    RevalueAssetAssetCollector,
)

ACTIVE = "O"
DIVESTED = "C"


def status_from_value(status: str) -> str:
    """
    Returns the status human readable representation.
    """
    # TODO: this should be the presentation layer.
    if status == "O":
        return "Active"
    if status == "C":
        return "Divested"

    raise Exception(f"Unknown status {status}")


class Assets(
    DivestAssetAssetCollector,
    DeleteAssetAssetCollector,
    OpenAssetAssetCollector,
    DepositIntoAssetAssetCollector,
    ImportTransactionsAssetCollector,
    RevalueAssetAssetCollector,
):
    """
    Assets implement the AssetsRepository protocol.
    """

    def __init__(self, session: typing.Any) -> None:
        self._session = session

    def __len__(self) -> None:
        sql_stmt = """
            SELECT COUNT(*) FROM account
        """
        prepared_statement = text(sql_stmt)
        row = self._session.execute(prepared_statement).first()
        return row[0]

    def __setitem__(self, asset_name: AssetName, asset: Asset) -> None:
        sql_stmt = """
            INSERT OR REPLACE INTO account (name, status)
                            VALUES (:name, :status)
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(
            name=str(asset.name),
            status=DIVESTED if asset.closed else ACTIVE,
        )
        self._session.execute(prepared_statement)

    def __getitem__(self, asset_name: AssetName) -> Asset:
        sql_stmt = """
            SELECT account.name as name,
                   account.status
              FROM account
             WHERE account.name = :name
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(asset_name))
        row = self._session.execute(prepared_statement).first()
        if not row:
            raise KeyError

        events = pastperfect.Events(self._session)
        asset_name = row[0]
        balance = Money(0)
        for event in events:
            if event.name == ASSET_REVALUED and event.data.get("name") == asset_name:
                balance = balance + Money(event.data.get("balance"))

            if event.name == ASSET_DEPOSITED and event.data.get("name") == asset_name:
                balance = balance + Money(event.data.get("balance"))

        return Asset(
            AssetName(row[0]),
            value=balance,
            closed=True if row[1] == DIVESTED else False,
        )

    def __delitem__(self, asset_name: AssetName) -> None:
        sql_stmt = "DELETE FROM account WHERE name = :name"
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(asset_name))
        self._session.execute(prepared_statement)
