class AssetName:
    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Asset name cannot be empty")
        self._name: str = name

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"AssetName({self._name})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, AssetName):
            return NotImplemented
        return self._name == __value._name

    def __hash__(self) -> int:
        return hash((self._name,))
