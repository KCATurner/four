"""
Main CLI entry point.
"""

# external
import argparse as _argparse

# internal
from four import chain, graph, infer


__all__ = [
    "parser"]


parser = _argparse.ArgumentParser(
    prog="four",
    formatter_class=_argparse.RawTextHelpFormatter,
    description="generate 4-chains")
commands = parser.add_subparsers(metavar='SUBCOMMAND')
for module in (chain, graph, infer):
    commands.add_parser(
        module.parser.prog,
        parents=[module.parser],
        formatter_class=_argparse.RawTextHelpFormatter,
        help=module.parser.description,
        add_help=False)


def _four():
    """
    Main entry point for four CLI.
    """
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs) # noqa


if __name__ == '__main__':
    _four()
