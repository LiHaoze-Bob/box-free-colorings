"""Reconstruct the nine cyclic seed orbits and check their 51-layer certificate.

Run from any directory with Python 3.9 or newer. Coordinates in the permutations
are zero-based. Each entry of a permutation is the destination of that index.
"""

from itertools import combinations
from pathlib import Path


ROW_PERMUTATION = (1, 2, 0, 4, 3)
COLUMN_PERMUTATION = (1, 2, 3, 4, 5, 0, 6)
SEEDS = (
    "0110110 1011010 0010011 1000101 0101001",
    "0010111 0101110 1011000 1100001 0111001",
    "0110110 1001010 0011100 0101001 1010101",
    "1010110 1000011 1001100 0110101 0101010",
    "1001100 1010011 0110101 0111010 0001011",
    "0010101 1001100 1100011 0011011 1111000",
    "0010011 0101110 1100011 1110100 1001001",
    "1010101 0110011 0111000 1001010 0100110",
    "1101010 0011100 0010011 1110001 1000110",
)


def step(layer):
    result = [[""] * 7 for _ in range(5)]
    for r, target_row in enumerate(ROW_PERMUTATION):
        for c, target_column in enumerate(COLUMN_PERMUTATION):
            result[target_row][target_column] = layer[r][c]
    return tuple("".join(row) for row in result)


def construct():
    layers = set()
    for seed, expected in zip(SEEDS, (3,) + (6,) * 8):
        first = tuple(seed.split())
        orbit = set()
        layer = first
        for _ in range(6):
            orbit.add(layer)
            layer = step(layer)
        if layer != first or len(orbit) != expected or orbit & layers:
            raise ValueError("The seed orbits have unexpected periods or overlap")
        layers.update(orbit)
    return sorted(layers)


def verify():
    layers = construct()
    certificate = Path(__file__).with_name("5x7x51_cyclic_certificate.txt")
    expected = [f"Layer {i}\n" + "\n".join(layer)
                for i, layer in enumerate(layers, 1)]
    if certificate.read_text().strip() != "\n\n".join(expected):
        raise ValueError("The expanded certificate differs from the seed orbits")

    occupied = set()
    for number, layer in enumerate(layers, 1):
        rectangles = 0
        for r, s in combinations(range(5), 2):
            for c, d in combinations(range(7), 2):
                color = layer[r][c]
                if color == layer[r][d] == layer[s][c] == layer[s][d]:
                    slot = (r, s, c, d, color)
                    if slot in occupied:
                        raise ValueError(f"Repeated colored rectangle in layer {number}: {slot}")
                    occupied.add(slot)
                    rectangles += 1
        if rectangles != 8:
            raise ValueError(f"Layer {number} has {rectangles} rectangles")
    print(f"{len(layers)} layers, {len(occupied)} occupied slots, zero monochromatic boxes")


if __name__ == "__main__":
    verify()
