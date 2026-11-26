"""Check finite witnesses and the uniform lift for the 5 x 7 multiplicity theorem.

Each pair of lines in the data file gives the first and last certified prefix
length and then the layers of a stack. Each layer is seven base-32 column
masks, with row zero in the low bit. Run from any directory with Python 3.9+.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIGITS = "0123456789abcdefghijklmnopqrstuv"
A = (7, 11, 12, 17, 17, 22, 26)
B = (5, 9, 10, 17, 19, 22, 28)
UNSETTLED = {53: 1, 105: 1}  # upper bounds exceed the proved lower bound by one


def check(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(None)
def slots(layer):
    occupied = []
    for p, (r, s) in enumerate(combinations(range(5), 2)):
        for e, (u, v) in enumerate(combinations(range(7), 2)):
            bit = (layer[u] >> r) & 1
            if bit == ((layer[u] >> s) & 1) == ((layer[v] >> r) & 1) == ((layer[v] >> s) & 1):
                occupied.append(21 * (2*p + bit) + e)
    check(len(occupied) == 8, "A layer does not have eight rectangles")
    return occupied


def uniform_block():
    for seed in (A, B):
        for shift in range(5):
            rotated = [((word << shift) | (word >> (5-shift))) & 31 for word in seed]
            for a in (1, 2, 4):
                for b in range(7):
                    layer = [0] * 7
                    for j, word in enumerate(rotated):
                        layer[(a*j+b) % 7] = word
                    yield tuple(layer)


def witnesses():
    path = ROOT / "5x7x53_five_box_certificate.txt"
    rows = [block.splitlines()[1:] for block in path.read_text().strip().split("\n\n")]
    prefix = [tuple(sum(int(bit) << i for i, bit in enumerate(column))
                    for column in zip(*layer)) for layer in rows]
    yield 1, 53, prefix

    lines = (ROOT / "5x7_multiplicity_certificates.txt").read_text().splitlines()
    check(len(lines) % 2 == 0, "Incomplete certificate record")
    for header, line in zip(lines[::2], lines[1::2]):
        first, last = map(int, header.split())
        layers = [tuple(DIGITS.index(d) for d in word) for word in line.split()]
        check(len(layers) == last and 1 <= first <= last, "Wrong certificate length")
        check(all(len(layer) == 7 for layer in layers), "Expected seven columns")
        yield first, last, layers


def main():
    block = list(uniform_block())
    uniform = Counter(slot for layer in block for slot in slots(layer))
    check(len(block) == 210 and uniform == {s: 4 for s in range(420)},
          "Invalid uniform lift")
    checked = {}
    for first, last, stack in witnesses():
        counts = [0]*420
        check(len(stack) == last, "Incomplete stack")
        for h, layer in enumerate(stack, 1):
            for slot in slots(layer):
                counts[slot] += 1
            if h < first:
                continue
            q, e = divmod(8*h, 420)
            boxes = sum(comb(n, 2) for n in counts)
            lower = 420*comb(q, 2) + e*q + 2*(h % 210 == 105)
            check(boxes == lower + UNSETTLED.get(h, 0), f"Incorrect count at {h}")
            check(h not in checked, f"Duplicate height {h}")
            checked[h] = boxes
    check(set(checked) == set(range(1, 211)) | {263, 315}, "Missing height")
    # Each residue has a sharp minimum-layer witness, and can now be lifted.
    sharp = {h % 210 for h in checked if h not in UNSETTLED}
    check(len(sharp) == 210, "A residue is missing a sharp witness")
    print("Verified the uniform 210-layer lift and all 210 residue classes.")
    print("Direct box counts:", {h: checked[h] for h in (52, 53, 54, 105, 263, 315)})


if __name__ == "__main__":
    main()
