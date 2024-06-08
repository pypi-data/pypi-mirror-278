from typing import Any


def assert_string_equals(expected: str, got: Any) -> None:
    """
    Compares an object objects in its string value and raises an AssertionError
    if it's not equal to the expected value.
    """
    __tracebackhide__ = True
    assert str(got) == expected, f"Expected {expected}, got {got}"  # nosec
