from itertools import combinations

import numpy as np
#from scipy.optimize import linprog
from scipy.optimize import milp, LinearConstraint


def ingest_p10(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    lights = []
    buttons = []
    joltage = []
    for line in lines:
        light = (line[1:].split("]")[0])
        lights.append(tuple([int(c == "#") for c in light]))
        bs = [x.split(")")[0] for x in line.split("(")[1:]]
        bs = [tuple([int(x) for x in b.split(",")]) for b in bs]
        buttons.append(tuple(bs))
        jolt = line[:-1].split("{")[1]
        joltage.append(tuple([int(j) for j in jolt.split(",")]))

    return lights, buttons, joltage


def _find_weights(button_mat, lights):
    n_lights, n_buttons = button_mat.shape
    # Note that we will never need to press a given button more than once
    for n in range(1, n_buttons + 1):
        for widx in combinations(range(n_buttons), n):
            w = np.zeros(n_buttons, dtype=int)
            w[list(widx)] = 1
            if np.all((np.dot(button_mat, w) % 2) == lights):
                return w


def p10a(lights, buttons):
    n_presses = 0
    for mlights, mbuttons in zip(lights, buttons):
        # Are we already there?
        if not any(mlights):
            continue

        # Build the button matrix B such that B w = l, where
        # w is the number of presses for each button, and l is the desired lights
        n_buttons = len(mbuttons)
        n_lights = len(mlights)
        button_mat = np.zeros((n_lights, n_buttons), dtype=int)
        for i, b in enumerate(mbuttons):
            button_mat[list(b), i] = 1

        # Check all combinations until we get one
        weights = _find_weights(button_mat, np.array(mlights))
        n_presses += np.sum(weights)

    return n_presses


def p10b(joltage, buttons):
    n_presses = 0
    for jolt, mbuttons in zip(joltage, buttons):
        # Are we already there?
        if not any(jolt):
            continue

        # Build the button matrix B such that B w = l, where
        # w is the number of presses for each button, and l is the desired lights
        n_buttons = len(mbuttons)
        n_jolt = len(jolt)
        button_mat = np.zeros((n_jolt, n_buttons), dtype=int)
        for i, b in enumerate(mbuttons):
            button_mat[list(b), i] = 1

        # Now we cheat and use scipy
        c = np.ones(n_buttons, dtype=int)
        constraints = LinearConstraint(button_mat, jolt, jolt)
        integrality = np.ones(n_buttons, dtype=int)
        soln = milp(c, constraints=constraints, integrality=integrality)
        if not soln.success:
            raise RuntimeError("What!")
        if not np.all(np.dot(button_mat, np.round(soln.x).astype(int)) == jolt):
            raise RuntimeError("You're mad!")
        print(soln.x.astype(int))
        n_presses += np.round(soln.x).astype(int).sum()

    return n_presses

if __name__ == "__main__":
    lights, buttons, joltage = ingest_p10("data/p10.txt")

    print(f"Part 1: {p10a(lights, buttons)}")
    print(f"Part 2: {p10b(joltage, buttons)}")

