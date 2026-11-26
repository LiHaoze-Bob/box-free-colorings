"""Generate and directly check 6 x 9 x 42 and 6 x 10 x 40 orbit certificates."""

from itertools import combinations
from math import comb


# A generator sends each old row/column index to the listed new index.
# The final entry is the color flip. The identity below is used at both widths.
ROW_IDENTITY = tuple(range(6))
NINE_GENERATORS = (
    (ROW_IDENTITY, (1, 2, 3, 4, 5, 6, 0, 7, 8), 0),
    ((3, 0, 5, 1, 2, 4), tuple(range(9)), 0),
)
NINE_SEEDS = (
    "110011001 100010110 111100100 001110011 010101010 001001101",
    "101000110 110101100 100011011 010010101 011110010 001101001",
)
TEN_GENERATORS = (
    ((0, 5, 3, 4, 1, 2), tuple(range(10)), 0),
    ((0, 2, 5, 3, 1, 4), (1, 2, 3, 4, 5, 6, 7, 0, 8, 9), 1),
)
TEN_SEEDS = ("1011010001 1100001101 1000111010 0101100011 0110010110 0011101100",)


def orbit(seed, generators):
    layer = tuple(seed.split())
    found = {layer}
    pending = [layer]
    while pending:
        layer = pending.pop()
        for rows, columns, flip in generators:
            image = [[""] * len(columns) for _ in rows]
            for i, r in enumerate(rows):
                for j, c in enumerate(columns):
                    image[r][c] = str(int(layer[i][j]) ^ flip)
            image = tuple("".join(row) for row in image)
            if image not in found:
                found.add(image)
                pending.append(image)
    return found


def verify(n, seeds, generators, orbit_size, rectangles):
    layers = set()
    for seed in seeds:
        part = orbit(seed, generators)
        if len(part) != orbit_size or layers & part:
            raise ValueError("Incorrect orbit size or overlapping orbits")
        layers.update(part)

    color_masks = []
    for layer in layers:
        masks = []
        for i, j in combinations(range(6), 2):
            for color in "01":
                mask = sum(1 << c for c in range(n) if layer[i][c] == layer[j][c] == color)
                masks.append(mask)
        if sum(comb(bin(mask).count("1"), 2) for mask in masks) != rectangles:
            raise ValueError("Incorrect number of monochromatic rectangles")
        color_masks.append(masks)
    # For any two layers and one colored row pair, a box exists exactly when
    # at least two common columns have that color in both rows and both layers.
    for a, b in combinations(color_masks, 2):
        for left, right in zip(a, b):
            shared = left & right
            if shared & (shared - 1):
                raise ValueError("Monochromatic box")
    print(f"6 x {n} x {len(layers)}: {len(layers) * rectangles} distinct colored slots, zero boxes")


if __name__ == "__main__":
    verify(9, NINE_SEEDS, NINE_GENERATORS, 21, 24)
    verify(10, TEN_SEEDS, TEN_GENERATORS, 40, 30)
