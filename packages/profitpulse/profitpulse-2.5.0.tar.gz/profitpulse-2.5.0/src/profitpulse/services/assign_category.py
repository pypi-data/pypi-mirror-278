import abc

from profitpulse.lib.seller import Category, Seller, SellerNotFoundError

seller_not_found_message = "Seller not found"


class AssignCategoryCategoryCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, name: str) -> Category: ...  # pragma: no cover

    @abc.abstractmethod
    def __setitem__(
        self, name: str, category: Category
    ) -> None: ...  # pragma: no cover


class AssignCategorySellerCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, name: str) -> Seller: ...  # pragma: no cover

    @abc.abstractmethod
    def __setitem__(self, name: str, seller: Seller) -> None: ...  # pragma: no cover


class AssignCategoryRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def seller(self) -> Seller: ...  # pragma: no cover

    @property
    @abc.abstractmethod
    def category(self) -> Category: ...  # pragma: no cover


class AssignCategoryService:
    def __init__(
        self,
        sellers: AssignCategorySellerCollector,
        categories: AssignCategoryCategoryCollector,
    ):
        self.sellers = sellers
        self.categories = categories

    def execute(self, request: AssignCategoryRequester) -> None:
        try:
            seller = self.sellers[str(request.seller)]
        except KeyError:
            raise SellerNotFoundError(seller_not_found_message)

        try:
            self.categories[str(request.category)]
        except KeyError:
            self.categories[str(request.category)] = request.category

        seller.assign(request.category)

        self.sellers[str(request.seller)] = seller
