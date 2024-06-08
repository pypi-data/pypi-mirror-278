import typing
from typing import Any

import pastperfect
from turbofan.database import text

from profitpulse.data import assets as assets_repository
from profitpulse.data.data import View
from profitpulse.lib.money import Money
from profitpulse.services.deposit_into_asset import ASSET_DEPOSITED
from profitpulse.services.revalue_asset import ASSET_REVALUED


class AssetsView(View):
    def __init__(self, session: typing.Any) -> None:
        self._session = session

    @property
    def data(self) -> Any:
        sql_stmt = "SELECT account.name as name, account.status FROM account"
        rows = self._session.execute(text(sql_stmt))
        assets = list(rows)
        events = pastperfect.Events(self._session)

        results = []
        for asset in assets:
            asset_name = asset[0]
            asset_details = [
                asset_name,
                "0.00",
                "Open" if asset[1] == assets_repository.ACTIVE else "Closed",
            ]
            total_balance = Money(0)
            for event in events:
                if (
                    event.name == ASSET_DEPOSITED or event.name == ASSET_REVALUED
                ) and event.data.get("name") == asset_name:
                    total_balance = total_balance + Money(event.data.get("balance"))

            asset_details[1] = str(total_balance)

            results.append(asset_details)

        return results
