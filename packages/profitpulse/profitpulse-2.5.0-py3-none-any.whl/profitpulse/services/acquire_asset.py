import abc
import typing
from typing import Optional

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.services.services import EventEmitterMixin, EventLogger


class AssetAlreadyExistsError(Exception):
    def __str__(self) -> str:
        return "An asset with the same name already exists"


class OpenAssetRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def asset_name(self) -> AssetName: ...  # pragma: no cover


class OpenAssetAssetCollector(abc.ABC):
    def get(self, asset_name: AssetName) -> Optional[Asset]: ...  # pragma: no cover

    def __setitem__(
        self, asset_name: AssetName, asset: Asset
    ) -> None: ...  # pragma: no cover


ASSET_ACQUIRED = "asset_acquired"


class AcquireAssetService(EventEmitterMixin):
    def __init__(
        self,
        assets: OpenAssetAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ):
        super().__init__(ASSET_ACQUIRED, event_log)
        self.assets = assets

    def execute(self, request: OpenAssetRequester) -> None:
        if self.assets.get(request.asset_name):
            raise AssetAlreadyExistsError()

        asset = Asset(request.asset_name)
        self.assets[request.asset_name] = asset

        self.emit(
            asset_name=str(request.asset_name),  # type: ignore
            value=int(asset.value),  # type: ignore
        )
