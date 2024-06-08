from datetime import datetime
from typing import Union

from typing_extensions import Self


class YearMonthDay(datetime):
    def __new__(cls, date: Union[str, datetime]) -> Self:
        if isinstance(date, str):
            # because sometimes it receives "2024-05-29 00:00:00", it must be
            # split
            date = datetime.strptime(date.split(" ")[0], "%Y-%m-%d")
        return datetime.__new__(cls, date.year, date.month, date.day)

    def __str__(self) -> str:
        return self.strftime("%Y-%m-%d")
