"""
Generate 4-chain tree graphs of various sizes given varying root nodes.

CLI Subcommand
==============

.. autoprogram:: four.graph:parser
   :prog: four graph
"""

# annotations
from typing import Optional

# external
import graphviz as _graphviz
import argparse as _argparse
from pathlib import Path as _Path

# internal
from four._oo_api import PNumber, PNumberLike


__all__ = [
    "parser"]


_LIMIT_WARNING_THRESHOLD: int = 100


def _graph(
        output: Optional[_Path] = None,
        root: PNumberLike = 4,
        limit: PNumberLike = 50,
        engine: str = "dot",
        skip_warnings: bool = False,
        directional: bool = False
) -> None:
    """
    Entry point for graph subcommand.

    Args:
        output: Save graph image to an output file; default = None.
        root: The root node of the graph; default = 4.
        limit: The maximum number to include in the tree; default = 50.
        engine: The layout of the graph nodes; default = 'dot'.
        skip_warnings: Skip warnings with y/yes; default = False.
        directional: Make graph edges directional; default = False.
    """
    graph = (_graphviz.Digraph if directional else _graphviz.Graph)(
        format="png",
        engine=engine,
        graph_attr={
            "concentrate": "true",
            "overlap": "false",
            "splines": "true",
            "minlen": "2",
            "rankdir": "BT",
            "mode": "hier"},
        node_attr={
            "shape": "circle"},
        edge_attr={
            "arrowhead": "normal",
            "arrowsize": "0.75"},
        strict=False)

    limit = PNumber(limit)
    if limit > _LIMIT_WARNING_THRESHOLD and not skip_warnings:
        if not input(
                "Max value may result in large image!"
                "\nProceed anyway? (y/n) [n]: ").lower() in ["y", "yes"]:
            print("Aborting...")
            exit()

    graph.node(name=str(root), label=f"<<B>{root}</B>>")
    for n in (PNumber(i) for i in range(int(limit) + 1)):
        graph.edge(str(n) or "0", str(n.name_length))

    if output is not None:
        graph.format = output.suffix.lstrip(".")
        graph.render(output.parent / output.stem, view=True)
    else:
        graph.view()


parser = _argparse.ArgumentParser(
    prog=_Path(__file__).stem,
    formatter_class=_argparse.RawTextHelpFormatter,
    description="generate graphs of four-chain trees")
parser.set_defaults(func=_graph)
parser.add_argument(
    "-y", "--yes",
    dest="skip_warnings",
    action="store_true",
    help="skip warnings with y/yes")
parser.add_argument(
    "-d", "--directional",
    action="store_true",
    help="make graph edges directional")
parser.add_argument(
    "-o", "--output",
    type=_Path,
    help="save image to output file")
parser.add_argument(
    "-r", "--root",
    type=int,
    default=4,
    help="set the root node of the graph;"
         "\ndefault: %(default)s")
parser.add_argument(
    "-l", "--limit",
    type=int,
    default=50,
    help="maximum number to include in the tree;"
         "\ndefault: %(default)s")
parser.add_argument(
    "-e", "--engine",
    type=str,
    default="dot",
    choices=sorted(_graphviz.ENGINES),
    metavar="ENGINE",
    help=f"change the layout of the graph nodes;"
         f"\nchoices: {', '.join(sorted(_graphviz.ENGINES))}"
         f"\ndefault: %(default)s")


if __name__ == "__main__":
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop("func", parser.print_help)(**inputs)  # noqa
