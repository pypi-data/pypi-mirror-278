from profitpulse.data.categories import Categories
from profitpulse.data.sellers import Sellers
from profitpulse.lib.seller import Category, Seller


def test_save_category_of_a_seller(tmp_db_session):
    Categories(tmp_db_session)
    sellers = Sellers(tmp_db_session)
    sellers["Seller"] = Seller("Seller")

    seller = sellers["Seller"]

    assert seller.category is None  # nosec

    seller.assign(Category("Health"))
    sellers["Seller"] = seller

    seller = sellers["Seller"]

    assert seller.category is not None  # nosec
    assert seller.category.name == "Health"  # nosec
