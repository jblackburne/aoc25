import numpy as np


def ingest_p12(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    shapes = []
    n_shapes = 6
    for ishape in range(n_shapes):
        shapestrs = tuple(lines[5 * ishape + 1:5 * ishape + 4])
        shapes.append(np.array([[c == "#" for c in line] for line in shapestrs], dtype=int))
    shapes = np.array(shapes)

    areastrs = [line.split(":") for line in lines[30:]]
    dims = [tuple([int(x) for x in a[0].split("x")]) for a in areastrs]
    nums = [tuple([int(x) for x in a[1].strip().split()]) for a in areastrs]

    return shapes, dims, nums


def p12a(shapes, dims, nums):
    # How many can fit without any packing?
    nfit_unpacked = np.array([(d[0] // 3) * (d[1] // 3) for d in dims])
    num_tiles = np.array([sum(n) for n in nums])
    ncases_easyfit = np.sum(nfit_unpacked >= num_tiles)

    # How many cases will never fit, even with perfect packing?
    nsq = np.sum(shapes, axis=(1, 2))
    nsquares_fullpack = [int(sum([nsh * n for nsh, n in zip(nshape, nsq)])) for nshape in nums]
    ncases_neverfit = sum(nsquares_fullpack > np.array([np.prod(d) for d in dims]))

    # How many remain?
    ncases_hard = len(nums) - (ncases_easyfit + ncases_neverfit)
    if ncases_hard > 0:
        print(f"Hm, gotta write a tricky algorithm for {ncases_hard} cases")

    return ncases_easyfit


if __name__ == "__main__":
    shapes, dims, nums = ingest_p12("data/p12.txt")

    print(f"Part 1: {p12a(shapes, dims, nums)}")
    print(f"Part 2: Merry Christmas!")
