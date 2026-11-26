"""Exact orbit calculation for fractional_53.md, using the standard library."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import factorial, gcd

from check_column_projections import DUPLICATE_LABELS, SEEDS


ROWS = tuple(combinations(range(5), 2))
COLUMNS = tuple(combinations(range(7), 2))
SLOTS = tuple(product(ROWS, (0, 1), COLUMNS))
SLOT_INDEX = {slot: i for i, slot in enumerate(SLOTS)}
RELATIONS = tuple(product(range(3), (0, 1), range(3)))
A = (7, 11, 12, 17, 17, 22, 26)
B = (5, 9, 10, 17, 19, 22, 28)


def relation(u, v):
    return (len(set(u[0]).intersection(v[0])), int(u[1] == v[1]),
            len(set(u[2]).intersection(v[2])))


def occupied(layer):
    return [s for s in SLOTS if all((layer[j] >> i) & 1 == s[1]
                                     for j, i in product(s[2], s[0]))]


def transform(layer, permutation, flip=0):
    return tuple(sum(((w >> i) & 1) << permutation[i] for i in range(5)) ^ flip
                 for w in layer)


def multisets(seed):
    return {tuple(sorted(transform(seed, p, flip)))
            for p in permutations(range(5)) for flip in (0, 31)}


def solve(matrix, column):
    """Rational Gaussian elimination with free coordinates set to zero."""
    table = [list(map(Fraction, row)) + [Fraction(z)] for row, z in zip(matrix, column)]
    size = len(column)
    pivots = []
    for j in range(size):
        row = len(pivots)
        k = next((i for i in range(row, size) if table[i][j]), None)
        if k is None:
            continue
        table[row], table[k] = table[k], table[row]
        divisor = table[row][j]
        table[row] = [z/divisor for z in table[row]]
        for i in range(size):
            if i != row and table[i][j]:
                factor = table[i][j]
                table[i] = [a-factor*b for a, b in zip(table[i], table[row])]
        pivots.append(j)
    assert all(not table[i][-1] for i in range(len(pivots), size))
    solution = [Fraction(0)] * size
    for i, j in enumerate(pivots):
        solution[j] = table[i][-1]
    return solution


def determinant(matrix):
    """Fraction-free Gaussian elimination for the displayed certificate minor."""
    matrix = [row[:] for row in matrix]
    sign, previous = 1, 1
    for j in range(len(matrix)-1):
        pivot = next((i for i in range(j, len(matrix)) if matrix[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            matrix[pivot], matrix[j] = matrix[j], matrix[pivot]
            sign = -sign
        value = matrix[j][j]
        for i in range(j+1, len(matrix)):
            for k in range(j+1, len(matrix)):
                numerator = matrix[i][k]*value - matrix[i][j]*matrix[j][k]
                matrix[i][k], remainder = divmod(numerator, previous)
                assert remainder == 0
        previous = value
    return sign*matrix[-1][-1]


def verify_lattice_minor():
    patterns = (17807, 47658, 47728, 133003, 139987, 144568, 193553, 221396,
                231978, 236584, 262751, 508426, 585989, 700584, 731298)
    coordinates = (1, 2, 3, 5, 6, 9, 10, 11, 12, 13, 15, 16, 17, 18)
    realizable = set()
    for seed in SEEDS:
        for layer in multisets(seed):
            labels = {2*ROWS.index(p)+c for p, c, e in occupied(layer)}
            realizable.add(sum(1 << i for i in labels))
    assert set(patterns) <= realizable
    matrix = [[((m >> i) & 1) - ((patterns[0] >> i) & 1) for m in patterns[1:]]
              for i in coordinates]
    assert determinant(matrix) == 2


def verify_lattice():
    templates = [transform(layer, tuple((i+t) % 5 for i in range(5)))
                 for layer in (A, B) for t in range(5)]
    base = 5*templates + [templates[i] for i in (0, 3, 6)]
    relabel = (0, 1, 4, 3, 2)
    labels = Counter(2*ROWS.index(p)+c for layer in base
                     for p, c, e in occupied(transform(layer, relabel)))
    assert all(labels[k] == 21 + (k in DUPLICATE_LABELS) for k in range(20))
    alternate = B[:5] + (B[6], B[5])
    old, new = set(occupied(B)), set(occupied(alternate))
    assert old-new == {((1, 4), 1, (4, 5))}
    assert new-old == {((1, 4), 1, (4, 6))}


def verify_fractional():
    orbits = [multisets(layer) for layer in SEEDS]
    assert len(set.union(*orbits)) == sum(map(len, orbits)) == 900
    assert all(len(occupied(layer)) == 8 for layer in SEEDS)
    parts = {k: [s for s in SLOTS if relation(SLOTS[0], s) == k] for k in RELATIONS}
    pair_counts = Counter()
    layer_count = 0
    for seed, orbit in zip(SEEDS, orbits):
        n = len(orbit)*factorial(7)
        for multiplicity in Counter(seed).values():
            n //= factorial(multiplicity)
        layer_count += n
        for u, v in product(occupied(seed), repeat=2):
            pair_counts[relation(u, v)] += n
    assert layer_count == 4384800
    gram = {}
    for k, part in parts.items():
        gram[k], remainder = divmod(pair_counts[k], 420*len(part))
        assert remainder == 0
    diag = gram[2, 1, 2]
    assert diag == 83520

    reduced = [[sum(gram[relation(parts[a][0], v)] for v in parts[b])
                for b in RELATIONS] for a in RELATIONS]
    n = len(RELATIONS)
    square = [[sum(reduced[i][k]*reduced[k][j] for k in range(n))
               for j in range(n)] for i in range(n)]
    coeff = solve(square, [gram[k] for k in RELATIONS])
    projected = [sum(z*y for z, y in zip(row, coeff)) for row in reduced]
    error = {k: z-int(k == (2, 1, 2)) for k, z in zip(RELATIONS, projected)}
    assert all(error[a, b, e] == error[a, b, 0] for a, b, e in RELATIONS)
    doubles = [(ROWS[i//2], i % 2) for i in DUPLICATE_LABELS]
    for p, c in product(ROWS, (0, 1)):
        assert sum(error[len(set(p).intersection(q)), int(c == d), 0]
                   for q, d in doubles) == 0

    # Express all corrections as integers over a common denominator before
    # checking the 900 column multisets and all choices of doubled positions.
    coeff = [diag*z for z in coeff]
    assert max(map(abs, coeff)) < 2
    denominator = 1
    for z in coeff:
        denominator *= z.denominator // gcd(denominator, z.denominator)
    numerators = {k: int(z*denominator) for k, z in zip(RELATIONS, coeff)}
    kernel = [[numerators[relation(u, v)] for v in SLOTS] for u in SLOTS]
    lowest = denominator
    for orbit in orbits:
        for layer in orbit:
            indices = [SLOT_INDEX[s] for s in occupied(layer)]
            weight = denominator
            for p, c in doubles:
                weight += min(sum(kernel[i][SLOT_INDEX[p, c, e]] for i in indices)
                              for e in COLUMNS)
            lowest = min(lowest, weight)
    assert 4*lowest > denominator
    return Fraction(lowest, denominator)


if __name__ == "__main__":
    verify_lattice()
    verify_lattice_minor()
    ratio = verify_fractional()
    print("Verified all 21^4 placements over the rationals and in the affine integer lattice.")
    print("Least fractional weight relative to the uniform value is", ratio)
