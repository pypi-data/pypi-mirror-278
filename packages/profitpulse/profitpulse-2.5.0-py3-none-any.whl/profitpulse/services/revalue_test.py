import pytest

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.revalue_asset import (
    AssetNotFoundError,
    RevalueAssetAssetCollector,
    RevalueAssetRequester,
    RevalueAssetService,
)


class RevalueAssetRequest(RevalueAssetRequester):
    def __init__(self, asset_name: str, value: int):
        self._asset_name = AssetName(asset_name)
        self._value = value

    @property
    def value(self) -> Money:
        return Money(self._value)

    @property
    def asset_name(self) -> AssetName:
        return self._asset_name


class Assets(RevalueAssetAssetCollector):
    def __init__(self, asset: Asset) -> None:
        self.asset = asset

    def __getitem__(self, asset_name: AssetName) -> Asset:
        return self.asset

    def __setitem__(self, asset_name: AssetName, asset: Asset) -> None:
        self.asset = asset


def test_return_error_when_asset_does_not_exist() -> None:
    asset_name = "TheAssetName"
    request = RevalueAssetRequest(asset_name, 0)

    service = RevalueAssetService(dict(), [])  # type: ignore

    with pytest.raises(
        AssetNotFoundError,
        match=f"Could not find an asset with name '{asset_name}'",
    ):
        service.execute(request)


def test_revalue_asset() -> None:
    asset_name = "TheAssetName"
    assets = Assets(Asset(asset_name=AssetName(asset_name)))

    request = RevalueAssetRequest(asset_name, 1)
    service = RevalueAssetService(assets, [])

    service.execute(request)

    assert assets.asset.value == Money(1)  # nosec
