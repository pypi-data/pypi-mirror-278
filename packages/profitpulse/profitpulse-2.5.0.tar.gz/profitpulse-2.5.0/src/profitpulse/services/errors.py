from profitpulse.lib.asset_name import AssetName


class AssetNotFoundError(Exception):
    def __init__(self, asset_name: AssetName) -> None:
        self._asset_name = asset_name

    def __str__(self) -> str:
        return f"Could not find an asset with name '{self._asset_name}'"
