from typing import Any, Iterator

from turbofan.database import text

from profitpulse.lib.seller import Category, Seller
from profitpulse.services.assign_category import AssignCategorySellerCollector
from profitpulse.services.import_transactions import ImportTransactionsSellerCollector


class Sellers(AssignCategorySellerCollector, ImportTransactionsSellerCollector):
    def __init__(self, session: Any) -> None:
        self._session = session

    def __getitem__(self, name: str) -> Seller:
        sql_stmt = """
            SELECT s.name, (SELECT name FROM category WHERE id=s.category_id )
              FROM seller s
             WHERE name=:name
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=name)
        row = self._session.execute(prepared_statement).first()
        if not row:
            raise KeyError

        if row[1]:
            return Seller(row[0], Category(row[1]))

        return Seller(row[0])

    def __setitem__(self, name: str, seller: Seller) -> None:
        sql_stmt = """
           INSERT INTO seller (name, category_id)
                VALUES (:name, (SELECT id FROM category WHERE name=:category_name))
           ON CONFLICT (name)
         DO UPDATE SET category_id = excluded.category_id;
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(
            name=name, category_name=str(seller.category)
        )
        self._session.execute(prepared_statement)

    def __iter__(self) -> Iterator[Seller]:
        sql_stmt = """
            SELECT s.name, (SELECT name FROM category WHERE id=s.category_id )
              FROM seller s
        """
        prepared_statement = text(sql_stmt)
        results = self._session.execute(prepared_statement)
        for row in results:
            if row[1]:
                yield Seller(row[0], Category(row[1]))
            else:
                yield Seller(row[0])
