import pastperfect
import pytest
from pastperfect import Event

from profitpulse.data.assets import Assets
from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.services.revalue_asset import ASSET_REVALUED


@pytest.mark.integration
def test_return_none_when_asset_not_found(tmp_db_session):
    assets = Assets(tmp_db_session)
    assert assets.get(AssetName("TheAssetName")) is None  # nosec


@pytest.mark.integration
def test_set_asset(tmp_db_session):
    asset = Asset(AssetName("TheAssetName"))
    assets = Assets(tmp_db_session)

    assets[asset.name] = asset


@pytest.mark.integration
def test_save_asset_balance(tmp_db_session):
    value = Money(10)
    asset_name = AssetName("TheAssetName")
    asset = Asset(asset_name=asset_name, value=value)
    assets = Assets(tmp_db_session)
    events = pastperfect.Events(tmp_db_session)
    events.append(
        Event(
            name=ASSET_REVALUED, data={"name": str(asset_name), "balance": int(value)}
        )
    )

    assets[asset.name] = asset

    asset = assets[asset_name]
    assert asset is not None  # nosec
    assert asset.value == value  # nosec


@pytest.mark.integration
def test_save_asset_closed_status(tmp_db_session):
    asset_name = AssetName("TheAssetName")
    asset = Asset(asset_name=asset_name)
    assets = Assets(tmp_db_session)

    asset.close()

    assets[asset.name] = asset

    asset = assets[asset.name]
    assert asset.closed is True  # nosec


@pytest.mark.integration
def test_delete_asset(tmp_db_session):
    asset_name = AssetName("TheAssetName")
    asset = Asset(asset_name=asset_name)
    asset_name1 = AssetName("TheAssetName1")
    asset1 = Asset(asset_name=asset_name1)
    assets = Assets(tmp_db_session)
    assets[asset1.name] = asset1

    assets[asset.name] = asset

    assert len(assets) == 2  # nosec

    del assets[asset.name]

    assert len(assets) == 1  # nosec
