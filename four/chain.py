"""
print four-chains of target lengths
"""
import pathlib
import argparse

import four._fp_method
import four._oo_method


parser = argparse.ArgumentParser(
    prog=pathlib.Path(__file__).stem,
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__.replace("\n", " "))
parser.set_defaults(
    func=four._fp_method.main)
parser.add_argument(
    '-q', '--quiet',
    action='store_true',
    help='only print numbers in chain')
parser.add_argument(
    '-s', '--start',
    type=str,
    default='4',
    help='number from which to start;'
         '\ndefault: %(default)s')
parser.add_argument(
    '-l', '--length',
    type=int,
    default=2,
    help='length of the target chain;'
         '\ndefault: %(default)s')
methods = parser.add_mutually_exclusive_group(
    required=False)
methods.add_argument(
    '--oo',
    action='store_const',
    dest='func',
    const=four._oo_method.main,
    help=argparse.SUPPRESS)
methods.add_argument(
    '--fp',
    action='store_const',
    dest='func',
    const=four._fp_method.main,
    help=argparse.SUPPRESS)


if __name__ == '__main__':
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs)  # noqa
