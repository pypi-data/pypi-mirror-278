import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.errors import AssetNotFoundError
from profitpulse.services.services import EventEmitterMixin, EventLogger


class RevalueAssetRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def asset_name(self) -> AssetName: ...  # pragma: no cover

    @property
    @abc.abstractmethod
    def value(self) -> Money: ...  # pragma: no cover


class RevalueAssetAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover

    @abc.abstractmethod
    def __setitem__(
        self, asset_name: AssetName, asset: Asset
    ) -> None: ...  # pragma: no cover


ASSET_REVALUED = "ASSET_REVALUED"


class RevalueAssetService(EventEmitterMixin):
    def __init__(
        self,
        assets: RevalueAssetAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ):
        super().__init__(ASSET_REVALUED, event_log)
        self.assets = assets

    def execute(self, request: RevalueAssetRequester) -> None:
        try:
            asset = self.assets[request.asset_name]
        except KeyError:
            raise AssetNotFoundError(request.asset_name)

        performance = asset.revalue(request.value)

        self.assets[request.asset_name] = asset

        self.emit(
            name=str(asset.name),  # type: ignore
            balance=int(performance),  # type: ignore
        )
