import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.money import Money
from profitpulse.lib.seller import Category, Seller
from profitpulse.lib.year_month_day import YearMonthDay
from profitpulse.services.services import EventEmitterMixin, EventLogger


class ImportTransactionsTransactionGater(abc.ABC):
    def __iter__(self) -> None:
        pass  # pragma: no cover


class ImportTransactionsAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover


EXPENSE_MADE = "expense_made"
EXPENSES_IMPORTED = "expenses_imported"


class ImportTransactionsSellerCollector(abc.ABC):
    def __setitem__(
        self, seller_name: str, seller: Seller
    ) -> None: ...  # pragma: no cover


class ImportTransactionsService(EventEmitterMixin):
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: ImportTransactionsTransactionGater,
        sellers: ImportTransactionsSellerCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ) -> None:
        self.transactions = transactions_gateway
        self.sellers = sellers

        super().__init__(EXPENSES_IMPORTED, event_log)

    def execute(self) -> None:
        last_imported_date = None
        for event in self._event_log:  # type: ignore
            if event.name != EXPENSES_IMPORTED:
                continue

            last_imported_date = YearMonthDay(event.data["last_seen_expense"])

        expense_dates = []
        expense_date = None
        for transaction in self.transactions:  # type: ignore
            if (
                last_imported_date
                and last_imported_date >= transaction.date_of_movement
            ):
                continue

            if transaction.value > 0:
                continue  # Ignore income

            expense_dates.append(transaction.date_of_movement)
            expense_date = YearMonthDay(transaction.date_of_movement)

            value = Money(int(str(transaction.value).replace(".", "")))

            self.sellers[transaction.seller] = Seller(
                transaction.seller,
                Category("Other"),
            )

            self.emit(
                event_name=EXPENSE_MADE,
                value=int(value),  # type: ignore
                date_of=str(expense_date),  # type: ignore
                description=transaction.seller,  # type: ignore
            )

        if not expense_date:
            return

        self.emit(last_seen_expense=str(YearMonthDay(sorted(expense_dates)[-1])))  # type: ignore
