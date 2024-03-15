"""
Common functions and artifacts shared between other submodules.
"""

# annotations
from typing import Any, Tuple, Generator

# external
import re as _re
import math as _math


__all__ = [
    "PERIOD_PATTERN",
    "KEY_PERIOD_VALUES",
    "KEY_PERIOD_EXCEPTIONS",
    "rebase",
    "occurs",
    "letters",
    "status"]


PERIOD_PATTERN = _re.compile(
    r"\[?(?P<period>"
    r"^\d{1,3}(?=(?:\d{3})*(?:\[\d|$))"
    r"|(?<=\d|\})\d{3}(?=\[?\d|$)"
    r"|(?<=\[)\d{3}(?=\]\{\d+\}))"
    r"(?:\]\{)?"
    r"(?P<repeat>(?<=\[\d{3}\]\{)\d+(?=\}))?\}?"
    r"|(?P<error>.+)")
"""
Regular expression for parsing string representations of period-lists.

The pattern is written to iterate over a period-list string and yield
matches for each properly formatted period. A properly formatted period
either appears as a repetition like "[P]{R}" where R > 0, or as exactly
3 digits. A period with fewer than 3 digits may appear, but only at the
very beginning of the period-list string.

Each match has the following named capture groups:

    period:
        Captures the value of each period.
    repeat:
        Captures the repeat value when the captured period is a
        repetition, otherwise None.
    error:
        Captures any improper formatting; None when the period-list
        string is well-formed. If error is captured, period and repeat
        will be None.

Examples:
    >>> for match in PERIOD_PATTERN.finditer("12345[678]{9}000"):
    ...     print(match.groupdict())
    ...
    {'period': '12', 'repeat': None, 'error': None}
    {'period': '345', 'repeat': None, 'error': None}
    {'period': '678', 'repeat': '9', 'error': None}
    {'period': '000', 'repeat': None, 'error': None}

    >>> for match in PERIOD_PATTERN.finditer("12345[678]{90}00"):
    ...     print(match.groupdict())
    ...
    {'period': '12', 'repeat': None, 'error': None}
    {'period': '345', 'repeat': None, 'error': None}
    {'period': '678', 'repeat': '90', 'error': None}
    {'period': None, 'repeat': None, 'error': '00'}
"""


KEY_PERIOD_VALUES = {
    3:  1,    # one
    4:  4,    # four
    5:  3,    # three
    6:  11,   # eleven
    7:  15,   # fifteen
    8:  13,   # thirteen
    9:  17,   # seventeen
    10: 24,   # twenty-four
    11: 23,   # twenty-three
    12: 73,   # seventy-three
    13: 101,  # one hundred one
    14: 104,  # one hundred four
    15: 103,  # one hundred three
    16: 111,  # one hundred eleven
    17: 115,  # one hundred fifteen
    18: 113,  # one hundred thirteen
    19: 117,  # one hundred seventeen
    20: 124,  # one hundred twenty-four
    21: 123,  # one hundred twenty-three
    22: 173,  # one hundred seventy-three
    23: 323,  # three hundred twenty-three
    24: 373,  # three hundred seventy-three
}
"""
A dictionary mapping letter-efficient period values by the number of
letters in their numerals.

Examples:
    >>> from four import letters
    >>> KEY_PERIOD_VALUES[letters("seventy-three")]
    12
"""


KEY_PERIOD_EXCEPTIONS = {
    4:   3,    # four < three
    15:  13,   # fifteen < thirteen
    24:  23,   # twenty-four < twenty-three
    104: 103,  # one hundred four < one hundred three
    115: 113,  # one hundred fifteen < one hundred thirteen
    124: 123,  # one hundred twenty-four < one hundred twenty-three
}
"""
Exceptions to KEY_PERIOD_VALUES for numbers with more than two periods.
"""


def rebase(decimal: int, base: int) -> Generator[Tuple[int, int], None, None]:
    """
    Get a tuple representation of decimal in the specified base.

    Args:
        decimal (int): Decimal (base-10) number to rebase.
        base (int): New base for decimal value.

    Yields:
        Tuple[int, int]: Tuples of (c, p) pairs representing digits in
        the new base, where c is the digit’s coefficient (in decimal)
        and p is the power that the new base, b, is raised to. I.e.
        (c, p) pairs such that the following equality holds:

        .. math:: n = \\sum (c \\times b^p \\mid (c, p) \\in R(n, b))

        Digits are yielded in order of significance, the first being
        most significant and last being the least.

    Examples:
        >>> list(rebase(123456789, 16))
        [(7, 6), (5, 5), (11, 4), (12, 3), (13, 2), (1, 1), (5, 0)]

        >>> list(rebase(123456789, 1000))
        [(123, 2), (456, 1), (789, 0)]
    """
    digits = _math.floor(_math.log(abs(decimal) or 1, base))
    yield from (
        ((decimal // base**power) % base, power)
        for power in range(digits, -1, -1))


def occurs(digit: int, limit: int, start: int = 0, base: int = 10) -> int:
    """
    Get the number of times digit occurs in the range [start, limit).

    .. math::

    Args:
        digit (int): The value of the digit to count in base-10.
        limit (int): The upper limit of the search (exclusive).
        start (int): The lower limit of the search (inclusive);
            default = 0.
        base (int): The number system base for digit; default = 10.

    Returns:
        int: The number of times digit occurs within the given range in
        a number system with the given base.

    Examples:
        >>> occurs(0, 100)
        10

        >>> occurs(1, 25, start=16)
        5

        >>> occurs(12, 100, base=16)
        6

        >>> occurs(123, 987654321, base=1000)
        2975655
    """
    if digit >= base or limit <= start:
        return 0

    if start < limit <= 0:
        return occurs(digit, abs(start) + 1, abs(limit) + 1, base)
    if start < 0 < limit:
        return occurs(digit, limit, 0, base) + occurs(digit, abs(start) + 1, 1, base)
    if 0 < start < limit:
        return occurs(digit, limit, 0, base) - occurs(digit, start, 0, base)

    # count = 0 if digit != 0 else 1
    # for coefficient, power in rebase(limit, base):
    #     power_of_base = base ** power
    #     count += power_of_base * (limit // base ** (power + 1))
    #     if coefficient > digit > 0:
    #         count += power_of_base
    #     elif coefficient == digit:
    #         count += limit % power_of_base
    #
    # return count

    count = 0 if digit != 0 else 1
    for coefficient, power in rebase(limit, base):
        power_of_base = base ** power
        count += power_of_base * (limit // base ** (power + 1))
        if digit < coefficient:
            count += power_of_base
        if digit == coefficient:
            count += limit % power_of_base
        if digit == 0:
            count -= power_of_base

    return count

    # return sum((
    #     sum((
    #         base**power * (limit // base**(power+1)),
    #         base**power if coefficient > digit else 0,
    #         limit % base**power if coefficient == digit else 0,
    #         -1 * base**power if digit == 0 else 0
    #     )) for coefficient, power in rebase(limit, base)
    # )) + (1 if digit == 0 else 0)


def count(digit, limit, position=None):
    import re
    total = 0
    if position is None:
        for num in range(limit):
            total += len(list(re.finditer(str(digit), str(num))))
    else:
        for num in range(limit):
            if str(num).zfill(len(str(limit)))[position-1] == str(digit):
                total += 1
    return total


def letters(string: str) -> int:
    """
    Get the number of letters in the given string.

    Args:
        string: The string to count letters in.

    Returns:
        int: The number of letters in string.

    Examples:
        >>> letters("hello world!")
        10
    """
    return len(_re.findall(r"[a-zA-Z]", string))


def status(number: Any, letters: Any, **kwargs) -> None:
    """
    Print a status message with number and letters.

    Args:
        number: The number to report on.
        letters: The number of letters in number.
        **kwargs: Additional keyword arguments to pass to print().

    Returns:
        None

    Examples:
        >>> status(1, 3)
        There are 3 letters in 1

        >>> status(1, 3, end="!")
        There are 3 letters in 1!
    """
    print(
        f"There are {str(letters)}"
        f" letters in {str(number)}"
        + " " * 10 + "\b" * 10,
        **kwargs)
