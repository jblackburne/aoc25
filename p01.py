def ingest_p01(fname):
    with open(fname, "r") as f:
        data = [(line[0], int(line[1:])) for line in f.readlines()]
    return data


def p01a(data):
    pos = 50
    num_zero = 0
    for lr, dist in data:
        sgn = 1 if lr == "R" else -1
        pos = (pos + sgn * dist + 100) % 100
        if pos == 0:
            num_zero += 1

    return num_zero


def p01b(data):
    pos = 50
    num_zero = 0
    for lr, dist in data:
        sgn = 1 if lr == "R" else -1
        for i in range(1, dist + 1):
            pos = (pos + sgn + 100) % 100
            if pos == 0:
                num_zero += 1

    return num_zero


if __name__ == "__main__":
    data = ingest_p01("data/p01.txt")

    print(f"Part 1: {p01a(data)}")
    print(f"Part 2: {p01b(data)}")
