import pytest
from turbofan.database import text

from profitpulse.data.assets_view import AssetsView
from profitpulse.lib.money import Money


class TestAssetsView:
    @pytest.mark.integration
    def test_return_no_data_when_no_assets(self, tmp_db_session):
        assert AssetsView(tmp_db_session).data == []  # nosec

    @pytest.mark.integration
    def test_return_one_asset_when_one_asset_exists(self, tmp_db_session):
        DatabaseScenario(tmp_db_session).open_asset(name="TheAssetName")
        assert AssetsView(tmp_db_session).data == [  # nosec
            ["TheAssetName", str(Money(0)), "Closed"]
        ]


class DatabaseScenario:
    def __init__(self, session):
        self.session = session
        self.asset_id = None

    def open_asset(self, name):
        sql_statement = "INSERT INTO account (name)VALUES (:name)"
        prepared_statement = text(sql_statement).bindparams(name=name)
        result = self.session.execute(prepared_statement)
        self.asset_id = result.lastrowid
        return self
