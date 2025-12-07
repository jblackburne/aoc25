import numpy as np
from functools import cache


def ingest_p07(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    data = []
    for line in lines:
        spos = line.find("S")
        if spos != -1:
            startpos = spos
        data.append([c == "^" for c in line])

    return np.asarray(data), startpos


def p07a(data, startpos):
    ny, nx = data.shape
    beamidxs = set([startpos])
    num_split = 0
    for yidx in range(ny - 1):
        newbeamidxs = set()
        for xidx in beamidxs:
            if data[yidx + 1, xidx]:
                # Split
                newbeamidxs.update((xidx - 1, xidx + 1))
                num_split += 1
            else:
                # Just move down
                newbeamidxs.add(xidx)
        beamidxs = newbeamidxs

    return num_split


@cache
def p07b(pos):
    ny, nx = data.shape
    yidx, xidx = pos
    # Base case
    if pos[0] == ny - 1:
        return 1
    elif data[yidx + 1, xidx]:
        # Split
        return (p07b((yidx + 1, xidx - 1)) +
                p07b((yidx + 1, xidx + 1)))
    else:
        # Just move down
        return p07b((yidx + 1, xidx))


if __name__ == "__main__":
    data, startpos = ingest_p07("data/p07.txt")

    print(f"Part 1: {p07a(data, startpos)}")
    print(f"Part 2: {p07b((0, startpos))}")
