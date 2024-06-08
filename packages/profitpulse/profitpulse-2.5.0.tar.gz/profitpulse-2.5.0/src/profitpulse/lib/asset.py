from typing import Optional

from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money


class AssetCantBeDeletedError(Exception):
    def __str__(self) -> str:
        return "Asset can't be deleted"


class AssetCantBeClosedError(Exception):
    def __str__(self) -> str:
        return "Asset can't be closed"


class Asset:
    def __init__(
        self,
        asset_name: AssetName,
        closed: bool = False,
        value: Optional[Money] = None,
    ):
        self._asset_name = asset_name
        self._closed = closed
        self._value: Money = Money(0)
        if value:
            self._value = value

    def __repr__(self) -> str:
        return f"Asset({self._asset_name})"

    def revalue(self, value: Money) -> Money:
        performance = value - self._value
        self._value = value
        return performance

    @property
    def name(self) -> AssetName:
        return self._asset_name

    @property
    def value(self) -> Money:
        return self._value

    def close(self) -> None:
        self._closed = True

    @property
    def closed(self) -> bool:
        return True if self._closed else False

    def deposit(self, amount: Money) -> bool:
        if self.closed:
            return False

        deposited = True

        if self._value + amount < Money(0):
            amount = Money(0)
            deposited = False

        self._value += amount

        return deposited

    def prepare_deletion(self) -> None:
        if self._value > Money(0):
            raise AssetCantBeDeletedError()
