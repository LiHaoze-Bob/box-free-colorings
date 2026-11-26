"""Classify 5-by-7 binary layers with exactly eight monochromatic rectangles.

Every column in such a layer must have two or three ones, as follows from
counting same-colour pairs of rows. Seven columns contribute at least 28
pairs to 20 coloured row-pair types. Their repetitions create at least eight
rectangles, with any unbalanced column increasing this lower bound.

Run with Python 3.9+; no input file or external packages are required.
"""

from itertools import combinations_with_replacement, permutations
from math import comb


def classify():
    weights = [bin(i).count("1") for i in range(32)]
    columns = [v for v in range(32) if weights[v] in (2, 3)]
    # Two columns form one monochromatic rectangle for each pair of rows
    # whose entries in both columns are all zero or all one.
    score = [[comb(weights[x & y], 2) + comb(weights[31 ^ (x | y)], 2)
              for y in range(32)] for x in range(32)]
    minimal = set()
    for layer in combinations_with_replacement(columns, 7):
        rectangles = 0
        for j, col in enumerate(layer):
            rectangles += sum(score[col][other] for other in layer[:j])
            if rectangles > 8:
                break
        if rectangles == 8:
            minimal.add(layer)

    transforms = []
    for perm in permutations(range(5)):
        transforms.append([sum(((col >> old) & 1) << new
                               for new, old in enumerate(perm)) for col in range(32)])
    remaining = minimal.copy()
    orbit_sizes = []
    while remaining:
        layer = min(remaining)
        orbit = {tuple(sorted(transform[col] ^ flip for col in layer))
                 for transform in transforms for flip in (0, 31)}
        if not orbit <= remaining:
            raise RuntimeError("Symmetry orbit is inconsistent with enumeration")
        remaining -= orbit
        orbit_sizes.append(len(orbit))
    print("Minimal layers up to column permutations:", len(minimal))
    print("Classes up to row/column permutations and global colour swap:", len(orbit_sizes))
    print("Class sizes among column multisets:", sorted(orbit_sizes))


if __name__ == "__main__":
    classify()
