import abc
from typing import Any


class View(abc.ABC):
    """
    Represents a view over the system data.
    """

    @property
    @abc.abstractmethod
    def data(self) -> Any:
        """
        Return data structures with values obtained from the data sources without
        any changes over those values.
        """
        ...  # pragma: no cover
