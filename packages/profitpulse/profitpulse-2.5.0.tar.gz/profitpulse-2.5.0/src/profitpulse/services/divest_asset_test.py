from typing import Optional

import pytest

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.services.divest_asset import (
    AssetNotFoundError,
    DivestAssetAssetCollector,
    DivestAssetRequester,
    DivestAssetService,
)


class DivestAssetRequest(DivestAssetRequester):
    def __init__(self, asset_name: str):
        self._asset_name = asset_name

    @property
    def asset_name(self) -> AssetName:
        return AssetName(self._asset_name)


def test_raise_exception_when_asset_is_not_found() -> None:
    asset_name = "TheAssetName"
    request = DivestAssetRequest(asset_name)
    assets = DivestAssetAssetsRepo()
    service = DivestAssetService(assets, [])

    with pytest.raises(
        AssetNotFoundError,
        match="Could not find an asset with name 'TheAssetName'",
    ):
        service.execute(request)


class DivestAssetAssetsRepo(DivestAssetAssetCollector):
    def __init__(self, asset: Optional[Asset] = None) -> None:
        self._asset = asset

    def __getitem__(self, asset_name: AssetName) -> Asset:
        if not self._asset:
            raise KeyError
        return self._asset

    def __setitem__(self, asset_name: AssetName, asset: Asset) -> None:
        self._asset = asset


def test_close_asset_when_the_asset_exists() -> None:
    asset_name = "TheAssetName"
    asset = Asset(AssetName(asset_name))
    assets = DivestAssetAssetsRepo(asset)
    request = DivestAssetRequest(asset_name)
    service = DivestAssetService(assets, [])

    service.execute(request)

    assert asset.closed  # nosec
