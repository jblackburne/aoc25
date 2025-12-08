import numpy as np


def p08a(data):
    # Identify the 1000 nearest pairs
    dists = np.linalg.norm(data - data[:, np.newaxis], axis=-1)
    dists[np.triu_indices_from(dists)] = np.inf
    nearest = np.unravel_index(np.argsort(dists.flat)[:1000], dists.shape)

    # Connect them up into circuits
    circuits = []
    for i, j in zip(*nearest):
        icirc = None
        jcirc = None
        for circ_idx in range(len(circuits)):
            if i in circuits[circ_idx]:
                icirc = circ_idx
            if j in circuits[circ_idx]:
                jcirc = circ_idx
        if icirc is None and jcirc is None:
            circuits.append(set([i, j]))
        elif icirc is None:
            circuits[jcirc].add(i)
        elif jcirc is None:
            circuits[icirc].add(j)
        elif icirc == jcirc:
            continue
        else:
            oldi = circuits.pop(max(icirc, jcirc))
            oldj = circuits.pop(min(icirc, jcirc))
            circuits.append(oldi.union(oldj))

    # Find the circuit sizes and return the product of the sizes of the largest three
    circ_sizes = sorted([len(circ) for circ in circuits], reverse=True)
    return circ_sizes[0] * circ_sizes[1] * circ_sizes[2]


def p08b(data):
    # Sort all pairs nearest to farthest
    num_boxes = len(data)
    num_pairs = num_boxes * (num_boxes - 1) // 2
    dists = np.linalg.norm(data - data[:, np.newaxis], axis=-1)
    dists[np.triu_indices_from(dists)] = np.inf
    nearest = np.unravel_index(np.argsort(dists.flat)[:num_pairs], dists.shape)

    # Connect them up into circuits
    circuits = []
    for i, j in zip(*nearest):
        icirc = None
        jcirc = None
        for circ_idx in range(len(circuits)):
            if i in circuits[circ_idx]:
                icirc = circ_idx
            if j in circuits[circ_idx]:
                jcirc = circ_idx
        if icirc is None and jcirc is None:
            circuits.append(set([i, j]))
        elif icirc is None:
            circuits[jcirc].add(i)
        elif jcirc is None:
            circuits[icirc].add(j)
        elif icirc == jcirc:
            continue
        else:
            oldi = circuits.pop(max(icirc, jcirc))
            oldj = circuits.pop(min(icirc, jcirc))
            circuits.append(oldi.union(oldj))
        if len(circuits) == 1 and len(circuits[0]) == num_boxes:
            return data[i, 0] * data[j, 0]


if __name__ == "__main__":
    data = np.loadtxt("data/p08.txt", delimiter=",", dtype=int)

    print(f"Part 1: {p08a(data)}")
    print(f"Part 2: {p08b(data)}")
