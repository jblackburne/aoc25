from functools import cache
from math import prod


def ingest_p11(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    graph = {}
    for line in lines:
        node, deststr = line.split(":")
        dests = tuple(deststr.split())
        graph[node] = dests

    return graph


@cache
def _num_paths_recursive(src, dest):
    if src == dest:
        return 1
    else:
        return sum(_num_paths_recursive(fwd, dest) for fwd in graph[src])



def p11a(graph):
    return _num_paths_recursive("you", "out")


def p11b(graph):
    "This solution benefited from looking at a picture of the graph"
    segments = (
        _num_paths_recursive("svr", "fft"),
        _num_paths_recursive("fft", "dac"),
        _num_paths_recursive("dac", "out"),
        )

    return prod(segments)


if __name__ == "__main__":
    graph = ingest_p11("data/p11.txt")
    graph["out"] = ()

    print(f"Part 1: {p11a(graph)}")
    print(f"Part 2: {p11b(graph)}")
