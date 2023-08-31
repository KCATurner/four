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
from tqdm import tqdm as _tqdm
from time import sleep as _sleep
from pathlib import Path as _Path
from itertools import cycle as _cycle
from threading import Thread as _Thread

# internal
from four import _oo_api, _fp_api
from four._core import status as _status


__all__ = [
    "parser",
    "iter_chain"]


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


def C(length: int = 1, chain_index: int = 1): # noqa
    """"""
    this_rank = [[_oo_api.PNumber(4)]]
    while any(len(c) < length for c in this_rank):
        next_rank = []
        for this_chain in this_rank:
            count = 0
            child = _oo_api._first(this_chain[-1])
            while child is not None and count < chain_index:
                index = 0
                for next_chain in next_rank:
                    if child < next_chain[-1]:
                        break
                    index += 1
                next_rank.insert(index, [*this_chain, child])
                child = _oo_api._next(child)
                count += 1
        if len(next_rank) == 0:
            for this_chain in this_rank:
                child = _oo_api._next(this_chain[-1])
                next_rank.append([*this_chain[:-1], child])
        this_rank = next_rank[:chain_index]

    if len(this_rank) < chain_index:
        raise IndexError(f"C[{length}][{chain_index}] does not exist!")

    return this_rank[chain_index - 1]

    # def iter_first(root, length):
    #     chain = [_oo_api.PNumber(root), ]
    #     yield chain[-1]
    #     while len(chain) < length:
    #         child = _oo_api._first(chain[-1])
    #         while child is None or child == chain[-1]:
    #             chain[-1] = _oo_api._next(chain[-1])
    #             child = _oo_api._first(chain[-1])
    #         chain.append(child)
    #         yield chain[-1]
    #
    # first_chain = list(iter_first(4, length))
    # chains = [first_chain, ]
    # while len(chains) < chain_index:
    #     chain = chains[-1][:-1]
    #     chain.append(_oo_api._next(chains[-1][-1]))
    #
    # for node in first_chain[::-1]:
    #     chains.append(first_chain)


    # chains = [[_oo_api.PNumber(4), ], ]
    # for rank in range(chain_index):
    #     # update existing chains
    #     for index in range(len(chains)):
    #         child = _oo_api._first(chains[index][-1])
    #         while child is None or child == chains[index][-1]:
    #             chains[index][-1] = _oo_api._next(chains[index][-1])
    #             child = _oo_api._first(chains[index][-1])
    #         chains[index].append(child)
    #     # add/replace chains
    #     while len(chains) < chain_index:
    #         chain = chains[-1][:-1]
    #         sibling = _oo_api._next(chains[-1][-1])
    #         if sibling is None:
    #
    #         chain.append()





    # chains = [first_chain, ]
    # for node in first_chain[::-1]:
    #     while len(chains) < chain_index:
    #         sibling = _oo_api._next(chains[-1][-1])
    #         if sibling is not None:
    #             chains.append(chains[-1])
    #             chains[-1][-1] = sibling




def iter_chain(
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
        >>> list(iter_chain(3, "21"))
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


def _chain(
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

    # result = dict.fromkeys(range(1, 32))
    # from conwech.lexicon import ZILLION_PERIOD_PREFIXES
    # for index, prefix in enumerate(ZILLION_PERIOD_PREFIXES):
    #     result[len(prefix)] = (index, prefix)
    #
    # for length, (index, prefix) in result.items():
    #     print(f"{length:>3}: ({index}, '{prefix}')")

    if hasattr(module, "_cli_verbosity"):
        module._cli_verbosity = int(verbosity)

    x = _oo_api._last(target=root)
    print(x)
    exit()

    # show we're thinking...
    spinner = _Spinner()
    if verbosity < 2:
        spinner.start()

    try:
        chain = iter_chain(length, root, module)
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


def __get_number_of_children(node: str):
    ...


def __get_next_child(node: str, start: str) -> Union[str, None]:
    node = _fp_api.parse_abbreviation(node)
    # target =


def __iter_children(node: str, limit: int) -> Generator[str, None, None]:
    child = __get_next_child(node, start="0")
    yield child
    count = 1
    while count > limit:
        child = __get_next_child(node, start=child)
        yield child
        count += 1


def __c(length: int, chain_index: int, module: ModuleType, verbosity: int = 0):

    C()


    number = _fp_api.parse_abbreviation("4")
    yield _fp_api.write_abbreviation(number)

    count = 1
    while count < length:
        number = api._first(number)  # noqa
        yield _fp_api.write_abbreviation(number)
        count += 1


    if len(chain) < 1:
        raise ValueError()

    if length == len(chain):
        return chain[element_index]

    if length > len(chain):
        generator = __iter_children(node=chain[-1], limit=chain_index)
        child = next(generator)
        if child is None:
            ...






parser = _argparse.ArgumentParser(
    prog=_Path(__file__).stem,
    formatter_class=_argparse.RawTextHelpFormatter,
    description="print four-chains of target lengths")
parser.set_defaults(
    func=C,
    module=_fp_api)
parser.add_argument(
    "-v", "--verbose",
    action="count",
    default=0,
    dest="verbosity",
    help="increase output verbosity")
# parser.add_argument(
#     "-r", "--root",
#     type=str,
#     default="4",
#     help="number from which to start;"
#          "\ndefault: %(default)s")
parser.add_argument(
    "-l", "--length",
    type=int,
    default=1,
    help="length of the target chain;"
         "\ndefault: %(default)s")
parser.add_argument(
    "-c", "--chain",
    type=lambda s: int(s) - 1,
    default=2,
    dest="chain_index",
    help="")
methods = parser.add_mutually_exclusive_group(
    required=False)
methods.add_argument(
    "--oo",
    action="store_const",
    dest="module",
    const=_oo_api,
    help=_argparse.SUPPRESS)
methods.add_argument(
    "--fp",
    action="store_const",
    dest="module",
    const=_fp_api,
    help=_argparse.SUPPRESS)


if __name__ == "__main__":
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop("func", parser.print_help)(**inputs)  # noqa
