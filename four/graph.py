"""
todo
"""
import re
import typing
import pathlib
import graphviz
import argparse
import conwech


def count_letters(number) -> int:
    """
    Count the number of letters in the name of number.
    """
    name = conwech.number2text(number)
    pattern = re.compile(r'[a-zA-z]+')
    return sum(len(m.group()) for m in pattern.finditer(name))


def get_four_chain(number) -> typing.List[int]:
    """
    Get a list of numbers in the four-chain starting from number.
    """
    result = [number, ]
    while result[-1] != 4:
        result.append(count_letters(result[-1]))
    return result


def proceed_anyway(prompt) -> bool:
    """
    Let user decide to proceed after prompt.
    """
    return bool(
        input(f'{prompt}\nProceed anyway? (y/n) [n]: ').lower()
        in ['y', 'yes'])


def main(output, length, max_start, show_all=False, skip_warnings=False):
    """
    todo
    """
    dot = graphviz.Graph(
        format=output.suffix.lstrip('.'),
        engine='dot',  # dot/neato/twopi/circo
        graph_attr={
            'concentrate': 'true',
            'overlap': 'false',
            'splines': 'true',
            'minlen': '2',
            'rankdir': 'BT',
            'mode': 'hier',
        },
        node_attr={
            'shape': 'circle',
        },
        edge_attr={
            'arrowhead': 'normal',
        },
        strict=False
    )

    if length > 8 and not skip_warnings:
        if not proceed_anyway('Exceedingly large target chain zillion!'):
            print('Aborting...')
            exit()

    if max_start > 100 and show_all and not skip_warnings:
        if not proceed_anyway('Max value may result in large image!'):
            print('Aborting...')
            exit()

    if show_all:
        for i in range(max_start + 1):
            dot.edge(str(i), str(count_letters(i)))
    else:
        dot.edge('4', '4')
        for i in range(1, length + 1):
            for j in range(max_start + 1):
                c = get_four_chain(j)
                if len(c) == i:
                    for h, t in zip(c[:-1], c[1:]):
                        dot.edge(str(h), str(t))
                    break

    dot.render(output.parent / output.stem)


parser = argparse.ArgumentParser(
        prog=pathlib.Path(__file__).stem,
        description='') # todo
parser.set_defaults(func=main)
parser.add_argument(
    'output',
    type=pathlib.Path, # noqa
    help='name of the output file')
parser.add_argument(
    '-l', '--length',
    type=int,
    default=8,
    help='graph chains up to this length; default: %(default)s')
parser.add_argument(
    '-m', '--max',
    dest='max_start',
    type=int,
    default=100,
    help='maximum start of chain; default: %(default)s')
parser.add_argument(
    '-a', '--all',
    dest='show_all',
    action='store_true',
    help='show all chains under max; default: %(default)s')
parser.add_argument(
    '-y', '--yes',
    dest='skip_warnings',
    action='store_true',
    help='skip warnings with y/yes; default: %(default)s')


if __name__ == '__main__':
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs)  # noqa
