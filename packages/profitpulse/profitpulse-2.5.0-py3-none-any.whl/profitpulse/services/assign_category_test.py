import pytest

from profitpulse.lib.seller import Category, Seller, SellerNotFoundError
from profitpulse.services.assign_category import (
    AssignCategoryRequester,
    AssignCategoryService,
    seller_not_found_message,
)


class AssignCategoryRequest(AssignCategoryRequester):
    def __init__(self, seller: str, category: str) -> None:
        self._seller = seller
        self._category = category

    @property
    def category(self) -> Category:
        return Category(self._category)

    @property
    def seller(self) -> Seller:
        return Seller(self._seller)


def test_return_error_when_seller_not_found() -> None:
    service = AssignCategoryService(dict(), dict())  # type: ignore

    with pytest.raises(SellerNotFoundError, match=seller_not_found_message):
        service.execute(AssignCategoryRequest("NonExistingSeller", "category"))


def test_create_category_when_not_found() -> None:
    sellers = {"Seller": Seller("Seller")}
    categories: dict[str, Category] = dict()

    service = AssignCategoryService(sellers, categories)  # type: ignore
    service.execute(AssignCategoryRequest("Seller", "Category"))

    assert len(categories) == 1  # nosec


def test_assign_category_to_seller() -> None:
    sellers = {"Seller": Seller("Seller")}
    categories = {"Category": Category("Category")}
    service = AssignCategoryService(sellers, categories)  # type: ignore

    service.execute(AssignCategoryRequest("Seller", "Category"))

    assert sellers["Seller"].category is not None  # nosec
    assert sellers["Seller"].category.name == "Category"  # nosec
