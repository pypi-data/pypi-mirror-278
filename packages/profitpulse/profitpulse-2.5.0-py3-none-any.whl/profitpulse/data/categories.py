from typing import Any, Iterable

from turbofan.database import text

from profitpulse.lib.seller import Category
from profitpulse.services.assign_category import AssignCategoryCategoryCollector


class Categories(AssignCategoryCategoryCollector):
    def __init__(self, session: Any) -> None:
        self._session = session

    def __getitem__(self, name: str) -> Category:
        sql_stmt = "SELECT * FROM category WHERE name=:name"
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=name)
        row = self._session.execute(prepared_statement).first()
        if not row:
            raise KeyError

        return Category(row[0])

    def __setitem__(self, name: str, category: Category) -> None:
        sql_stmt = "INSERT INTO category (name, budget) VALUES (:name, 0)"
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=name)
        self._session.execute(prepared_statement)

    def __iter__(self) -> Iterable[Category]:
        sql_stmt = "SELECT name FROM category"
        prepared_statement = text(sql_stmt)
        results = self._session.execute(prepared_statement)
        for row in results:
            yield Category(row[0])
