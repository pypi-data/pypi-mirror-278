from datetime import datetime, timedelta

import pastperfect
import pytest
from pastperfect import Event

from profitpulse.data.expenses_view import ExpensesView
from profitpulse.lib.year_month_day import YearMonthDay
from profitpulse.services.import_transactions import EXPENSE_MADE

date_now = YearMonthDay(datetime.now())


# fmt: off
@pytest.mark.parametrize(
    "events, expected", [
        ([], []),
        ([Event(name="ARandomEvent", data={})], []),
        (
                [
                    Event(name=EXPENSE_MADE, data={
                        "value": 1,
                        "description": "TheSellerIdentification",
                        "date_of": str(date_now),
                    }),
                    Event(name=EXPENSE_MADE, data={
                        "value": 2,
                        "description": "TheSellerIdentification2",
                        "date_of": str(date_now),
                    })
                ],
                [
                    [1, "TheSellerIdentification", "", str(date_now)],
                    [2, "TheSellerIdentification2", "", str(date_now)]
                ]
        ),
    ])
# fmt: on
def test_expenses_view(tmp_db_session, events, expected):
    evts = pastperfect.Events(tmp_db_session)
    for event in events:
        evts.append(event)

    expenses_view = ExpensesView(tmp_db_session)

    assert expenses_view.data == expected  # nosec


def test_limit_values_matching_a_seller_when_one_is_specified(tmp_db_session):
    events = [
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 1,
                "description": "TheSellerIdentification",
                "date_of": str(date_now),
            },
        ),
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 2,
                "description": "TheSellerIdentification2",
                "date_of": str(date_now),
            },
        ),
    ]
    evts = pastperfect.Events(tmp_db_session)
    for event in events:
        evts.append(event)

    expenses_view = ExpensesView(tmp_db_session, seller="TheSellerIdentification2")

    assert expenses_view.data == [
        [2, "TheSellerIdentification2", "", str(date_now)]
    ]  # nosec


def test_group_by_seller(tmp_db_session):
    events = [
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 1,
                "description": "TheSellerIdentification",
                "date_of": str(date_now),
            },
        ),
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 2,
                "description": "TheSellerIdentification",
                "date_of": str(date_now),
            },
        ),
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 2,
                "description": "TheSellerIdentification2",
                "date_of": str(date_now),
            },
        ),
    ]
    evts = pastperfect.Events(tmp_db_session)
    for event in events:
        evts.append(event)

    expenses_view = ExpensesView(tmp_db_session, group_seller=True)

    assert expenses_view.data == [
        [3, "TheSellerIdentification"],
        [2, "TheSellerIdentification2"],
    ]  # nosec


def test_filter_by_start_date(tmp_db_session):
    yesterday = datetime.now() - timedelta(days=1)

    events = [
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 1,
                "description": "TheSellerIdentification",
                "date_of": yesterday.strftime("%Y-%m-%d"),
            },
        ),
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 2,
                "description": "TheSellerIdentification",
                "date_of": yesterday.strftime("%Y-%m-%d"),
            },
        ),
        Event(
            name=EXPENSE_MADE,
            data={
                "value": 2,
                "description": "TheSellerIdentification2",
                "date_of": str(
                    (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
                ),
            },
        ),
    ]
    evts = pastperfect.Events(tmp_db_session)
    for event in events:
        evts.append(event)

    expenses_view = ExpensesView(
        tmp_db_session, since=datetime.now() - timedelta(days=2)
    )

    assert expenses_view.data == [
        [1, "TheSellerIdentification", "", yesterday.strftime("%Y-%m-%d")],
        [2, "TheSellerIdentification", "", yesterday.strftime("%Y-%m-%d")],
    ]  # nosec
