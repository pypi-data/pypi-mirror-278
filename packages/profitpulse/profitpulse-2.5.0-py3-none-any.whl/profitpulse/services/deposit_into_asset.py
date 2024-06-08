import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.errors import AssetNotFoundError
from profitpulse.services.services import EventEmitterMixin, EventLogger


class DepositIntoAssetRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def asset_name(self) -> AssetName: ...  # pragma: no cover

    @property
    @abc.abstractmethod
    def amount(self) -> Money: ...  # pragma: no cover


class DepositIntoAssetAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover

    @abc.abstractmethod
    def __setitem__(
        self, asset_name: AssetName, asset: Asset
    ) -> None: ...  # pragma: no cover


ASSET_DEPOSITED = "asset_deposited"


class DepositIntoAssetService(EventEmitterMixin):
    def __init__(
        self,
        assets: DepositIntoAssetAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ):
        super().__init__(ASSET_DEPOSITED, event_log)
        self._assets = assets

    def execute(self, request: DepositIntoAssetRequester) -> None:
        try:
            asset = self._assets[request.asset_name]
        except KeyError:
            raise AssetNotFoundError(request.asset_name)

        deposited = asset.deposit(request.amount)

        self._assets[request.asset_name] = asset

        if not deposited:
            return

        self.emit(
            name=str(asset.name),  # type: ignore
            balance=int(request.amount),  # type: ignore
        )
