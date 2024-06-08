import typing

import pastperfect
from sqlalchemy import text

from profitpulse.data.assets import DIVESTED, status_from_value
from profitpulse.data.data import View
from profitpulse.lib.money import Money
from profitpulse.services.deposit_into_asset import ASSET_DEPOSITED
from profitpulse.services.revalue_asset import ASSET_REVALUED


class PulseView(View):
    def __init__(self, session: typing.Any):
        self._session = session

    @property
    def data(self) -> typing.Any:  # noqa
        sql_stmt = """SELECT name, status as name FROM account ORDER BY id ASC"""
        assets = self._session.execute(text(sql_stmt))

        events = pastperfect.Events(self._session)

        results = []
        total = Money(0)
        for asset in assets:
            asset_name = asset[0]
            status = asset[1]
            asset_details = ["n/a"] * 5
            invested = Money(0)
            current = Money(0)

            has_events = False
            for event in events:
                has_events = True

                # Current
                if (
                    event.name == ASSET_REVALUED or event.name == ASSET_DEPOSITED
                ) and event.data.get("name") == asset_name:
                    current = current + Money(event.data.get("balance"))

                # Invested
                if (
                    event.name == ASSET_DEPOSITED
                    and event.data.get("name") == asset_name
                ):
                    invested = invested + Money(event.data.get("balance", 0))

            asset_details[0] = asset_name
            asset_details[1] = status_from_value(status)
            if not has_events:
                results.append(asset_details)
                continue

            asset_details[2] = str(invested)
            asset_details[3] = str(current)
            if status == DIVESTED:
                asset_details[3] = "n/a"  # TODO: presentation
            else:
                total = total + current
            asset_details[4] = str(current - invested)

            results.append(asset_details)

        return {"total": str(total), "assets": results}
