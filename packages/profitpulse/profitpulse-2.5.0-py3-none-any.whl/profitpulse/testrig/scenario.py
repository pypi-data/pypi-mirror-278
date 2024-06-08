# type: ignore
from typing import Optional

from typer.testing import CliRunner

from profitpulse.cli.main import cli

runner = CliRunner(mix_stderr=False)


class CLIScenario:
    """
    Builds scenarios up on the tests can be run and evaluates the result taking
    the context (CLI) into asset.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self, *_, **__) -> None:
        self._app = cli

    def assign_category(self, seller, category):
        result = runner.invoke(
            self._app,
            ["categories", "assign", seller, category],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec

        return result.stdout

    # Asset management -----------------------------------------------------------------------------------------------

    def show_assets(self):
        """
        Shows all the assets and their current balance.
        """
        result = runner.invoke(self._app, ["assets", "show"], catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec

        return result.stdout

    expect_assets__first_usage = ""

    def open_asset(self, asset_name):
        """
        Opens a new asset.
        """

        result = runner.invoke(
            self._app, ["assets", "open", asset_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec

    def divest(self, asset_name: str) -> None:
        result = runner.invoke(
            self._app, ["assets", "divest", asset_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec
        assert result.stdout == "", result.stdout  # nosec

    def delete_asset(self, asset_name: str) -> None:
        """
        Deletes an asset.
        """
        result = runner.invoke(
            self._app, ["assets", "delete", asset_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec

    # Money transactions  ----------------------------------------------------------------------------------------------

    def deposit(
        self, cent_amount: int, asset_name: str, comment: Optional[str] = None
    ) -> None:
        args = ["deposit", str(cent_amount), asset_name]
        if comment:
            args.append("--comment")
            args.append(comment)
        result = runner.invoke(self._app, args, catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec

    def withdraw(self, cent_amount: int, asset_name: str) -> None:
        result = runner.invoke(
            self._app,
            ["withdraw", str(cent_amount), asset_name],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec

    def transfer(self, amount: int, from_asset: str, to_asset: str):
        result = runner.invoke(
            self._app,
            ["transfer", str(amount), from_asset, to_asset],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    # Reports ----------------------------------------------------------------------------------------------------------

    def revalue(self, amount: int, asset_name: str):
        result = runner.invoke(
            self._app, ["revalue", str(amount), asset_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    def pulse(self):
        """
        Shows a global view of the user finances.
        """

        result = runner.invoke(self._app, ["pulse"], catch_exceptions=False)

        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    # I don't remember what these are .... facepalm --------------------------------------------------------------------

    def report(
        self,
        seller: Optional[str] = None,
        group_seller: Optional[bool] = False,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ):
        cmd = ["report"]
        if seller:
            cmd.append("--seller")
            cmd.append(seller)

        if group_seller:
            cmd.append("--group-seller")

        if since:
            cmd.append("--since")
            cmd.append(since)

        if until:
            cmd.append("--until")
            cmd.append(until)

        result = runner.invoke(self._app, cmd, catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    @property
    def current_month(self) -> str:
        """
        Returns the current month of the imported transactions.
        """
        # This is one of the months defined in the fixture file comprovativo_cgd.csv
        return "8"

    def import_transactions(self, transactions_file: str):
        result = runner.invoke(
            self._app,
            ["import", str(transactions_file)],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout
