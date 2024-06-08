import pytest

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.deposit_into_asset import (
    AssetNotFoundError,
    DepositIntoAssetAssetCollector,
    DepositIntoAssetRequester,
    DepositIntoAssetService,
)


class AssetsNoAsset(DepositIntoAssetAssetCollector):
    def __getitem__(self, asset_name: AssetName) -> Asset:
        raise KeyError

    def __setitem__(self, asset_name: AssetName, asset: Asset) -> None:
        pass


class DepositInAssetRequest(DepositIntoAssetRequester):
    @property
    def asset_name(self) -> AssetName:
        return AssetName("TheAssetName")

    @property
    def comment(self) -> None:
        return None

    @property
    def amount(self) -> Money:
        return Money(100)


def test_raise_error_if_asset_does_not_exist() -> None:
    request = DepositInAssetRequest()
    assets = AssetsNoAsset()

    service = DepositIntoAssetService(assets, [])
    with pytest.raises(
        AssetNotFoundError,
        match="Could not find an asset with name 'TheAssetName'",
    ):
        service.execute(request)


class AssetsStub(DepositIntoAssetAssetCollector):
    def __init__(self, asset: Asset) -> None:
        self._asset = asset
        self.asset_added = False

    def __getitem__(self, asset_name: AssetName) -> Asset:
        return self._asset

    def __setitem__(self, asset_name: AssetName, asset: Asset) -> None:
        self.asset_added = True
        self._asset = asset


def test_save_deposit_into_asset() -> None:
    request = DepositInAssetRequest()
    asset = Asset(AssetName("TheAssetName"))
    assets = AssetsStub(asset)

    service = DepositIntoAssetService(assets, [])

    service.execute(request)

    assert assets.asset_added  # nosec


class DepositInAssetWithCommentRequest(DepositIntoAssetRequester):
    @property
    def asset_name(self) -> AssetName:
        return AssetName("TheAssetName")

    @property
    def amount(self) -> Money:
        return Money(100)


def test_inject_the_comment_into_the_asset_deposit_when_one_is_defined() -> None:
    request = DepositInAssetWithCommentRequest()
    asset = Asset(AssetName("TheAssetName"))
    assets = AssetsStub(asset)

    service = DepositIntoAssetService(assets, [])

    service.execute(request)

    assert assets.asset_added  # nosec
