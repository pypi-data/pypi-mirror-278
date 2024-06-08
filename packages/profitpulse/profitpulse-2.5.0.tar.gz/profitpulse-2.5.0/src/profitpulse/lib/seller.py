from dataclasses import dataclass
from typing import Optional


class SellerNotFoundError(Exception):
    pass


@dataclass(frozen=True)
class Category:
    name: str

    def __str__(self) -> str:
        return self.name


class Seller:
    def __init__(self, name: str, category: Optional[Category] = None) -> None:
        self.category = category
        self.name = name

    def __str__(self) -> str:
        return self.name

    def assign(self, category: Category) -> None:
        self.category = category
