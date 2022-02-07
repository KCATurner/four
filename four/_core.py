"""
Common functions and artifacts shared between other submodules.
"""

import re
import math


KEY_PERIOD_VALUES = {
    3:  1,   # one
    4:  4,   # four
    5:  3,   # three
    6:  11,  # eleven
    7:  15,  # fifteen
    8:  13,  # thirteen
    9:  17,  # seventeen
    10: 24,  # twenty-four
    11: 23,  # twenty-three
    12: 73,  # seventy-three
    13: 101, # one hundred one
    14: 104, # one hundred four
    15: 103, # one hundred three
    16: 111, # one hundred eleven
    17: 115, # one hundred fifteen
    18: 113, # one hundred thirteen
    19: 117, # one hundred seventeen
    20: 124, # one hundred twenty-four
    21: 123, # one hundred twenty-three
    22: 173, # one hundred seventy-three
    23: 323, # three hundred twenty-three
    24: 373, # three hundred seventy-three
}
"""
Periods with minimum value and maximum letters.
"""

KEY_PERIOD_EXCEPTIONS = {
    4:   3,
    15:  13,
    24:  23,
    104: 103,
    115: 113,
    124: 123,
}
"""
Exceptions to KEY_PERIODS for numbers with more than two periods.
"""

PERIOD_PATTERN = re.compile(
    r"((?:^\d+)|(?<=\})(?:\d{3})+(?=\[|$)|\[(\d{3})\]\{(\d+)\})|(\d+)")
"""
Regular expression for parsing string representations of period lists.
"""


def rebase(decimal: int, base: int, generate: bool = False):
    """
    Get a tuple representation of decimal in the specified base.

    Args:
        decimal (int): Decimal number to rebase.
        base (int): New base for decimal value.
        generate (bool): Returns generator if True; default = False.

    Returns:
        Tuples of (c, p) pairs such that
            ``sum(c*b**p for c, p in rebase(n, b)) == n``.

    Examples:
        >>> rebase(123456789, 16)
        [(7, 6), (5, 5), (11, 4), (12, 3), (13, 2), (1, 1), (5, 0)]
        >>> rebase(123456789, 1000)
        [(123, 2), (456, 1), (789, 0)]
        >>> type(rebase(123456789, 2, True))
        <class 'generator'>
    """
    digits = math.floor(math.log(abs(decimal) or 1, base))
    result = (((decimal // base**power) % base, power)
              for power in range(digits, -1, -1))
    return result if generate else list(result)


def occurs(digit: int, limit: int, start: int = 0, base: int = 10):
    """
    Get the number of times digit occurs in the range [start, limit).

    Args:
        digit (int): The value of the digit to count in base-10.
        limit (int): The upper limit of the search (exclusive).
        start (int): The lower limit of the search (inclusive); default = 0.
        base (int): The number system base for digit; default = 10.

    Returns:
        The number of times digit occurs within the given range in a
            number system with the given base.

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

    return sum((
        sum((
            base**power * (limit // base**(power+1)),
            base**power if coefficient > digit else 0,
            limit % base**power if coefficient == digit else 0,
            -1 * base**power if digit == 0 else 0
        )) for coefficient, power in rebase(limit, base, True)
    )) + (1 if digit == 0 else 0)


def letters(string: str):
    """
    Get the number of letters in the given string.
    """
    return len(re.findall(r"[a-zA-Z]", string))


def status(number, letters, **kwargs):
    """
    Print a status message with number and the letters
    """
    print(f"there are {str(letters)} letters in {str(number)}" + ' '*10 + '\b'*10, **kwargs)
