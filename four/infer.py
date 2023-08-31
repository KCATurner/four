"""
Estimate the number of periods in letter-efficient numbers given a
target name length.

CLI Subcommand
==============

.. autoprogram:: four.infer:parser
   :prog: four infer
"""

# annotations
from typing import (
    Tuple, List, Sequence, Iterable, Generator, Callable)

# external
import numpy as _numpy
import argparse as _argparse
from pathlib import Path as _Path
from functools import wraps as _wraps
from decimal import Decimal as _Decimal
from scipy.optimize import curve_fit as _curve_fit
from matplotlib import pyplot as _plt

# internal
from four._oo_api import PNumber, PNumberLike


__all__ = [
    "parser",
    "metadata",
    "LENGTH_PERIODS_TO_TARGET_PERIODS",
    "iter_quick_targets",
    "iter_exact_targets",
    "quick_quotient_predictions",
    "quick_power_predictions",
    "exact_quotient_predictions",
    "exact_power_predictions"]


def metadata(**attributes) -> Callable:
    """
    Add a metadata dict with the given attributes to a function.

    Args:
        **attributes: keyword arguments for the metadata dict to
            be added to any functions decorated by the resulting
            decorator.

    Returns:
        Callable: A function decorator.
    """
    def decorator(function):
        function.metadata = dict(**attributes)
        return function
    return decorator


_NUM_PERIODS_LIMIT: int = 80


# flake8: noqa E501
_LENGTH_PERIODS_TO_TARGETS: Tuple['PNumber', ...] = (
    PNumber("1"),  # special case
    PNumber("23323[373]{10}"),
    PNumber("1113323[373]{6813}"),
    PNumber("[001]{2}101[373]{4871694}"),
    PNumber("[001]{5}123323[373]{3791494971}"),
    PNumber("[001]{3}[373]{3092853994989}"),
    PNumber("1111[373]{2606002475064901}"),
    PNumber("1023[373]{2254991260552259193}"),
    PNumber("[001]{4}011[373]{1979011924519216258099}"),
    PNumber("[001]{6}023[373]{1769139951254665665194745}"),
    PNumber("13[373]{1599094619904847217338965998}"),
    PNumber("[001]{11}113323[373]{1459597675004987823940303423468}"),
    PNumber("1023323[373]{1342630260718287677471881486112769}"),
    PNumber("1[373]{1241974586839600506950334186979234030}"),
    PNumber("[001]{9}103[373]{1154822795145947607586005151997230900878}"),
    PNumber("1173[373]{1078536012673848841885528843874391056212397}"),
    PNumber("[001]{10}003[373]{1011368893462550309303348839638098831508521905}"),
    PNumber("[001]{15}023[373]{952298907634362342715309199373403290388424993440}"),
    PNumber("[001]{6}013323[373]{899582009592966764742145990168693237057157169096767}"),
    PNumber("[001]{9}323[373]{853016277682649080751443513223200504054031722089945126}"),
    PNumber("1111[373]{810842244143078230207178526848445570765639452671396053015}"),
    PNumber("[001]{9}003323[373]{772629157016700279190079590303687484322902672529866859284805}"),
    PNumber("[001]{11}113323[373]{738108150896247048761949783579790129077024324473713590411617993}"),
    PNumber("[001]{23}113[373]{706250496598018934045305116753208728479925160646619335762356070482}"),
    PNumber("[001]{24}111[373]{676991714116884157849439377675579051317959756266912472332511840499179}"),
    PNumber("[001]{26}103323[373]{650187289137337413741767935402059560884890228828331276190907287787851105}"),
    PNumber("[001]{12}323[373]{625370743334828808769672391164150624787772897946318093436104159473006135911}"),
    PNumber("323[373]{602161787945501785691808024798459898599267734515983437405811022825770582378182}"),
    PNumber("[001]{17}111[373]{580790728347595654231718547425758831837688847497539541197768262761298377335527995}"),
    PNumber("[001]{29}003323[373]{560950519157670543253128955152083170154477733834327522851337826267419549587212730810}"),
    PNumber("[001]{19}103323[373]{542469293934532238342458452769793933320365718251515987735582372390744898849938747523698}"),
    PNumber("[001]{22}103323[373]{525077457265377517240598187599087087743988499027922875261418908490442649634380496044544852}"))


LENGTH_PERIODS_TO_TARGET_PERIODS: Tuple[int, ...] = tuple(
    n.num_periods for n in _LENGTH_PERIODS_TO_TARGETS)
"""
Tuple mapping the number of periods `P` in the length `L` of a
number `N`'s name, to the number of periods in `N` for the first
32 most letter-efficient numbers with names of length `L`, where
:math:`L = \\sum_{x=0}^{P} 373 \\times 1000^x` when :math:`P \\ne 0`.
When `P = 0`, `L = 1` since no number can have fewer than 1 period.

Example:
    >>> n = PNumber("1113323[373]{6813}")
    >>> n.name_length == PNumber("[373]{2}")
    True
    >>> LENGTH_PERIODS_TO_TARGET_PERIODS[2] == n.num_periods
    True
"""


def _iter_x_as_period_lists(
        X: Iterable[PNumberLike] # noqa
) -> Generator['PNumber', None, None]:
    """
    Iterate over each value x in X and yield x as a PNumber.

    Args:
        X: Values to cast to PNumbers.

    Yields:
        PNumber: Each value in X cast to a PNumber.
    """
    yield from (
        number if isinstance(number, PNumber)
        else PNumber("373" * int(number) or 0)
        for number in X)


def iter_exact_targets(
        X: Iterable[PNumberLike] # noqa
) -> Generator[int, None, None]:
    """
    Iterate over X yielding the exact value of each PNumber.

    While the exact value of a PNumber is calculated using string
    multiplication and concatenations for performance reasons,
    mathematically it is a nested summation:

    .. math:: x = \\sum_{i=0}^{L}\\sum_{j=L-R}^{R}

    int(''.join(str(value).zfill(3) * repeat for value, repeat in self))

    Args:
        X: todo

    Yields:
        int: The Exact value of each PNumber in X.
    """
    yield from (
        int(periods)
        for periods in _iter_x_as_period_lists(X))


def iter_quick_targets(
        X: Iterable[PNumberLike] # noqa
) -> Generator[int, None, None]:
    """
    Iterate over X yielding the approximate value of each PNumber.

    Each PNumber x in X is approximated by multiplying the value of the
    leading period by the power of 1000 equal to the total number of
    periods in the number x.

    Args:
        X: todo

    Yields:
        int: Approximation for the value of each PNumber in X.
    """
    yield from (
        periods.approximate(num_periods=1)
        for periods in _iter_x_as_period_lists(X))


@metadata(equation_template="F(x) ≈ x / {}")
def quick_quotient_predictions(
        X: Iterable[PNumberLike], # noqa
        a: int = 712275
) -> List[int]:
    """
    Use integer division :math:`p \\approx x \\div a` to predict the
    number of periods `p` in the smallest number `n` with a name `x`
    letters long for each target length in `X` such that
    :math:`n \\approx 373 \\times 1000^p`.

    Args:
        X: Target name lengths.
        a: Integer division denominator.

    Returns:
        List[int]: Predictions for each target length x in X.
    """
    return [
        max(1, int(x) // a)
        for x in iter_quick_targets(X)]


@metadata(equation_template="F(x) ≈ x / {}")
def exact_quotient_predictions(
        X: Iterable[PNumberLike], # noqa
        a: int = 711
) -> List[int]:
    """
    Use integer division :math:`p \\approx x \\div a` to predict the
    number of periods `p` in the smallest number `n` with a name `x`
    letters long for each target length in `X` such that
    :math:`n \\approx \\sum_{i=0}^{p} 373 \\times 1000^i`.

    Args:
        X: Target name lengths.
        a: integer division denominator.

    Returns:
        List[int]: Predictions for each target length x in X.
    """
    return [
        max(1, int(x) // a)
        for x in iter_exact_targets(X)]


@metadata(equation_template="F(x) ≈ {:e} * x^{:e}")
def quick_power_predictions(
        X: Iterable[PNumberLike], # noqa
        a: float = 3.964551835037818e-06,
        b: float = 9.952827374375254e-01
) -> List[float]:
    """
    Use power equation :math:`p \\approx ax^b` to predict the number of
    periods `p` in the smallest number `n` with a name `x` letters long
    for each target length in `X` such that
    :math:`n \\approx\\ 373 \\times 1000^{p}`.

    Args:
        X: Target name lengths.
        a: power equation base coefficient.
        b: power equation exponent.

    Returns:
        List[float]: Predictions for each target length x in X.

    Todo:
        - See if Decimals will work in place of floats.
    """
    return [
        float(a * (int(x) ** b))
        for x in iter_quick_targets(X)]


@metadata(equation_template="F(x) ≈ {:e} * x^{:e}")
def exact_power_predictions(
        X: Iterable[PNumberLike], # noqa
        a: float = 3.8438562337548433e-03,
        b: float = 9.952827374375255e-01
) -> List[float]:
    """
    Use power equation :math:`p \\approx ax^b` to predict the number of
    periods `p` in the smallest number `n` with a name `x` letters long
    for each target length in `X` such that
    :math:`n \\approx \\sum_{i=0}^{p} 373 \\times1000^i`.

    Args:
        X: Target name lengths.
        a: power equation base coefficient.
        b: power equation exponent.

    Returns:
        List[float]: Predictions for each target length x in X.

    Todo:
        - See if Decimals will work in place of floats.
    """
    return [
        float(a * (int(t) ** b))
        for t in iter_exact_targets(X)]


@metadata(equation_template="F(x) ≈ {:e} * x^{:e}")
def prototype_predict(
        X: Iterable[PNumberLike], # noqa
        a: float,
        b: float
) -> List[float]:
    """
    todo

    Args:
        X: Target name lengths.
        a: power equation base coefficient.
        b: power equation exponent.

    Returns:
        List[float]: Predictions for each target length x in X.
    """
    an, ad = _Decimal(a).as_integer_ratio()
    bn, bd = _Decimal(b).as_integer_ratio()

    def get_n_root(n, t) -> int:
        ...  # todo...

    result = []
    for target in iter_exact_targets(X):
        y = (an * (get_n_root(bd, target) ** bn)) // ad
        result.append(y)

    return result


def _infer(
        targets: Sequence['PNumber'],
        graph_result: bool = False,
        use_integer_math: bool = False,
        approximate_targets: bool = False,
        function: Callable = None
) -> None:
    """
    Entry point for four infer.

    Args:
        targets: Target number length(s).
        graph_result: Graph the resulting prediction(s) when True;
            default = False
        use_integer_math: Use equations compatible with integer math
            when True; default = False.
        approximate_targets: Approximate targets by largest period when
            True; default = False.
        function: Ignore use_integer_math and approximate_targets and
            use custom predictive function instead; default None.
    """
    train_y = _numpy.array(LENGTH_PERIODS_TO_TARGET_PERIODS)
    train_x = _numpy.arange(len(train_y), dtype=int)

    func = function or {
        (False, False): exact_power_predictions,
        (False, True): quick_power_predictions,
        (True, False): exact_quotient_predictions,
        (True, True): quick_quotient_predictions,
    }[use_integer_math, approximate_targets]

    # floats required for training but not prediction
    train_func = _wraps(func)(
        lambda *args: _numpy.array([
            float(int(n)) for n in func(*args)]))

    popt, *_ = _curve_fit(train_func, train_x, train_y)
    if use_integer_math:
        popt = [int(arg) for arg in popt]

    target_length_periods = [t.num_periods for t in targets]
    target_number_periods = func(targets, *popt)

    for target, tnp in zip(targets, target_number_periods):
        print(f"The smallest number with a {target}"
              f" letter name is ≈[373]{{{tnp}}}")

    if graph_result:
        for target in targets:
            if target.num_periods > _NUM_PERIODS_LIMIT:
                print(f"{target} may be too large to graph!")

        eq_label = f"{func.__name__}(x" + ", {}" * len(popt) + ")"
        if hasattr(func, "metadata") and isinstance(func.metadata, dict):
            eq_label = func.metadata.get("equation_template", eq_label)

        curve_x = _numpy.arange(1, _NUM_PERIODS_LIMIT + 1)
        curve_y = func(curve_x, *popt)

        _plt.plot(curve_x, curve_y, "k-", label=eq_label.format(*popt))
        _plt.plot(train_x, train_y, "ko", label="Training Data")

        _plt.plot(target_length_periods, target_number_periods, "ro", label="Estimate(s)")
        for target, x, y in zip(targets, target_length_periods, target_number_periods):
            _plt.annotate(
                f"{target}\n({x}, ≈{y:e})", xy=(x, y), xycoords='data',
                horizontalalignment='right', verticalalignment='bottom')

        _plt.xlabel("# of Periods in Target Number Name Length")
        _plt.ylabel("# of Periods in Target Number")
        _plt.xscale("log")
        _plt.yscale("log")
        _plt.legend()
        _plt.show()


parser = _argparse.ArgumentParser(
    prog=_Path(__file__).stem,
    formatter_class=_argparse.RawTextHelpFormatter,
    description="estimate letter-efficient numbers")
parser.set_defaults(func=_infer)
parser.add_argument(
    'targets',
    nargs="+",
    type=PNumber,
    help="Target number length(s)")
parser.add_argument(
    "-g", "--graph",
    action="store_true",
    dest="graph_result",
    help="graph the resulting prediction(s)")
parser.add_argument(
    "-w", "--whole",
    action="store_true",
    dest="use_integer_math",
    help="use equation with only whole numbers: F(x, a) = T(x) / a\n"
         "instead of default power equation: F(x, a, b) = a * T(x) ** b")
parser.add_argument(
    "-q", "--quick",
    action="store_true",
    dest="approximate_targets",
    help="approximate targets by largest period: T(x) = 373 * 1000 ** x\n"
         "instead of using entire target value: T(x) = int(x)")
parser.add_argument(
    "-f", "--function",
    type=lambda f: globals()[f],
    help=_argparse.SUPPRESS)


if __name__ == '__main__':
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs)  # noqa
