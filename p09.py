from copy import copy
from itertools import batched, product
from collections import defaultdict

import numpy as np


def p09a(data):
    areas = np.prod(np.abs(data - data[:, np.newaxis]) + 1, axis=-1)
    return areas.max()


def _classify_endpoints(points):
    state = "invalid"
    newpoints = []
    for ip, p in enumerate(points):
        if state == "valid":
            if p[1] == 'b':
                continue
            elif p[1] == 'x':
                state = "invalid"
                newpoints.append(p[0])
            else:  # p[1] == 'e'
                if (len(points) - ip) % 2:
                    state = "invalid"
                    newpoints.append(p[0])
        else: # state == "invalid"
            if p[1] == 'b':
                state = "valid"
                newpoints.append(p[0])
            elif p[1] == 'x':
                state = "valid"
                newpoints.append(p[0])
            else:  # p[1] == 'e'
                raise ValueError("What!")

    return newpoints


def p09b(data):
    # Go from point to point, storing "endpoints" of red/green regions
    # on individual rows
    endpoints = defaultdict(list)
    j0, i0 = data[0]
    for j1, i1 in np.roll(data, -1, axis=0):
        if j1 == j0:
            # Moving sideways
            endpoints[j0].extend([(min(i0, i1), 'b'), (max(i0, i1), 'e')])
        else:
            # Moving up/down
            for j in range(min(j0, j1) + 1, max(j0, j1)):
                endpoints[j].append((i0, 'x'))
        j0, i0 = j1, i1

    # Sort the endpoints, then remove end/begin pairs directly next to
    # each other, then mark them as alternating begin/end to make a
    # list of valid, non-abutting segments in each row
    segments = defaultdict(list)
    for k, v in endpoints.items():
        vorig = sorted(v)
        v = _classify_endpoints(sorted(v))
        todrop = []
        for end, begin in batched(v[1:-1], 2, strict=True):
            if end + 1 == begin:
                todrop.extend((end, begin))
        for x in todrop:
            v.remove(x)
        for begin, end in batched(v, 2, strict=True):
            segments[k].append((begin, end))

    # Now we can start evaluating pairs
    areas = sum([[((abs(i1 - i0) + 1) * (abs(j1 - j0) + 1), (j0, i0), (j1, i1))
                  for j1, i1 in data[idx0 + 1:]]
                 for idx0, (j0, i0) in enumerate(data[:-1])], start=[])
    areas.sort(reverse=True)
    for area, (j0, i0), (j1, i1) in areas:
        # Check if this rectangle is contained within the valid area
        contained = True
        for j in range(min(j0, j1), max(j0, j1) + 1):
            in_segment = False
            for seg in segments[j]:
                if seg[0] <= i0 <= seg[1] and seg[0] <= i1 <= seg[1]:
                    in_segment = True
            if not in_segment:
                contained = False
                break
        if contained:
            return area

    return -1


if __name__ == "__main__":
    data = np.loadtxt("data/p09.txt", delimiter=",", dtype=int)

    print(f"Part 1: {p09a(data)}")
    print(f"Part 2: {p09b(data)}")
