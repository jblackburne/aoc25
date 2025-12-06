from math import prod


def ingest_p06(fname):
    with open(fname, "r") as f:
        lines = f.readlines()

    numbers = [[int(x) for x in line.strip().split()] for line in lines[:-1]]
    ops = lines[-1].strip().split()

    return lines, numbers, ops


def p06a(numbers, ops):
    operands = list(zip(*numbers))
    total = 0
    for nums, op in zip(operands, ops):
        total += (sum(nums) if op == "+" else
                  prod(nums) if op == "*" else 0)

    return total


def p06b(lines):
    # "Transpose" the string array
    data = ["".join(x).strip() for x in zip(*lines)]

    # Batch the numbers into problems
    problems = []
    this_prob = []
    for x in data:
        if x:
            this_prob.append(x)
        else:
            problems.append(tuple(this_prob))
            this_prob = []

    # Do the math
    total = 0
    for problem in problems:
        op = problem[0][-1]
        operands = (problem[0][:-1],) + tuple(problem[1:])
        nums = (int(x) for x in operands)
        total += (sum(nums) if op == "+" else
                  prod(nums) if op == "*" else 0)

    return total


if __name__ == "__main__":
    lines, numbers, ops = ingest_p06("data/p06.txt")

    print(f"Part 1: {p06a(numbers, ops)}")
    print(f"Part 2: {p06b(lines)}")
