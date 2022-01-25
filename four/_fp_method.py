"""
todo
"""
from conwech.functions import number2text
from conwech.lexicon import NATURAL_NUMBERS_LT_1000, ZILLION_PERIOD_PREFIXES

from four._core import *


def letters_from_period_values(*number: list):
    """
    Count the letters attributed to period values in number's numeral.

    Args:
        *number (list): A number as a list of (P, R) tuples.

    Returns:
        The number of letters attributed to period values in number's
        numeral.
    """
    if all([int(period) == 0 for period, _ in number]):
        return len("zero")

    return sum((
        repeat * letters(NATURAL_NUMBERS_LT_1000[int(period)])
        for period, repeat in number))


def letters_from_period_names(*number: list):
    """
    Count the letters attributed to period names in number's numeral.

    Args:
        *number (list): A number as a list of (P, R) tuples.

    Returns:
        The number of letters attributed to period names in number's
        numeral.
    """
    prefix_lengths = [
        len(f"{prefix}illi") for prefix in ZILLION_PERIOD_PREFIXES]

    def from_names_in_range(min_z, max_z):
        return sum([
            sum((occurs(period, max_z, max(0, min_z), base=1000)
                 * prefix_lengths[period]
                 for period in range(1000))),
            (max_z - max(0, min_z)) * len("on"),
            len("thousand") - len("nillion") if min_z <= 0 < max_z else 0])

    zillion, missing = -1, 0
    for period, repeat in number[::-1]:
        zillion += repeat
        if int(period) == 0:
            missing += from_names_in_range(zillion - repeat, zillion)

    return from_names_in_range(0, zillion) - missing


def letters_in_number_name(*number: list, debug: bool = False):
    """
    Count all the letters in number's numeral.

    Args:
        *number (list): A number as a list of (P, R) tuples.
        debug (bool): Print extra debug information when true.

    Returns:
        The number of letters in number's numeral.
    """
    letters = sum([
        letters_from_period_values(*number),
        letters_from_period_names(*number)])

    if debug:
        status(write_abbreviation_string(*number),
               write_abbreviation_string(*number_to_periods(letters)),
               end='\r')

    return letters


def number_from_brute_force(target: int, debug: bool = False):
    """
    Find the smallest positive integer with a name of target length.

    Args:
        target (int): The number of letters that should be in the name
            of the number returned.
        debug (bool): Print extra debug information when true.

    Returns:
        A period list representing the smallest number with the target
        number of letters in its name.
    """
    if target < 3:
        raise ValueError("No number names shorter than 3 letters!")

    number = {3: 6, 4: 5, 5: 3}.get(target, 6)
    while letters(number2text(number)) != target:
        if debug:
            status(number, letters(number2text(number)), end='\r')
        number += 1

    return number_to_periods(number)


def number_from_name_length(target: int, debug: bool = False):
    """
    Find the smallest positive integer with a name of target length.

    Args:
        target (int): The number of letters that should be in the name
            of the number returned.
        debug (bool): Print extra debug information when true.

    Returns:
        A period list representing the smallest number with the target
        number of letters in its name.
    """
    if target < 3:
        raise ValueError("No number names shorter than 3 letters!")
    if target == 3:
        return [["006", 1], ]
    if target == 4:
        return [["005", 1], ]

    base = 2
    max_periods = ["373", 1]
    num_letters = letters_in_number_name(max_periods, debug=debug)
    while num_letters < target:
        max_periods[-1] *= base
        num_letters = letters_in_number_name(max_periods, debug=debug)

    # variant of binary search
    for _, power in rebase(max_periods[-1], base, True):
        while num_letters > target:
            max_periods[-1] -= base ** power
            num_letters = letters_in_number_name(max_periods, debug=debug)
        if num_letters < target:
            max_periods[-1] += base ** power
            num_letters = letters_in_number_name(max_periods, debug=debug)

    min_periods = ["001", 0]
    min_periods[-1], remainder = divmod(num_letters - target, 21)
    max_periods[-1] -= min_periods[-1]

    options = {
        0:  [],
        1:  [["323", 1], ], # three hundred twenty-three
        2:  [["173", 1], ], # one hundred seventy-three
        3:  [["123", 1], ], # one hundred twenty-three
        4:  [["124", 1], ], # one hundred twenty-four
        5:  [["117", 1], ], # one hundred seventeen
        6:  [["113", 1], ], # one hundred thirteen
        7:  [["115", 1], ], # one hundred fifteen
        8:  [["111", 1], ], # one hundred eleven
        9:  [["103", 1], ], # one hundred three
        10: [["104", 1], ], # one hundred four
        11: [["101", 1], ], # one hundred one
        12: [["073", 1], ], # seventy-three
        13: [["023", 1], ], # twenty-three
        14: [["024", 1], ], # twenty-four
        15: [["017", 1], ], # seventeen
        16: [["013", 1], ], # thirteen
        17: [["015", 1], ], # fifteen
        18: [["011", 1], ], # eleven
        19: [["003", 1], ], # three
        20: [["004", 1], ], # four
        21: [["001", 1], ], # one
    }

    mid_periods = options[remainder]
    # exceptions where smaller value period has longer name
    if remainder in [4, 7, 10, 14, 17, 20] and max_periods[-1] >= 2:
        mid_periods = options[remainder - 1] + [["323", 1], ]
    max_periods[-1] -= len(mid_periods)

    return [
        (period, repeat)
        for period, repeat
        in [min_periods, *mid_periods, max_periods]
        if repeat > 0]


def number_to_periods(number: int) -> list:
    """
    Convert an integer to a list of (P, R) tuples.

    Args:
        number (int): The integer to convert.

    Returns:
        A list of (P, R) tuples representing number.
    """
    periods = iter(f'{int(number):,}'.split(','))
    result = [[next(periods).zfill(3), 1]]
    for period in periods:
        if period == result[-1][0]:
            result[-1][1] += 1
        else:
            result.append([period, 1])
    return [tuple(p) for p in result]


def number_from_periods(*periods: list) -> int:
    """
    Convert a list of (P, R) tuples to an integer.

    Note:
        Does not scale well!

    Args:
        *periods (list): The list of (period, repeat) tuples to convert.

    Returns:
        The integer representation of periods.
    """
    return int(''.join(v * c for v, c in periods))


def write_abbreviation_string(*periods: list, max_repeat: int = 1) -> str:
    """
    Get a more legible abbreviation of the given periods.

    Args:
        *periods (tuple): A list of tuples like (P, R) representing a
            number, where P is a period value to be repeated N number
            of times before moving on to the next tuple in the list.
        max_repeat (int): Abbreviate a period tuple (P, N) as [P]{N}
            when N > min(max(max_repeat, 1), 1000); default = 1.

    Returns:
        A more legible string representing period_list.

    Examples:
        >>> write_abbreviation_string(('123', 1), ('456', 2))
        '123[456]{2}'
        >>> write_abbreviation_string(('987', 6), ('543', 2), max_repeat=2)
        '[987]{6}543543'

    """
    return ''.join(
        f"[{p}]{{{c}}}" if c > min(max(max_repeat, 1), 1000) else c * str(p).zfill(3)
        for p, c in periods).lstrip('0') or '0'


def parse_abbreviation_string(abbreviation: str):
    """
    Retrieve a list of periods from its string representation.

    Args:
        abbreviation: A numeric string which may contain repeated
            periods represented like [P]{R} where P is the period value
            and N is the number of times the period is repeated.

    Returns:
        A list of tuples like (P, R) representing a number, where P is
        a period value to be repeated N number of times before moving on
        to the next tuple in the list.
    """
    periods = []

    for match in PERIOD_PATTERN.finditer(abbreviation):
        segment, value, repeat, error = match.groups()
        if segment.isdigit():
            periods.extend(
                [str(period).zfill(3), 1]
                for period, _ in rebase(int(segment), 1000, True))
        else:
            periods.append([value, int(repeat)])

    periods = iter(periods)
    result = [next(periods, ["000", 0])]
    for period, repeat in periods:
        if period == result[-1][0]:
            result[-1][-1] += repeat
        else:
            result.append([period, repeat])

    return result


def main(length: int, start: str, quiet: bool = True):
    """
    Entry point for CLI functional method.

    Args:
        length (int): Length of the target chain.
        start (str): Number from which to start.
        quiet (bool): Only print numbers in chain when true.

    Returns:
        None
    """
    count = 1
    prev_periods = parse_abbreviation_string(str(start))
    while count < length:
        target = number_from_periods(*prev_periods)
        curr_periods = number_from_name_length(target, debug=not quiet)
        status(write_abbreviation_string(*curr_periods),
               write_abbreviation_string(*prev_periods))
        prev_periods = curr_periods
        count += 1
