"""
generate four-chains
"""
import argparse

from four import chain, graph


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__.replace('\n', ' '))
commands = parser.add_subparsers(metavar='SUBCOMMAND')
for module in (chain, graph):
    commands.add_parser(
        module.parser.prog,
        parents=[module.parser],
        formatter_class=argparse.RawTextHelpFormatter,
        help=module.parser.description,
        add_help=False)


def main():
    """ For internal use only! """
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs) # noqa


if __name__ == '__main__':
    main()
