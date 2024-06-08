import pytest
from pastperfect import Event, Events
from turbofan.database import text

from profitpulse.data.assets import ACTIVE, DIVESTED
from profitpulse.data.pulse_view import PulseView
from profitpulse.services.deposit_into_asset import ASSET_DEPOSITED
from profitpulse.services.revalue_asset import ASSET_REVALUED


@pytest.mark.integration
def test_return_no_assets_or_total_when_no_assets_exist(tmp_db_session):
    pulse_view = PulseView(tmp_db_session)

    data = pulse_view.data

    assert data == {"assets": [], "total": "0.00"}  # nosec


@pytest.mark.integration
def test_return_not_available_when_not_events_exist_for_account(tmp_db_session):
    sql_stmt = "INSERT INTO account (name, status) VALUES (:name, :status)"
    prep_stmt = text(sql_stmt).bindparams(name="TheAssetName", status=DIVESTED)
    tmp_db_session.execute(prep_stmt)
    pulse_view = PulseView(tmp_db_session)

    data = pulse_view.data

    assert data == {  # nosec
        "total": "0.00",
        "assets": [["TheAssetName", "Divested", "n/a", "n/a", "n/a"]],
    }


# fmt: off
@pytest.mark.integration
@pytest.mark.parametrize(
    "events, expected_total", [
        ([], "0.00"),
        ([Event(name=ASSET_DEPOSITED, data={})], "0.00"),
        ([Event(name=ASSET_DEPOSITED, data={"name": "a"})], "0.00"),
        ([Event(name=ASSET_DEPOSITED, data={"name": "a", "balance": None})], "0.00"),
        ([Event(name=ASSET_DEPOSITED, data={"name": "a", "balance": 1})], "0.01"),
        ([
             Event(name=ASSET_DEPOSITED, data={"name": "a", "balance": 1}),
             Event(name=ASSET_REVALUED, data={"name": "a", "balance": 1}),
         ], "0.02"),
        ([
             Event(name=ASSET_REVALUED, data={"name": "a", "balance": 2}),
             Event(name=ASSET_DEPOSITED, data={"name": "a", "balance": 1}),
         ], "0.03"),
    ])
# fmt: on
def test_show_total_value_of_assets(tmp_db_session, events, expected_total):
    sql_stmt = "INSERT INTO account (name, status) VALUES (:name, :status)"
    prep_stmt = text(sql_stmt).bindparams(name="a", status=ACTIVE)
    tmp_db_session.execute(prep_stmt)
    pulse_view = PulseView(tmp_db_session)
    evts = Events(tmp_db_session)
    for event in events:
        evts.append(event)

    data = pulse_view.data

    assert data["total"] == expected_total  # nosec


@pytest.mark.integration
def test_should_return_the_asset_details(tmp_db_session):
    sql_stmt = "INSERT INTO account (name, status) VALUES (:name, :status)"
    prep_stmt = text(sql_stmt).bindparams(name="TheAssetName", status=ACTIVE)
    tmp_db_session.execute(prep_stmt)
    events = Events(tmp_db_session)
    events.append(
        Event(name=ASSET_DEPOSITED, data={"name": "TheAssetName", "balance": 200})
    )
    events.append(
        Event(name=ASSET_REVALUED, data={"name": "TheAssetName", "balance": 100})
    )
    pulse_view = PulseView(tmp_db_session)

    data = pulse_view.data

    assert data == {  # nosec
        "total": "3.00",
        "assets": [["TheAssetName", "Active", "2.00", "3.00", "1.00"]],
    }
