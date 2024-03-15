"""
Object-oriented approach to the 4-chain search algorithm.
"""

# annotations
from typing import Union, Tuple, Iterable, Generator

# external
from warnings import warn as _warn
from itertools import cycle as _cycle
from conwech import lexicon as _lexicon

# internal
from four._core import (
    PERIOD_PATTERN as _PERIOD_PATTERN,
    KEY_PERIOD_VALUES as _KEY_PERIOD_VALUES,
    KEY_PERIOD_EXCEPTIONS as _KEY_PERIOD_EXCEPTIONS,
    rebase as _rebase,
    occurs as _occurs,
    letters as _letters,
    status as _status)


__all__ = [
    "RPeriodLike",
    "PNumberLike",
    "RPeriod",
    "PNumber"]


RPeriodLike = Union[int, Tuple[int, int], 'RPeriod']
PNumberLike = Union[int, str, Iterable[RPeriodLike]]


_cli_verbosity: int = 0
"""
Determines how verbose CLI output is for _number_from_name_length.
"""


def C(length: int = 1, chain_index: int = 1): # noqa
    """"""
    this_rank = [[PNumber(4)]]
    while any(len(c) < length for c in this_rank):
        next_rank = []
        for this_chain in this_rank:
            count = 0
            child = _first(this_chain[-1])
            while child is not None and count < chain_index:
                index = 0
                for next_chain in next_rank:
                    if child < next_chain[-1]:
                        break
                    index += 1
                next_rank.insert(index, [*this_chain, child])
                child = _next(child)
                count += 1
        if len(next_rank) == 0:
            for this_chain in this_rank:
                child = _next(this_chain[-1])
                next_rank.append([*this_chain[:-1], child])
        this_rank = next_rank[:chain_index]

    if len(this_rank) < chain_index:
        raise IndexError(f"C[{length}][{chain_index}] does not exist!")

    return this_rank[chain_index - 1]


def _first(target: PNumberLike) -> Union['PNumber', None]:
    """
    Find the first integer with a name of target length.

    Args:
        target: The number of letters that should be in the name of the
            number returned.

    Returns:
        A PNumber representing the next number with the target number of
        letters in its name.

    Examples:
        >>> _first(23)
        [(323, 1)]

        >>> _first(323)
        [(1, 1), (103, 1), (323, 1), (373, 8)]
    """
    target = target if isinstance(target, PNumber) else PNumber(target)

    if target < 3:
        return None
    if target == 4:
        return PNumber(0)
    if target <= 24:
        return PNumber(_KEY_PERIOD_VALUES[int(target)])

    # defined once for reuse in _letters function
    _end = "\n" if _cli_verbosity > 2 else "\r"

    def _letters(number: PNumber):
        letters = number.name_length
        if _cli_verbosity > 1:
            _status(number, letters, end=_end)
        return letters

    # delayed to avoid circular import
    from four.infer import exact_quotient_predictions as predictor
    target_number_periods, = predictor([target.num_periods, ])
    r_periods = PNumber([(373, target_number_periods), ])
    while _letters(r_periods) < target:
        r_periods[0].repeat *= 2

    l_periods = PNumber(373)
    m_periods = PNumber(373)
    r_oneless = PNumber([(373, r_periods[0].repeat - 1), ])
    while not (r_oneless.name_length < target <= r_periods.name_length):
        m_periods[0].repeat = (l_periods[0].repeat + r_periods[0].repeat) // 2
        if _letters(m_periods) < target:
            l_periods[0].repeat = m_periods[0].repeat
        else:
            r_periods[0].repeat = m_periods[0].repeat
            r_oneless[0].repeat = r_periods[0].repeat - 1

    periods = PNumber(r_periods)
    while _letters(periods) > target:
        periods.prepend((1, 1))
        periods[-1].repeat -= 1

    periods[0].repeat -= 1
    periods.insert(1, (0, 1))
    for length, period in _KEY_PERIOD_VALUES.items():
        periods[1].value = period
        if _letters(periods) == target:
            break

    if periods[-1].repeat > 0 and periods[1].value in _KEY_PERIOD_EXCEPTIONS.keys():
        periods[1].value = _KEY_PERIOD_EXCEPTIONS[periods[1].value]
        periods.insert(2, (323, 1))
        periods[-1].repeat -= 1

    return PNumber(str(periods))


def _next(node: PNumberLike) -> Union['PNumber', None]:
    """"""
    node = node if isinstance(node, PNumber) else PNumber(node)

    if node == 0:
        return PNumber(5)

    lsp_value = node[-1].value
    lsp_length = _letters(_lexicon.NATURAL_NUMBERS_LT_1000[lsp_value])
    new_value = next(
        (period for period, numeral
         in enumerate(
            _lexicon.NATURAL_NUMBERS_LT_1000[lsp_value + 1:],
            start=lsp_value + 1)
         if _letters(numeral) == lsp_length),
        None)

    result = PNumber(str(node))
    if new_value is None:
        # todo...
        return None
    else:
        if result[-1].repeat > 1:
            result[-1].repeat -= 1
            result.append((new_value, 1))
        elif result[-1].repeat == 1:
            result[-1].value = new_value

    return result


def _last(target: PNumberLike) -> Union['PNumber', None]:
    """
    Find the largest positive integer with a name of target length.

    Args:
        target: The number of letters that should be in the name of the
            number returned.

    Returns:
        A PNumber representing the largest number with the target number
        of letters in its name.

    Examples:
        >>> print(_last(9))
        96

        >>> print(_last(10))
        10[000]{3}

        >>> print(_last(23))
        10[000]{100002003}
    """
    target = target if isinstance(target, PNumber) else PNumber(target)
    if target < 3:
        return None
    if target < 10:
        return PNumber({3: 10, 4: 9, 5: 60, 6: 90, 7: 70, 8: 66, 9: 96}[int(target)])

    target = int(target)
    budget = target - len("ten") - len("on")
    quotient, remainder = divmod(budget, 5)
    if remainder == 0:
        # f"ten {'billi' * quotient}on"
        return PNumber([(10, 1), (0, int("002" * quotient) + 1)])
    elif remainder == 1:
        # f"ten trilli{'billi' * (quotient - 1)}on"
        return PNumber([(10, 1), (0, int("3" + "002" * (quotient - 1)) + 1)])
    elif remainder == 2:
        # f"ten decilli{'billi' * (quotient - 1)}on"
        return PNumber([(10, 1), (0, int("10" + "002" * (quotient - 1)) + 1)])
    elif remainder == 3:
        # f"ten centilli{'billi' * (quotient - 1)}on"
        return PNumber([(10, 1), (0, int("100" + "002" * (quotient - 1)) + 1)])
    elif remainder == 4:
        if quotient == 1:
            # "nine centillion"
            return PNumber([(9, 1), (0, 101)])
        else:
            # f"ten centillitrilli{'billi' * (quotient - 2)}on"
            return PNumber([(10, 1), (0, int("100003" + "002" * (quotient - 2)) + 1)])


class PNumber(list):
    """
    A number as a list of RPeriods.
    """

    def __init__(self, number: PNumberLike = None, debug: bool = False):
        """
        A list of RPeriods like (P, R) where P is the value of the
        RPeriod and R is the number of times that period repeats.

        Args:
            number: A number or sequence of RPeriods.
            debug: If true, print debug information whenever certain
                attributes are calculated. Generally only inteneded for
                use with CLI

        Examples:
            >>> PNumber(123000000000)
            [(123, 1), (0, 3)]

            >>> PNumber("123[000]{3}")
            [(123, 1), (0, 3)]

            >>> PNumber([(123, 1), (0, 3)])
            [(123, 1), (0, 3)]

        See Also:
            - :class:`RPeriod`
            - :attr:`four._core.PERIOD_PATTERN`
        """
        super().__init__()
        self.debug = bool(debug)
        if isinstance(number, int):
            self.extend(PNumber._iter_periods_from_int(number))
        elif isinstance(number, str):
            self.extend(PNumber._iter_periods_from_str(number))
        elif number is not None:
            self.extend(number)

    @staticmethod
    def _iter_periods_from_int(number: int) -> Generator['RPeriod', None, None]:
        """
        Generates RPeriods from an integer.

        Args:
            number: The integer to pull RPeriods from.

        Yields:
            RPeriod: Each RPeriod identified in the given number.

        Raises:
            TypeError: When number is not of type int.
        """
        if not isinstance(number, int):
            raise TypeError(f"number must be of type {int}!")

        yield from (
            RPeriod(period, 1)
            for period, _ in _rebase(number, 1000))

    @staticmethod
    def _iter_periods_from_str(number: str) -> Generator['RPeriod', None, None]:
        """
        Generates RPeriods from a string.

        Args:
            number: The string to pull RPeriods from.

        Yields:
            RPeriod: Each RPeriod identified in number.

        Raises:
            TypeError: When number is not of type str.
            ValueError: When number string is improperly formatted.

        See Also:
            - :attr:`four._core.PERIOD_PATTERN`
        """
        if not isinstance(number, str):
            raise TypeError(f"number must be of type {str}!")

        for match in _PERIOD_PATTERN.finditer(number):
            period, repeat, error = match.groups()
            if error is not None:
                raise ValueError(f"invalid string segment: '{error}'")
            yield RPeriod(int(period), int(repeat or 1))

    @property
    def num_periods(self) -> int:
        """
        The number of periods in this PNumber.
        """
        return max(0, sum((repeat for _, repeat in self)))

    @property
    def zillion(self) -> int:
        """
        One less than the number of periods in this PNumber.
        """
        return self.num_periods - 1

    @property
    def name_length(self) -> 'PNumber':
        """
        Number of letters in this PNumber's name.
        """
        return PNumber(self._value_letters + self._name_letters)

    @property
    def _value_letters(self) -> int:
        """
        Letters attributed to period values in the number's numeral.
        """
        if self.zillion == -1:
            return 0
        if all([period.value == 0 for period in self]):
            return len("zero")
        return sum((
            repeat * _letters(_lexicon.NATURAL_NUMBERS_LT_1000[value])
            for value, repeat in self))

    @property
    def _name_letters(self) -> int:
        """
        Letters attributed to period names in the number's numeral.
        """
        if self.zillion < 0:
            return 0

        prefix_lengths = [
            len(f"{prefix}illi")
            for prefix in _lexicon.ZILLION_PERIOD_PREFIXES]

        def _from_names_in_range(min_z, max_z):
            return sum([
                sum((_occurs(period, max_z, max(0, min_z), base=1000)
                     * prefix_lengths[period]
                     for period in range(1000))),
                (max_z - max(0, min_z)) * len("on"),
                len("thousand") - len("nillion") if min_z <= 0 < max_z else 0])

        zillion, missing = -1, 0
        for period in self[::-1]:
            zillion += period.repeat
            if period.value == 0:
                missing += _from_names_in_range(
                    zillion - period.repeat, zillion)

        return _from_names_in_range(0, zillion) - missing

    def __setitem__(
            self, index: Union[int, slice],
            periods: Union[RPeriodLike, Iterable[RPeriodLike]]) -> None:
        if isinstance(index, int):
            index = slice(index, index + 1)
            periods = [periods, ]

        periods = [RPeriod(period) for period in periods]

        super().__setitem__(index, periods)
        self._compress()

    def __delitem__(self, index: Union[int, slice]) -> None:
        super().__delitem__(index)
        self._compress()

    def __int__(self) -> int:
        return self.approximate(self.num_periods)

    def __str__(self) -> str:
        return ''.join(str(period) for period in self).lstrip('0')

    def __eq__(self, other: PNumberLike) -> bool:
        return self._compare(other) == 0

    def __ne__(self, other) -> bool:
        return self._compare(other) != 0

    def __lt__(self, other: PNumberLike) -> bool:
        return self._compare(other) < 0

    def __gt__(self, other: PNumberLike) -> bool:
        return self._compare(other) > 0

    def __le__(self, other: PNumberLike) -> bool:
        return self._compare(other) <= 0

    def __ge__(self, other: PNumberLike) -> bool:
        return self._compare(other) >= 0

    def _compare(self, other: PNumberLike) -> Union[int, float]:
        """
        Compare two PNumber objects.

        Args:
            other: The other PNumber to compare to self.

        Returns:
            An integer; negative when self < other, positive when
                self > other, and 0 when self == other.
        """
        other = PNumber(other)
        if str(self) == str(other):
            return 0

        difference = self.zillion - other.zillion
        if difference != 0:
            return difference / abs(difference)

        periods = zip(_cycle(self), _cycle(other))
        for slf, oth in periods:
            difference = slf.value - oth.value
            if difference != 0:
                return difference
            if slf.repeat < oth.repeat:
                return next(periods, [slf, oth])[0].value - oth.value
            if slf.repeat > oth.repeat:
                return slf.value - next(periods, [slf, oth])[1].value

    def _compress(self) -> None:
        """
        Housekeeping method for combining RPeriods when necessary.
        """
        index = 0
        while index < len(self) - 1:
            if self[index].value == self[index + 1].value:
                self[index].repeat += self[index + 1].repeat
                del self[index + 1]
            else:
                index += 1

    def extend(self, periods: Iterable[RPeriodLike]) -> None:
        """
        Append the given periods to this PNumber.

        Args:
            periods: A sequence of RPeriods.
        """
        self.__setitem__(slice(len(self), None), list(periods))

    def append(self, period: RPeriodLike) -> None:
        """
        Append the given period to this PNumber.

        Args:
            period: An RPeriod to append.
        """
        self.__setitem__(slice(len(self), None), [period, ])

    def prepend(self, period: RPeriodLike) -> None:
        """
        Append the given period to the front of this PNumber.

        Args:
            period: An RPeriod to prepend.
        """
        self.__setitem__(slice(None, 0), [period])

    def insert(self, index: Union[int, slice], period: RPeriodLike) -> None:
        """
        Insert the given period into the PNumber at the given index.

        Args:
            index: The index to put period.
            period: An RPeriod to insert.
        """
        self.__setitem__(slice(index, index), [period, ])

    def inject(self, zillion: int, period: RPeriodLike) -> None:
        """
        Inject the given period at a specific zillion value.

        Args:
            zillion: The zillion value of the period to inject.
            period: An RPeriod to inject.
        """
        period = RPeriod(period)
        if zillion > self.zillion:
            self.insert(0, period)

        last_zillion = -1
        this_zillion = -1
        for index in range(len(self) - 1, -1, -1):
            this_zillion += self[index].repeat
            if this_zillion >= zillion:
                if self[index].value == period.value:
                    self[index].repeat += period.repeat
                else:
                    self[index:index+1] = [
                        (self[index].value, this_zillion - zillion),
                        period,
                        (self[index].value, zillion - last_zillion)
                    ]
                break
            last_zillion += self[index].repeat

    def approximate(self, num_periods: int = 1) -> int:
        """
        Get an approximated value for this PNumber.

        Args:
            num_periods: The number of periods to use in the
                approximation; default = 1.

        Returns:
            The value of this PNumber approximated to the given number
            of periods.
        """
        if self.num_periods > 100000 and num_periods > 100000:
            _warn(
                f"{self} is very large! Integer approximation may be costly!",
                ResourceWarning)

        result = ""
        exponent = max(0, self.num_periods - num_periods)
        for value, repeat in self:
            result += str(value).zfill(3) * min(repeat, num_periods)
            num_periods -= repeat
            if num_periods <= 0:
                break

        return int(result or 0) * 1000 ** exponent


class RPeriod:
    """
    Basic container for a repeated period.
    """

    def __init__(self, value: RPeriodLike, repeat: int = 1):
        """
        One or more consecutive periods in a number with the same value
        represented as a tuple-like container (P, R) where P is a valid
        period value in the range [0, 1000), and R is the number of
        times P is repeated.

        Args:
            value: The value of the period.
            repeat: Number of times this period repeats.

        Examples:
            >>> RPeriod(123)
            (123, 1)

            >>> RPeriod(123)
            (12, 3)

            >>> RPeriod((1, 23))
            (1, 23)

        See Also:
            - :class:`PNumber`
        """
        self.__value: int = 0
        self.__repeat: int = 0

        if not isinstance(value, int):
            self.value, self.repeat = value
        else:
            self.value = value
            self.repeat = repeat

    def __iter__(self) -> Generator[int, None, None]:
        yield self.value
        yield self.repeat

    def __repr__(self) -> str:
        return f"({self.value}, {self.repeat})"

    def __str__(self) -> str:
        if self.repeat < 1:
            return ""
        if self.repeat == 1:
            return str(self.value).zfill(3)
        if self.repeat > 1:
            return f"[{str(self.value).zfill(3)}]{{{self.repeat}}}"

    @staticmethod
    def check_value(value: int) -> None:
        """
        Asserts RPeriod value validity; called whenever the value of an
        RPeriod is set.

        Args:
            value: An RPeriod value.

        Raises:
            TypeError: When value is not an int.
            ValueError: When value is not in the range [0, 1000).

        Examples:
            >>> RPeriod("123")
            Traceback (most recent call last):
            ...
            TypeError: RPeriod value must be <class 'int'>; got <class 'str'>

            >>> RPeriod(-1)
            Traceback (most recent call last):
            ...
            ValueError: RPeriod value must be in range [0, 1000); got -1

            >>> RPeriod(1000)
            Traceback (most recent call last):
            ...
            ValueError: RPeriod value must be in range [0, 1000); got 1000
        """
        if not isinstance(value, int):
            raise TypeError(
                f"RPeriod value must be {int}; got {type(value)}")
        if value not in range(1000):
            raise ValueError(
                f"RPeriod value must be in range [0, 1000); got {value}")

    @staticmethod
    def check_repeat(repeat: int) -> None:
        """
        Asserts RPeriod repeat validity; called whenever the repeat of
        an RPeriod is set.

        Args:
            repeat: An RPeriod repeat.

        Raises:
            TypeError: When repeat is not an int.
            ValueError: When repeat < 0.

        Examples:
            >>> RPeriod(123, None)
            Traceback (most recent call last):
            ...
            TypeError: RPeriod repeat must be <class 'int'>; got <class 'NoneType'>

            >>> RPeriod(32, -1)
            Traceback (most recent call last):
            ...
            ValueError: RPeriod repeat must be positive; got -1
        """
        if not isinstance(repeat, int):
            raise TypeError(
                f"RPeriod repeat must be {int}; got {type(repeat)}")
        if repeat < 0:
            raise ValueError(
                f"RPeriod repeat must be positive; got {repeat}")

    @property
    def value(self) -> int:
        """
        The period value in the range [0, 1000).
        """
        return self.__value

    @value.setter
    def value(self, value: int) -> None:
        """
        Setter for value property.
        """
        RPeriod.check_value(value)
        self.__value = value

    @property
    def repeat(self) -> int:
        """
        The number of times this period is repeated.
        """
        return self.__repeat

    @repeat.setter
    def repeat(self, repeat: int) -> None:
        """
        Setter for repeat property.
        """
        RPeriod.check_repeat(repeat)
        self.__repeat = repeat
