# type: ignore
from typing import Dict, Optional

import pytest

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.services.acquire_asset import (
    AcquireAssetService,
    AssetAlreadyExistsError,
    OpenAssetAssetCollector,
    OpenAssetRequester,
)


class AssetsStub(OpenAssetAssetCollector):
    def __init__(self) -> None:
        self._assets: Dict[AssetName, Asset] = dict()

    def get(self, asset_name: AssetName) -> Optional[Asset]:
        try:
            return self._assets[asset_name]
        except KeyError:
            return None

    def __setitem__(self, asset_name: AssetName, asset: Asset) -> None:
        self._assets[asset_name] = asset


class OpenAssetRequest(OpenAssetRequester):
    def __init__(self, asset_name: str):
        self._asset_name = AssetName(asset_name)

    @property
    def asset_name(self) -> AssetName:
        return self._asset_name


def test_raise_error_if_an_asset_with_same_name_already_exists() -> None:
    asset_name = "TheAssetName"
    request = OpenAssetRequest(asset_name)
    assets = AssetsStub()
    service = AcquireAssetService(assets, [])

    service.execute(request)

    with pytest.raises(
        AssetAlreadyExistsError,
        match="An asset with the same name already exists",
    ):
        service.execute(request)


def test_save_asset_when_its_a_new_asset() -> None:
    request = OpenAssetRequest(asset_name="TheAssetName")
    assets = AssetsStub()
    service = AcquireAssetService(assets, [])

    service.execute(request)

    assert assets.get(request.asset_name) is not None  # nosec
