"""Verify 486 five-layer tails for unsigned exact cover at height 53."""

from collections import Counter
from itertools import combinations
from pathlib import Path

from check_complement_pairs import EDGES, VALID_DOUBLES, canonical
from verify_height_multiplicity import DIGITS, slots


def tail_holes(layers):
    """Return the 18 geometries already supplied in both colors by the tail."""
    assert len(layers) == 5 and len(set(layers)) == 5
    counts = Counter(s for layer in layers for s in slots(layer))
    holes, doubles = [], []
    for q in range(210):
        col, row = divmod(q, 10)
        blue, red = (counts[21*(2*row+c)+col] for c in (0, 1))
        assert min(blue, red) <= 1
        if min(blue, red) == 1:
            holes.append(q)
        if red != blue:
            assert abs(red-blue) == 1
            doubles.append(2*row + int(red > blue))
    assert len(holes) == 18 and len(doubles) == 4 and frozenset(doubles) in VALID_DOUBLES
    h = Counter(q % 10 for q in holes)
    for triple in combinations(range(5), 3):
        assert sum(99+h[EDGES.index(e)] for e in combinations(triple, 2)) % 2 == 0
    return tuple(holes)


def main():
    records = Path(__file__).with_name("complement_tails_53.txt").read_text().splitlines()
    shapes = set()
    for line in records:
        words = line.split()
        assert len(words) == 5 and all(len(w) == 7 for w in words)
        layers = [tuple(DIGITS.index(d) for d in word) for word in words]
        shapes.add(canonical(tail_holes(layers)))
    assert len(records) == len(shapes) == 486
    print("486 inequivalent 18-geometry leaves; all five-layer witnesses and triangle parities verified.")


if __name__ == "__main__":
    main()
