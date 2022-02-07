"""
generate graphs of four-chain trees
"""

import typing
import pathlib
import graphviz
import argparse

from four._oo_method import PeriodList


def get_four_chain(number) -> typing.List[int]:
    """
    Get a list of numbers in the four-chain ending with number.
    """
    number = PeriodList(number)
    result = [number, ]
    while result[-1] != PeriodList(4):
        result.append(result[-1].name_length)
    return result


def proceed_anyway(prompt) -> bool:
    """
    Let user decide to proceed after prompt.
    """
    return bool(
        input(f'{prompt}\nProceed anyway? (y/n) [n]: ').lower()
        in ['y', 'yes'])


def main(output=None, root=4, limit=50, engine='dot',
         skip_warnings=False, directional=False):
    """
    Entry point for graph subcommand.
    """
    graph = (graphviz.Digraph if directional else graphviz.Graph)(
        format='png',
        engine=engine,
        graph_attr={
            'concentrate': 'true',
            'overlap': 'false',
            'splines': 'true',
            'minlen': '2',
            'rankdir': 'BT',
            'mode': 'hier'},
        node_attr={
            'shape': 'circle'},
        edge_attr={
            'arrowhead': 'normal',
            'arrowsize': '0.75'},
        strict=False)

    limit = PeriodList(limit)
    if limit > 100 and not skip_warnings:
        if not proceed_anyway('Max value may result in large image!'):
            print('Aborting...')
            exit()

    graph.node(name=str(root), label=f'<<B>{root}</B>>')
    for n in (PeriodList(i) for i in range(int(limit) + 1)):
        if PeriodList(root) in get_four_chain(n)[1:]:
            graph.edge(str(n) or '0', str(n.name_length))

    if output is not None:
        graph.format = output.suffix.lstrip('.')
        graph.render(output.parent / output.stem, view=True)
    else:
        graph.view()


parser = argparse.ArgumentParser(
    prog=pathlib.Path(__file__).stem,
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__.replace("\n", " "))
parser.set_defaults(func=main)
parser.add_argument(
    '-y', '--yes',
    dest='skip_warnings',
    action='store_true',
    help='skip warnings with y/yes')
parser.add_argument(
    '-d', '--directional',
    action='store_true',
    help='make graph edges directional')
parser.add_argument(
    '-o', '--output',
    type=pathlib.Path, # noqa
    help='save image to output file')
parser.add_argument(
    '-r', '--root',
    type=int,
    default=4,
    help='set the root node of the graph;'
         '\ndefault: %(default)s')
parser.add_argument(
    '-l', '--limit',
    type=int,
    default=50,
    help='maximum number to include in the tree;'
         '\ndefault: %(default)s')
parser.add_argument(
    '-e', '--engine',
    type=str,
    default='dot',
    choices=sorted(graphviz.ENGINES),
    metavar='ENGINE',
    help='change the layout of the graph nodes;'
         '\nchoices: %(choices)s'
         '\ndefault: %(default)s')


if __name__ == '__main__':
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs)  # noqa
