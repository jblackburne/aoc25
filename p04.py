import numpy as np


NPAD=2

def ingest_p04(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    ny = len(lines) + 2 * NPAD
    nx = len(lines[0]) + 2 * NPAD
    data = np.zeros((ny, nx), dtype=np.int32)
    data[NPAD:-NPAD, NPAD:-NPAD] = np.asarray([[c == "@" for c in line] for line in lines])

    return data


def _can_reach(data):
    num_neighbors = np.sum([data[NPAD + j:-NPAD + j, NPAD + i:-NPAD + i]
                            for j in range(-1, 2) for i in range(-1, 2)], axis=0)
    num_neighbors -= data[NPAD:-NPAD, NPAD:-NPAD]

    can_reach = np.zeros_like(data)
    can_reach[NPAD:-NPAD, NPAD:-NPAD] = np.logical_and(
        num_neighbors < 4, data[NPAD:-NPAD, NPAD:-NPAD] == 1)

    return can_reach.astype(np.int32)


def p04a(data):
    return np.sum(_can_reach(data))


def p04b(data):
    num_removed = 0
    while True:
        can_reach = _can_reach(data)
        num_removable = np.sum(can_reach)
        if num_removable == 0:
            break
        num_removed += num_removable
        data -= can_reach

    return num_removed


if __name__ == "__main__":
    data = ingest_p04("data/p04.txt")

    print(f"Part 1: {p04a(data)}")
    print(f"Part 2: {p04b(data)}")
