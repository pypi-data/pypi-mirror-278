import pytest

from profitpulse.lib.asset import Asset, AssetCantBeDeletedError
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.delete_asset import (
    AssetNotFoundError,
    DeleteAssetRequester,
    DeleteAssetService,
)


class DeleteAssetRequest(DeleteAssetRequester):
    @property
    def asset_name(self) -> AssetName:
        return AssetName("TheAssetName")


def test_raise_error_when_asset_does_not_exist() -> None:
    request = DeleteAssetRequest()
    service = DeleteAssetService({}, [])  # type: ignore
    with pytest.raises(
        AssetNotFoundError,
        match=f"Could not find an asset with name '{request.asset_name}'",
    ):
        service.execute(request)


def test_raise_error_when_asset_cant_be_deleted() -> None:
    request = DeleteAssetRequest()
    asset = Asset(asset_name=request.asset_name, value=Money(10))
    assets = {request.asset_name: asset}

    service = DeleteAssetService(assets, [])  # type: ignore
    with pytest.raises(
        AssetCantBeDeletedError,
        match="Asset can't be deleted",
    ):
        service.execute(request)


def test_delete_asset_when_exists() -> None:
    request = DeleteAssetRequest()
    asset = Asset(asset_name=request.asset_name, value=Money(0))
    assets = {request.asset_name: asset}

    service = DeleteAssetService(assets, [])  # type: ignore
    service.execute(request)

    assert len(assets) == 0  # nosec
