import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.services.errors import AssetNotFoundError
from profitpulse.services.services import EventEmitterMixin, EventLogger


class DivestAssetRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def asset_name(self) -> AssetName: ...  # pragma: no cover


class DivestAssetAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover

    @abc.abstractmethod
    def __setitem__(
        self, account_name: AssetName, value: Asset
    ) -> None: ...  # pragma: no cover


ASSET_DIVESTED = "asset_divested"


class DivestAssetService(EventEmitterMixin):
    """
    Closes an asset.
    """

    def __init__(
        self,
        assets: DivestAssetAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ):
        super().__init__(ASSET_DIVESTED, event_log)
        self.assets = assets

    def execute(self, request: DivestAssetRequester) -> None:
        try:
            asset = self.assets[request.asset_name]
        except KeyError:
            raise AssetNotFoundError(request.asset_name)

        asset.close()

        self.assets[request.asset_name] = asset

        self.emit(
            name=str(asset.name),  # type: ignore
        )
