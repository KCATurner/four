"""
A purely functional programming approach to the 4-chain search
algorithm.
"""

# annotations
from typing import Union, Tuple, List, Sequence

# external
import re as _re
import math as _math
import functools as _functools
from conwech import lexicon as _lexicon

# internal
from four._core import (
    PERIOD_PATTERN as _PERIOD_PATTERN,
    KEY_PERIOD_VALUES as _KEY_PERIOD_VALUES,
    KEY_PERIOD_EXCEPTIONS as _KEY_PERIOD_EXCEPTIONS,
    rebase as _rebase,
    occurs as _occurs,
    status as _status)


__all__ = [
    "number_to_periods",
    "periods_to_number",
    "parse_abbreviation",
    "write_abbreviation",
    "letters_in_period_values",
    "letters_in_period_names",
    "letters_in_number_name"]


_cli_verbosity: int = 0
"""
Determines how verbose CLI output is for _number_from_name_length.
"""


def _first(
        target: Union[int, str, Sequence[Tuple[int, int]]]
) -> List[Tuple[int, int]]:
    """
    Find the first integer with a name of target length.

    Args:
        target: The number of letters that should be in the name of the
            number returned.

    Returns:
        A period-list representing the smallest number with the target
        number of letters in its name.

    Examples:
        >>> _first(23)
        [(323, 1)]

        >>> _first(323)
        [(1, 1), (103, 1), (323, 1), (373, 8)]
    """
    if isinstance(target, str):
        target = parse_abbreviation(target)
    if not isinstance(target, int):
        target = periods_to_number(target)

    if target < 3:
        raise ValueError("No number names shorter than 3 letters!")
    if target == 3:
        return [(6, 1), ]
    if target == 4:
        return [(5, 1), ]
    if target in _KEY_PERIOD_VALUES.keys():
        return [(_KEY_PERIOD_VALUES[target], 1), ]

    # defined once for reuse in _letters function
    _end = "\n" if _cli_verbosity > 2 else "\r"

    @_functools.wraps(letters_in_number_name)
    def _letters(number: Sequence[Tuple[int, int]]):
        letters = letters_in_number_name(number)
        if _cli_verbosity > 1:
            _status(
                write_abbreviation(number),
                write_abbreviation(number_to_periods(letters)),
                end=_end)
        return letters

    # delayed to avoid circular import
    from four.infer import exact_quotient_predictions
    n_max, = exact_quotient_predictions([
        sum(repeat for _, repeat in number_to_periods(target)), ])
    while _letters([(373, n_max), ]) < target:
        n_max *= 2

    n_min = 1
    while not (_letters([(373, n_max - 1), ])
               < target <=
               _letters([(373, n_max), ])):
        n_mid = (n_min + n_max) // 2
        if _letters([(373, n_mid), ]) < target:
            n_min = n_mid
        else:
            n_max = n_mid

    num_letters = _letters([(373, n_max), ])
    min_periods = [(1, _math.ceil((num_letters - target) / 21)), ]
    max_periods = [(373, n_max - min_periods[-1][-1]), ]

    mid_periods = []
    num_letters = _letters([*min_periods, *max_periods])
    if num_letters < target:
        min_periods = [(1, min_periods[-1][-1] - 1), ]
        mid_periods.append((min(
            (period for letters, period in _KEY_PERIOD_VALUES.items()
             if letters - 3 == target - num_letters)), 1))

    if max_periods[-1][-1] > 0 and mid_periods[0][0] in _KEY_PERIOD_EXCEPTIONS.keys():
        mid_periods = [(_KEY_PERIOD_EXCEPTIONS[mid_periods[0][0]], 1), (323, 1)]
        max_periods = [(373, max_periods[-1][-1] - 1), ]

    return [
        (period, repeat)
        for period, repeat
        in [*min_periods, *mid_periods, *max_periods]
        if repeat > 0]


def number_to_periods(number: Union[int, float]) -> List[Tuple[int, int]]:
    """
    Convert a number to a list of (P, R) tuples.

    Args:
        number: A number to convert.

    Returns:
        A list of (P, R) tuples representing the given number, where P
        is a period value to be repeated R number of times before moving
        on to the next tuple in the list.

    Examples:
        >>> number_to_periods(123000000000)
        [(123, 1), (0, 3)]

        >>> number_to_periods(1.23e17)
        [(123, 1), (0, 3)]

    See Also:
        - :func:`periods_to_number`
    """
    periods = []
    for period, _ in _rebase(int(number), base=1000):
        if periods and periods[-1][0] == period:
            periods[-1] = (period, periods[-1][1] + 1)
        else:
            periods.append((period, 1))
    return periods


def periods_to_number(periods: Sequence[Tuple[int, int]]) -> int:
    """
    Convert a sequence of (P, R) tuples to an integer.

    Note:
        Does not scale well with large R values!

    Args:
        periods: A sequence of tuples like (P, R) representing a number,
            where P is a period value to be repeated R number of times
            before moving on to the next tuple in the sequence.

    Returns:
        The integer representation of periods.

    Examples:
        >>> periods_to_number([(123, 1), (0, 3)])
        123000000000

    See Also:
        - :func:`number_to_periods`
    """
    return int("".join(
        str(period).zfill(3) * repeat
        for period, repeat in periods
    ) or 0)


def parse_abbreviation(abbreviation: str) -> List[Tuple[int, int]]:
    """
    Retrieve a number from its given string abbreviation.

    Args:
        abbreviation: A pseudo-numeric string in which repeated periods
            are represented like "[P]{R}" where P is the period value
            and R is the number of times the period is repeated.

    Returns:
        A list of (P, R) tuples representing a number, where P is a
        period value to be repeated R number of times before moving on
        to the next tuple in the list.

    Examples:
        >>> parse_abbreviation("123[456]{2}")
        [(123, 1), (456, 2)]

        >>> parse_abbreviation("[987]{6}543543")
        [(987, 6), (543, 2)]

    See Also:
        - :func:`write_abbreviation`
        - :attr:`four._core.PERIOD_PATTERN`
    """
    periods = []

    for match in _PERIOD_PATTERN.finditer(abbreviation):
        period, repeat, error = match.groups()

        if error is not None:
            raise ValueError(f"invalid abbreviation segment: '{error}'")

        period = int(period)
        repeat = int(repeat or 1)
        if periods and period == periods[-1][0]:
            periods[-1] = (periods[-1][0], periods[-1][1] + repeat)
        else:
            periods.append((period, repeat))

    return periods


def write_abbreviation(number: Sequence[Tuple[int, int]]) -> str:
    """
    Get a more legible abbreviation of the given number.

    Args:
        number: A sequence of tuples like (P, R) representing a number,
            where P is a period value to be repeated R number of times
            before moving on to the next tuple in the sequence.

    Returns:
        A pseudo-numeric string in which repeated periods are
        represented like "[P]{R}" where P is the period value and R is
        the number of times the period is repeated.

    Examples:
        >>> write_abbreviation([(123, 1), (456, 2), (789, 3)])
        '123[456]{2}[789]{3}'

    See Also:
        - :func:`parse_abbreviation`
        - :attr:`four._core.PERIOD_PATTERN`
    """
    return "".join(
        f"[{period:0>3}]{{{repeat}}}" if repeat > 1
        else f"{period:0>3}" if repeat > 0 else ""
        for period, repeat in number).lstrip("0") or "0"


def letters_in_period_values(number: Sequence[Tuple[int, int]]) -> int:
    """
    Count the letters attributed to period values in number's numeral.

    Args:
        number: A sequence of tuples like (P, R) representing a number,
            where P is a period value to be repeated R number of times
            before moving on to the next tuple in the sequence.

    Returns:
        The number of letters attributed to period values in number's
        numeral.

    Examples:
        >>> # "one ... one ... one"
        >>> letters_in_period_values([(1, 3), ])
        9
    """
    if all([int(period) == 0 for period, _ in number]):
        return len("zero")

    return sum((
        repeat * len(_re.findall(
            r"[a-zA-Z]", _lexicon.NATURAL_NUMBERS_LT_1000[int(period)]))
        for period, repeat in number))


def letters_in_period_names(number: Sequence[Tuple[int, int]]) -> int:
    """
    Count the letters attributed to period names in number's numeral.

    Args:
        number: A sequence of tuples like (P, R) representing a number,
            where P is a period value to be repeated R number of times
            before moving on to the next tuple in the sequence.

    Returns:
        The number of letters attributed to period names in number's
        numeral.

    Examples:
        >>> # "... million ... thousand ..."
        >>> letters_in_period_names([(1, 3), ])
        15
    """
    prefix_lengths = [
        len(f"{prefix}illi") for prefix in _lexicon.ZILLION_PERIOD_PREFIXES]

    def from_names_in_range(min_z, max_z):
        # return sum([
        #     sum((_occurs(period, max_z, max(0, min_z), base=1000)
        #          * prefix_lengths[period]
        #          for period in range(1000))),
        #     (max_z - max(0, min_z)) * len("on"),
        #     len("thousand") - len("nillion") if min_z <= 0 < max_z else 0])
        total = (max_z - max(0, min_z)) * len("on")
        for period in range(1000):
            total += _occurs(period, max_z, max(0, min_z), base=1000) * prefix_lengths[period]
        if min_z <= 0 < max_z:
            total += len("thousand") - len("nillion")
        return total

    zillion, missing = -1, 0
    for period, repeat in number[::-1]:
        zillion += repeat
        if int(period) == 0:
            missing += from_names_in_range(zillion - repeat, zillion)

    return from_names_in_range(0, zillion) - missing


def letters_in_number_name(number: Sequence[Tuple[int, int]]) -> int:
    """
    Count all the letters in number's numeral.

    Args:
        number: A sequence of tuples like (P, R) representing a number,
            where P is a period value to be repeated R number of times
            before moving on to the next tuple in the sequence.

    Returns:
        The number of letters in number's numeral.

    Examples:
        >>> # "one million one thousand one"
        >>> letters_in_number_name([(1, 3), ])
        24

    See Also:
        - :func:`letters_in_period_values`
        - :func:`letters_in_period_names`
    """
    return letters_in_period_values(number) + letters_in_period_names(number)
