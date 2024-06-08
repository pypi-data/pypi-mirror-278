import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.services.errors import AssetNotFoundError
from profitpulse.services.services import EventEmitterMixin, EventLogger


class DeleteAssetRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def asset_name(self) -> AssetName: ...  # pragma: no cover


class DeleteAssetAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover

    @abc.abstractmethod
    def __delitem__(self, asset_name: AssetName) -> None: ...  # pragma: no cover


ASSET_DELETED = "ASSET_DELETED"


class DeleteAssetService(EventEmitterMixin):
    def __init__(
        self,
        assets: DeleteAssetAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ):
        super().__init__(ASSET_DELETED, event_log)
        self._assets = assets

    def execute(self, request: DeleteAssetRequester) -> None:
        try:
            asset = self._assets[request.asset_name]
        except KeyError:
            raise AssetNotFoundError(asset_name=request.asset_name)

        asset.prepare_deletion()

        del self._assets[request.asset_name]
