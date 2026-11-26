"""Expand and verify the fifteen Klein four orbits giving N(5, 7) = 52."""

from collections import Counter
from itertools import combinations
from pathlib import Path


# Each triple gives the orbit length, the rectangle count per layer, and five rows.
SEEDS = (
    (2, 8, "0100101 0010011 1010110 0101110 1001001"),
    (2, 9, "0101101 1010011 1110100 0111010 0000110"),
    (2, 9, "1100001 0011001 0101010 1010100 0000111"),
    (2, 8, "1101100 1011010 1000101 0001011 0110001"),
    (4, 8, "1111000 0010110 1001011 1100101 0101110"),
    (4, 8, "1001010 1110000 0101101 0100110 0010011"),
    (4, 8, "1000111 0101100 0101011 0011110 1110000"),
    (4, 8, "0001110 0111010 0110101 1011001 1100010"),
    (4, 8, "0111010 0100101 1001011 1010110 0011100"),
    (4, 8, "1100011 0110110 1011000 0001111 0010101"),
    (4, 8, "0001011 0010110 0111100 1011000 1100101"),
    (4, 8, "0011011 1010110 1001101 0111000 1100001"),
    (4, 8, "0100101 0101010 1011100 0010111 1001011"),
    (4, 8, "0011110 1001100 1111000 0100101 1000011"),
    (4, 8, "1011001 1100010 0110011 0001110 0101101"),
)
# Each of these involutions permutes the rows and columns and exchanges the colors.
GENERATORS = (
    ((1, 0, 2, 3, 4), (1, 0, 3, 2, 5, 4, 6)),
    ((0, 1, 3, 2, 4), (2, 3, 0, 1, 4, 5, 6)),
)


def transform(layer, generator):
    rows, columns = generator
    return tuple("".join("1" if layer[r][c] == "0" else "0" for c in columns)
                 for r in rows)


def slots(layer):
    for r, s in combinations(range(5), 2):
        for c, d in combinations(range(7), 2):
            color = layer[r][c]
            if color == layer[r][d] == layer[s][c] == layer[s][d]:
                yield r, s, c, d, color


def construct():
    layers = set()
    occupied = set()
    distribution = Counter()
    for size, count, seed in SEEDS:
        layer = tuple(seed.split())
        a = transform(layer, GENERATORS[0])
        b = transform(layer, GENERATORS[1])
        orbit = {layer, a, b, transform(a, GENERATORS[1])}
        if len(orbit) != size or layers & orbit:
            raise ValueError("Incorrect orbit length or repeated layer")
        layers.update(orbit)
        for member in orbit:
            rectangles = set(slots(member))
            if len(rectangles) != count or occupied & rectangles:
                raise ValueError("Incorrect rectangle count or a repeated colored rectangle")
            occupied.update(rectangles)
            distribution[count] += 1
    if len(layers) != 52 or len(occupied) != 420 or distribution != {8: 48, 9: 4}:
        raise ValueError("Incorrect final counts")
    return sorted(layers)


def main():
    layers = construct()
    path = Path(__file__).with_name("5x7x52_klein_certificate.txt")
    expected = "\n\n".join(f"Layer {i}\n" + "\n".join(layer)
                           for i, layer in enumerate(layers, 1)) + "\n"
    if path.read_text() != expected:
        raise ValueError("The expanded certificate differs from the orbit construction")
    print("52 layers, 48 with 8 rectangles and 4 with 9 rectangles")
    print("All 420 colored slots occur once. Monochromatic boxes: 0")


if __name__ == "__main__":
    main()
