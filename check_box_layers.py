"""Check the Alm–Miller 5×7×50 certificate and test exact local extensions.

Run with Python 3.9+:
    python3 check_box_layers.py 5x7x50_exact_zero_certificate.txt
Input: https://github.com/algorithmachine/box-free-colorings/blob/main/5x7x50_exact_zero_certificate.txt
"""

import argparse
import re
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path


ROW_PAIRS = list(combinations(range(5), 2))
COLUMN_PAIRS = [(1 << a) | (1 << b) for a, b in combinations(range(7), 2)]


def read_layers(path):
    sections = re.split(r"^Layer [0-9]+\s*$", path.read_text(), flags=re.MULTILINE)
    layers = []
    for section in sections[1:]:
        rows = section.split()
        if len(rows) != 5 or any(not re.fullmatch(r"[01]{7}", r) for r in rows):
            raise ValueError("Each layer must contain five rows of seven bits")
        layers.append(tuple(int(row, 2) for row in rows))
    if len(layers) != 50:
        raise ValueError("Expected the 50-layer certificate")
    return layers


def row_pair_mask(first, second):
    """For this pair of rows, encode 21 column pairs × 2 colours as 42 bits."""
    mask = 0
    for index, cols in enumerate(COLUMN_PAIRS):
        if (first & second & cols) == cols:
            mask |= 1 << (2 * index + 1)
        if ((first | second) & cols) == 0:
            mask |= 1 << (2 * index)
    return mask


PAIR_MASK = [[row_pair_mask(a, b) for b in range(128)] for a in range(128)]


def signature(layer):
    return tuple(PAIR_MASK[layer[i]][layer[j]] for i, j in ROW_PAIRS)


def enumerate_extensions(fixed):
    """Generate every layer compatible with the fixed layers, row by row."""
    occupied = dict.fromkeys(ROW_PAIRS, 0)
    for layer in fixed:
        for p, slots in zip(ROW_PAIRS, signature(layer)):
            occupied[p] |= slots

    @lru_cache(maxsize=None)
    def compatible_rows(i, j, row):
        forbidden = occupied[i, j]
        return sum(1 << b for b, mask in enumerate(PAIR_MASK[row]) if not mask & forbidden)

    def extend(prefix):
        if len(prefix) == 5:
            yield prefix
            return
        candidates = (1 << 128) - 1
        for i, row in enumerate(prefix):
            candidates &= compatible_rows(i, len(prefix), row)
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            yield from extend(prefix + (bit.bit_length() - 1,))

    yield from extend(())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    layers = read_layers(parser.parse_args().certificate)
    signatures = [signature(layer) for layer in layers]
    sizes = Counter(sum(bin(mask).count("1") for mask in s) for s in signatures)
    # A repeated slot in two layers gives exactly one monochromatic box.
    boxes = sum(bin(a & b).count("1") for u, v in combinations(signatures, 2)
                for a, b in zip(u, v))
    print("Rectangles per layer (count: layers):", dict(sorted(sizes.items())))
    print("Monochromatic boxes in the certificate:", boxes)
    if boxes:
        raise ValueError("The certificate has monochromatic boxes")
    print("Ways to append one layer:", sum(1 for _ in enumerate_extensions(layers)))
    counts = Counter()
    replacements = 0
    for index in range(len(layers)):
        fixed = layers[:index] + layers[index + 1:]
        options = [signature(layer) for layer in enumerate_extensions(fixed)]
        counts[len(options)] += 1
        replacements += sum(all(not (a & b) for a, b in zip(u, v))
                            for u, v in combinations(options, 2))
    print("Possible single replacements after one deletion (options: cases):", dict(sorted(counts.items())))
    print("Ways to replace one layer by two:", replacements)


if __name__ == "__main__":
    main()
