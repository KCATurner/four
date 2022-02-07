"""
todo
"""
import warnings
import itertools

from conwech.lexicon import NATURAL_NUMBERS_LT_1000, ZILLION_PERIOD_PREFIXES
from four._core import *


warnings.resetwarnings()
warnings.filterwarnings('always', category=ResourceWarning)


class Period(list):
    """
    todo
    """

    def __init__(self, value: int = 0, repeat: int = 1):
        """
        todo

        Args:
            value (int):
            repeat (int):
        """
        super().__init__([0, 0])
        if repeat > 0:
            self.value = value
            self.repeat = repeat

    @property
    def value(self) -> int:
        """
        todo
        """
        return self[0]

    @value.setter
    def value(self, value: int):
        """
        todo

        Args:
            value (int):

        Returns:
            None
        """
        if not isinstance(value, int):
            raise TypeError(f"period value must be int; got {type(value)}")
        if value not in range(1000):
            raise ValueError(f"period value outside range [0, 1000): {value}")
        self[0] = value

    @property
    def repeat(self) -> int:
        """
        todo
        """
        return self[1]

    @repeat.setter
    def repeat(self, repeat: int):
        """
        todo

        Args:
            repeat (int):

        Returns:
            None
        """
        if not isinstance(repeat, int):
            raise TypeError(f"period repeat must be int; got {type(repeat)}")
        self[1] = max(repeat, 0)

    def __str__(self):
        if self.repeat < 1:
            return ''
        if self.repeat == 1:
            return str(self.value).zfill(3)
        if self.repeat > 1:
            return f'[{str(self.value).zfill(3)}]{{{self.repeat}}}'


class PeriodList(list):
    """
    todo
    """

    def __init__(self, periods=None, debug=False):
        """
        todo

        Args:
            periods:
            debug (bool):
        """
        super().__init__()
        self.debug = bool(debug)
        if isinstance(periods, int):
            self.extend(PeriodList._iter_from_int(periods))
        elif isinstance(periods, str):
            self.extend(PeriodList._iter_from_str(periods))
        elif periods is not None:
            self.extend(periods)

    @staticmethod
    def _iter_from_int(periods):
        """
        todo

        Args:
            periods:

        Yields:

        """
        if not isinstance(periods, int):
            raise TypeError(f"input must be of type {int}!")

        yield from (Period(period) for period, _ in rebase(periods, 1000, True))

    @staticmethod
    def _iter_from_str(periods):
        """
        todo

        Args:
            periods:

        Yields:

        """
        if not isinstance(periods, str):
            raise TypeError(f"input must be of type {str}!")

        for match in PERIOD_PATTERN.finditer(periods):
            segment, value, repeat, error = match.groups()
            if error is not None:
                raise ValueError(f"invalid string segment: '{error}'")
            if segment.isdigit():
                yield from PeriodList._iter_from_int(int(segment))
            else:
                yield Period(int(value), int(repeat))

    @property
    def zillion(self):
        """
        todo
        """
        return max(sum((period.repeat for period in self)), 0) - 1

    @property
    def name_length(self):
        """
        todo
        """
        length = PeriodList(self._value_letters + self._name_letters)

        if self.debug:
            status(str(self), str(length), end='\r')

        return length

    @property
    def _value_letters(self):
        """
        todo
        """
        if self.zillion == -1:
            return 0
        if all([period.value == 0 for period in self]):
            return len("zero")
        return sum((
            repeat * letters(NATURAL_NUMBERS_LT_1000[value])
            for value, repeat in self))

    @property
    def _name_letters(self):
        if self.zillion < 0:
            return 0

        prefix_lengths = [
            len(f"{prefix}illi") for prefix in ZILLION_PERIOD_PREFIXES]

        def _from_names_in_range(min_z, max_z):
            return sum([
                sum((occurs(period, max_z, max(0, min_z), base=1000)
                     * prefix_lengths[period]
                     for period in range(1000))),
                (max_z - max(0, min_z)) * len("on"),
                len("thousand") - len("nillion") if min_z <= 0 < max_z else 0])

        zillion, missing = -1, 0
        for period in self[::-1]:
            zillion += period.repeat
            if period.value == 0:
                missing += _from_names_in_range(zillion - period.repeat, zillion)

        return _from_names_in_range(0, zillion) - missing

    def __setitem__(self, index, periods):
        if isinstance(index, int):
            index = slice(index, index + 1)
            periods = [periods]

        if any(not isinstance(period, Period) for period in periods):
            raise TypeError(f"all items must be of type {Period}!")

        super().__setitem__(index, periods)
        self._compress()

    def __delitem__(self, index):
        super().__delitem__(index)
        self._compress()

    def __int__(self):
        if any(period.repeat > 10000 for period in self):
            warnings.warn(
                f"{self} is exceedingly large! Casting to int may be impossible!",
                ResourceWarning)

        # # worse performance than str.join
        # result = sum((
        #     value * 1000 ** power
        #     for value, power
        #     in zip(*itertools.chain(itertools.repeat(*period) for period in self[::-1]),
        #            range(self.zillion + 1))))

        return int(''.join(str(period.value).zfill(3) * period.repeat for period in self))

    def __str__(self):
        return ''.join(str(period) for period in self).lstrip('0')

    def __lt__(self, other):
        return self._compare(other) < 0

    def __gt__(self, other):
        return self._compare(other) > 0

    def __le__(self, other):
        return self._compare(other) <= 0

    def __ge__(self, other):
        return self._compare(other) >= 0

    def _compare(self, other):
        """
        todo

        Args:
            other:

        Returns:

        """
        if not isinstance(other, PeriodList):
            other = PeriodList(other)
        if self == other:
            return 0

        difference = self.zillion - other.zillion
        if difference != 0:
            return difference

        periods = zip(itertools.cycle(self), itertools.cycle(other))
        for slf, oth in periods:
            difference = slf.value - oth.value
            if difference != 0:
                return difference
            if slf.repeat < oth.repeat:
                return next(periods, [slf, oth])[0].value - oth.value
            if slf.repeat > oth.repeat:
                return slf.value - next(periods, [slf, oth])[1].value

    def _compress(self):
        """
        todo

        Returns:
            None
        """
        index = 0
        while index < len(self) - 1:
            if self[index].value == self[index + 1].value:
                self[index].repeat += self[index + 1].repeat
                del self[index + 1]
            else:
                index += 1

    def extend(self, iterable):
        """
        todo

        Args:
            iterable:

        Returns:
            None
        """
        self.__setitem__(slice(len(self), None), list(iterable))

    def append(self, period):
        """
        todo

        Args:
            period:

        Returns:
            None
        """
        self.__setitem__(slice(len(self), None), [period])

    def prepend(self, period):
        """
        todo

        Args:
            period:

        Returns:
            None
        """
        self.__setitem__(slice(None, 0), [period])

    def insert(self, index, period):
        """
        todo

        Args:
            index:
            period:

        Returns:
            None
        """
        self.__setitem__(slice(index, index), [period])

    def inject(self, zillion, period):
        """
        todo

        Args:
            zillion:
            period:

        Returns:

        """
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
                        Period(self[index].value, this_zillion - zillion),
                        period,
                        Period(self[index].value, zillion - last_zillion)
                    ]
                break
            last_zillion += self[index].repeat


def number_from_name_length(target, debug: bool = False):
    """
    todo

    Args:
        target:
        quiet:
        **kwargs:

    Returns:

    """
    target = PeriodList(target)
    if target < PeriodList(3):
        raise ValueError("No number names shorter than 3 letters!")
    if target == PeriodList(3):
        return PeriodList(6)
    if target == PeriodList(4):
        return PeriodList(5)
    if target <= PeriodList(24):
        return PeriodList(KEY_PERIOD_VALUES[int(target)])

    guess = 1 # = math.ceil(0.0032 * (math.e ** (6.8543 * sum(r for _, r in target))))
    r_periods = PeriodList([Period(373, guess)], debug=debug)
    while r_periods.name_length < target:
        r_periods[0].repeat *= 2

    l_periods = PeriodList(373, debug=False)
    m_periods = PeriodList(373, debug=debug)
    r_oneless = PeriodList([Period(373, r_periods[0].repeat - 1)], debug=False)
    while not (r_oneless.name_length < target <= r_periods.name_length):
        m_periods[0].repeat = (l_periods[0].repeat + r_periods[0].repeat) // 2
        if m_periods.name_length < target:
            l_periods[0].repeat = m_periods[0].repeat
        else:
            r_periods[0].repeat = m_periods[0].repeat
            r_oneless[0].repeat = r_periods[0].repeat - 1

    periods = PeriodList(r_periods, debug=debug)
    while periods.name_length > target:
        periods.prepend(Period(1, 1))
        periods[-1].repeat -= 1

    if periods.name_length < target:
        periods[0].repeat -= 1
        periods.insert(1, Period(0, 1))
        for period in [3, 11, 13, 17, 23, 73, 101, 103, 111, 113, 117, 123, 173, 323]:
            periods[1].value = period
            if periods.name_length >= target:
                periods[1] = Period(period, 1)
                break

    if periods.name_length > target:
        periods[-1].repeat -= 1
        periods.insert(2, Period(323, 1))

    return periods


def main(length: int = 2, start: str = "4", quiet: bool = True):
    """
    todo

    Args:
        length (int):
        start (int):
        **kwargs:

    Returns:
        None
    """
    count = 1
    prev_periods = PeriodList(start)
    while count < length:
        curr_periods = number_from_name_length(prev_periods, debug=not quiet)
        status(curr_periods, prev_periods)
        prev_periods = curr_periods
        count += 1
