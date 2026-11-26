"""Develop 15 seeds and count every monochromatic box in the 53-layer stack."""

from collections import Counter
from itertools import combinations, permutations
from pathlib import Path


# Bit i of a column word is the bit in row i. The first entry is the
# number of layers contributed by the seed to the certificate.
SEEDS = (
    (1, (18, 17, 9, 10, 28, 28, 7)),
    (1, (18, 17, 11, 11, 6, 5, 28)),
    (1, (5, 6, 28, 28, 10, 9, 19)),
    (1, (10, 9, 5, 6, 19, 19, 28)),
    (1, (28, 28, 18, 17, 5, 6, 11)),
    (2, (7, 11, 9, 14, 21, 18, 28)),
    (2, (7, 22, 10, 25, 18, 5, 28)),
    (2, (14, 5, 19, 9, 25, 18, 28)),
    (6, (28, 19, 21, 6, 13, 11, 24)),
    (6, (19, 24, 13, 6, 26, 20, 11)),
    (6, (6, 20, 9, 26, 24, 13, 19)),
    (6, (10, 6, 11, 22, 28, 17, 5)),
    (6, (12, 21, 3, 25, 10, 22, 5)),
    (6, (18, 14, 20, 3, 9, 5, 25)),
    (6, (14, 26, 19, 20, 9, 7, 5)),
)
SECOND_SEEDS = SEEDS[:8] + (
    (6, (19, 12, 11, 6, 21, 5, 24)),
    (6, (20, 5, 28, 18, 25, 7, 10)),
    (6, (25, 17, 7, 26, 22, 3, 12)),
    (6, (28, 19, 26, 9, 6, 21, 10)),
    (6, (26, 5, 6, 19, 9, 28, 14)),
    (6, (17, 22, 5, 26, 11, 12, 6)),
    (6, (12, 17, 11, 22, 5, 24, 7)),
)
ROW_ACTION = (1, 0, 3, 4, 2)
COLUMN_ACTION = (3, 2, 5, 4, 1, 0, 6)


def move(layer):
    result = [0] * 7
    for j, word in enumerate(layer):
        result[COLUMN_ACTION[j]] = sum(((word >> i) & 1) << ROW_ACTION[i] for i in range(5))
    return tuple(result)


def develop(seeds=SEEDS):
    layers = []
    for size, seed in seeds:
        powers = [seed]
        for _ in range(5):
            powers.append(move(powers[-1]))
        if move(powers[-1]) != seed or (size == 1 and powers[3] != seed):
            raise ValueError(f"Unexpected action on seed {seed}")
        for exponent in (0, 3, 1, 4, 2, 5)[:size]:
            layers.append(powers[exponent])
    if len(set(layers)) != 53:
        raise ValueError("Expected 53 distinct layers")
    return [tuple("".join(str((word >> r) & 1) for word in layer) for r in range(5))
            for layer in layers]


def check(seeds, filename):
    layers = develop(seeds)
    blocks = [f"Layer {i}\n" + "\n".join(layer) for i, layer in enumerate(layers, 1)]
    path = Path(__file__).with_name(filename)
    if path.read_text().strip() != "\n\n".join(blocks):
        raise ValueError("Expanded layers differ from the seed construction")

    row_pairs = tuple(combinations(range(5), 2))
    column_pairs = tuple(combinations(range(7), 2))
    slot_counts = Counter()
    for layer in layers:
        rectangles = 0
        for i, j in row_pairs:
            for a, b in column_pairs:
                bit = layer[i][a]
                if bit == layer[i][b] == layer[j][a] == layer[j][b]:
                    slot_counts[i, j, a, b, bit] += 1
                    rectangles += 1
        if rectangles != 8:
            raise ValueError(f"Expected eight rectangles, found {rectangles}")
    if Counter(slot_counts.values()) != {1: 416, 2: 4}:
        raise ValueError("Unexpected rectangle multiplicities")

    boxes = []
    for u, v in combinations(range(53), 2):
        x, y = layers[u], layers[v]
        for i, j in row_pairs:
            for a, b in column_pairs:
                if x[i][a] == x[i][b] == x[j][a] == x[j][b] == y[i][a] == y[i][b] == y[j][a] == y[j][b]:
                    boxes.append((u + 1, v + 1, i, j, a, b, x[i][a]))
    if len(boxes) != 4:
        raise ValueError(f"Direct eight-corner count found {len(boxes)} boxes")
    extreme_weights = sum(sum(row.count("1") for row in layer) in (16, 19) for layer in layers)
    print(f"{filename} has 53 distinct minimum layers, 416 single slots, 4 double slots")
    print("Direct eight-corner count gives four monochromatic boxes")
    for u, v, i, j, a, b, bit in boxes:
        print(f"  layers {u},{v}, rows {i},{j}, columns {a},{b}, color {bit}")
    return extreme_weights


def check_fixed_layers():
    """Stabilize the four repeated slots and the five involution-fixed layers."""
    fixed = set(develop()[:5])
    doubles = {(2, 3, 0, 1, 0), (2, 4, 2, 3, 0), (3, 4, 4, 5, 0), (0, 1, 0, 1, 1)}
    slot_stabilizers = 0
    preserving = []
    for rows in permutations(range(5)):
        if set(rows[:2]) != {0, 1}:
            continue
        for cols in permutations(range(7)):
            if cols[6] != 6:
                continue
            images = {(*sorted((rows[i], rows[j])), *sorted((cols[a], cols[b])), bit)
                      for i, j, a, b, bit in doubles}
            if images != doubles:
                continue
            slot_stabilizers += 1
            layers = {tuple("".join(layer[r][c] for c in cols) for r in rows)
                      for layer in fixed}
            if layers == fixed:
                preserving.append((rows, cols))
    identity = (tuple(range(5)), tuple(range(7)))
    involution = ((1, 0, 2, 3, 4), (1, 0, 3, 2, 5, 4, 6))
    if slot_stabilizers != 32 or set(preserving) != {identity, involution}:
        raise ValueError("Unexpected stabilizer of the common fixed layers")
    print("32 relabelings preserve the four doubled slots; only identity and the involution preserve the five fixed layers.")


def main():
    check_fixed_layers()
    first = check(SEEDS, "5x7x53_four_box_certificate.txt")
    second = check(SECOND_SEEDS, "5x7x53_four_box_second_certificate.txt")
    if (first, second) != (14, 2):
        raise ValueError("Unexpected layer-weight invariant")
    print(f"Layers with weight 16 or 19 number {first} and {second} in the two colorings")


if __name__ == "__main__":
    main()
