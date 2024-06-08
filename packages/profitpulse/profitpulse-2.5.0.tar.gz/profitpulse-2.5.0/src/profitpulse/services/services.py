from __future__ import annotations

import typing

import pastperfect


class EventLogger(typing.Protocol):
    def append(
        self, event: pastperfect.Event
    ) -> pastperfect.Events: ...  # pragma: no cover


class EventEmitterMixin:
    def __init__(
        self,
        event_name: str,
        event_log: EventLogger,
        *_: typing.Any,
        **___: typing.Dict[typing.Any, typing.Any],
    ) -> None:
        if event_log is None:
            raise Exception("'Event logged' service must have an event log")
        self._event_log = event_log
        self._event_name = event_name

    def emit(
        self, event_name: typing.Optional[str] = None, **kwargs: dict[str, typing.Any]
    ) -> None:
        en = self._event_name
        if event_name:
            en = event_name

        self._event_log.append(pastperfect.Event(name=en, data=kwargs))


# class StrEnum(str, Enum):
#     # Once python3.9 and python.3.10 support is dropped, we can use
#     # https://docs.python.org/3/library/enum.html#enum.StrEnum
#     pass
#
#
# class PulseEvent(StrEnum):
#     ASSET_DEPOSITED = "1"
#     TRANSACTION_IMPORTED = "2"
#     ASSET_REVALUED = "3"
