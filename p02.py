from copy import copy


def ingest_p02(fname):
    with open(fname, "r") as f:
        data = f.readline().split(",")

    data = [tuple(entry.strip().split("-")) for entry in data]

    return data


def p02a(data):
    data = copy(data)
    sum_invalid = 0
    while len(data) > 0:
        first, last = data.pop()
        num_digit = len(first)
        len_diff = len(last) - num_digit
        if len_diff > 0:
            data.append((str(10**num_digit), last))
            last = str(10**num_digit - 1)
        if num_digit % 2:
            continue
        topfirst = int(first[:num_digit // 2])
        toplast = int(last[:num_digit // 2])
        first = int(first)
        last = int(last)
        for top in range(topfirst, toplast + 1):
            top_str = str(top)
            toptop = int(f"{top_str}{top_str}")
            if first <= toptop <= last:
                sum_invalid += toptop

    return sum_invalid


def p02b(data):
    data = copy(data)
    invalid = set()
    while len(data) > 0:
        sfirst, slast = data.pop()
        num_digit = len(sfirst)
        len_diff = len(slast) - num_digit
        if len_diff > 0:
            data.append((str(10**num_digit), slast))
            slast = str(10**num_digit - 1)
        first = int(sfirst)
        last = int(slast)
        for pattern_len in range(1, num_digit // 2 + 1):
            if num_digit % pattern_len:
                continue
            for top in range(int(sfirst[:pattern_len]), int(slast[:pattern_len]) + 1):
                top_str = str(top)
                toptop = int(top_str * (num_digit // pattern_len))
                if first <= toptop <= last:
                    invalid.add(toptop)

    return sum(invalid)


if __name__ == "__main__":
    data = ingest_p02("data/p02.txt")

    print(f"Part 1: {p02a(data)}")
    print(f"Part 2: {p02b(data)}")
