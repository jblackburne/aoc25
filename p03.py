def p03b(data, ndigit = 12):
    total_jolt = 0
    for line in data:
        idx = 0
        high_digits = []
        for idigit in range(ndigit):
            # Get the highest digit in the line (excluding the last (ndigit - idigit - 1) chars)
            high_digit = 0
            high_idx = 0
            remaining = (line[idx:-(ndigit - idigit - 1)] if idigit + 1 < ndigit else
                         line[idx:])
            for i, c in enumerate(remaining, start=idx):
                digit = int(c)
                if digit > high_digit:
                    high_digit = digit
                    high_idx = i
            high_digits.append(str(high_digit))
            idx = high_idx + 1
        total_jolt += int("".join(high_digits))

    return total_jolt


if __name__ == "__main__":
    with open("data/p03.txt", "r") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Part 1: {p03b(data, ndigit=2)}")
    print(f"Part 2: {p03b(data)}")
