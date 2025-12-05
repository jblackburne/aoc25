from copy import copy


def ingest_p05(fname):
    with open(fname, "r") as f:
        read_ranges = True
        ranges = []
        ingredients = []
        for line in f:
            line = line.strip()
            if len(line) == 0:
                read_ranges = False
                continue
            if read_ranges:
                ranges.append(tuple(int(x) for x in line.split("-")))
            else:
                ingredients.append(int(line))

    return ranges, ingredients


def p05a(ranges, ingredients):
    num_fresh = 0
    for ing in ingredients:
        for lo, hi in ranges:
            if lo <= ing <= hi:
                num_fresh += 1
                break

    return num_fresh


def p05b(ranges):
    ranges = copy(ranges)
    dedup = []
    while len(ranges) > 0:
        rlo, rhi = ranges.pop()
        disqualified = False
        for dlo, dhi in dedup:
            if rlo <= dlo and rhi >= dhi:
                ranges.append((rlo, dlo - 1))
                ranges.append((dhi + 1, rhi))
                disqualified = True
                break
            if dlo <= rlo <= dhi:
                rlo = dhi + 1
            if dlo <= rhi <= dhi:
                rhi = dlo - 1
            if rhi < rlo:
                disqualified = True
                break
        if not disqualified:
            dedup.append((rlo, rhi))

    return sum(dhi - dlo + 1 for dlo, dhi in dedup)


if __name__ == "__main__":
    ranges, ingredients = ingest_p05("data/p05.txt")

    print(f"Part 1: {p05a(ranges, ingredients)}")
    print(f"Part 2: {p05b(ranges)}")
