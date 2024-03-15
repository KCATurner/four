"""
Calculate and print 4-chains of specified target lengths from various
root nodes.

CLI Subcommand
==============

.. autoprogram:: four.chain:parser
   :prog: four chain
"""

# annotations
from types import ModuleType
from typing import (
    Union, Literal, Sequence, Generator,
    get_args as _get_args)

# external
import argparse as _argparse
from time import sleep as _sleep
from pathlib import Path as _Path
from itertools import cycle as _cycle
from threading import Thread as _Thread

# internal
from four import _oo_api, _fp_api
from four._core import status as _status


__all__ = [
    "parser",
    "iter_first_chain"]


API = Union[Literal["fp", "oo"], ModuleType]


class _Spinner:

    def __init__(self, cycle: Union[str, Sequence[str]] = "|/-\\", delay: float = 0.1):
        """
        CLI Spinner so users know we aren't hanging...

        Args:
            cycle: set of strings/chars to cycle through.
            delay: Update frequency for spinner printing.
        """
        self.cycle = _cycle(cycle)
        self.delay = float(delay)
        self._busy = False

    def __enter__(self):
        # To support usage as context manager
        self.start()

    def __exit__(self, exception, value, traceback):
        # To support usage as context manager
        self.stop()
        if exception is not None:
            return False

    def _spin(self) -> None:
        """
        Target for threading.Thread.
        """
        while self._busy:
            string = next(self.cycle)
            print(string, end="\b" * len(string), flush=True)
            _sleep(self.delay)

    def start(self) -> None:
        """
        Start printing spinner to stdout in separate thread.
        """
        self._busy = True
        _Thread(target=self._spin).start()

    def stop(self) -> None:
        """
        Stop printing spinner to stdout in separate thread.
        """
        self._busy = False


def iter_first_chain(
        length: int,
        root: str,
        api: API = "fp"
) -> Generator[str, None, None]:
    """
    Generate the first 4-chain of the given length with the given root.

    Args:
        length: Length of the target chain.
        root: Number from which to start; root may be a well-formed
            period-list string containing period repetitions.
        api: The backend four API to use: "fp" (functional) or "oo"
            (object-oriented); api may also be a python module that
            defines a _first() function which returns the first number N
            with L letters in its name given L, where both L and N are
            positive integers in the form of a list of (P, R) tuples.

    Yields:
        str: Each number in the target 4-chain abreviated as a
        well-formmed period-list string.

    Raises:
        NotImplimentedError: When a python module given for api does
            not impliment a _first() function.

    Examples:
        >>> list(iter_first_chain(3, "21"))
        [[(21, 1)], [(123, 1)], [(001, 1), (113, 1), (373, 3)]]

    See Also:
        - :attr:`four._core.PERIOD_PATTERN`
    """
    api = dict(zip(_get_args(API), (_fp_api, _oo_api))).get(api, api)
    if not hasattr(api, "_first"):
        raise NotImplementedError(
            f"{api} module has no _first() function for defining a"
            f" 4-chain generator")

    number = _fp_api.parse_abbreviation(root)
    yield _fp_api.write_abbreviation(number)

    count = 1
    while count < length:
        number = api._first(number) # noqa
        yield _fp_api.write_abbreviation(number)
        count += 1


def _first_chain(
        module: ModuleType,
        length: int = 2,
        root: Union[int, str] = 4,
        verbosity: int = 0
) -> None:
    """
    Print the first 4-chain of the given length with the given root.

    Args:
        module: The module used to generate the 4-chain.
        length: Length of the target chain; default = 2.
        root: Number from which to start; default = 4.
        verbosity: Set level of output verbosity; default = 0.
    """
    if hasattr(module, "_cli_verbosity"):
        module._cli_verbosity = int(verbosity)

    # show we're thinking...
    spinner = _Spinner()
    if verbosity < 2:
        spinner.start()

    try:
        chain = iter_first_chain(length, root, module)
        if verbosity == 0:
            print(next(chain), end="")
            count = 1
            while count < length:
                print(" <- ", end="", flush=True)
                print(f"{next(chain)}", end="")
                count += 1
        else:
            previous = next(chain)
            for number in chain:
                _status(number, previous)
                previous = number

    except Exception as exception:
        # catch and re-raise any exception, so we can stop spinner
        raise exception

    finally:
        spinner.stop()


def _chain(length: int, chain_index: int, module: ModuleType, verbosity: int = 0):
    """"""
    if hasattr(module, "_cli_verbosity"):
        module._cli_verbosity = int(verbosity)

    # show we're thinking...
    spinner = _Spinner()
    spinner.start()

    try:
        if hasattr(module, "C"):
            chain = iter(module.C(length, chain_index))
            if verbosity == 0:
                print(next(chain), end="")
                count = 1
                while count < length:
                    print(" <- ", end="", flush=True)
                    print(f"{next(chain)}", end="")
                    count += 1
            else:
                previous = next(chain)
                for number in chain:
                    _status(number, previous)
                    previous = number
        else:
            print(f"Sequence C implementation missing from {module}")

    except Exception as exception:
        # catch and re-raise any exception, so we can stop spinner
        raise exception

    finally:
        spinner.stop()


parser = _argparse.ArgumentParser(
    prog=_Path(__file__).stem,
    formatter_class=_argparse.RawTextHelpFormatter,
    description="print four-chains of target lengths")
parser.set_defaults(
    func=_chain,
    module=_oo_api)
parser.add_argument(
    "-v", "--verbose",
    action="count",
    default=0,
    dest="verbosity",
    help="increase output verbosity")
parser.add_argument(
    "-l", "--length",
    type=int,
    default=1,
    help="length of the target chain;"
         "\ndefault: %(default)s")
parser.add_argument(
    "-c", "--chain",
    type=int,
    default=1,
    dest="chain_index",
    help="the target chain (by 1-based index)")


if __name__ == "__main__":
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop("func", parser.print_help)(**inputs)  # noqa
