"""Verify the finite layer and column assertions in minority_inventory.md."""

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations


EDGES = tuple(combinations(range(5), 2))
DISJOINT = tuple(tuple(j for j, f in enumerate(EDGES) if not set(e).intersection(f))
                 for e in EDGES)
SEEDS = (
    (3, 3, 12, 21, 22, 25, 26),
    (3, 5, 9, 14, 18, 20, 25),
    (3, 5, 9, 14, 18, 21, 28),
    (3, 5, 10, 12, 19, 22, 25),
    (3, 5, 10, 13, 19, 22, 24),
    (3, 5, 10, 13, 22, 24, 25),
)
DUPLICATE_LABELS = (1, 3, 9, 18)  # Red on 01,02,12 and blue on 34.
FOUR_BLOCKS = tuple(
    (2*e+c,) + tuple(2*f+1-c for f in DISJOINT[e])
    for e in range(10) for c in (0, 1)
)


def verify_layer_types():
    cycles = {frozenset(tuple(sorted((v[i], v[(i+1) % 5]))) for i in range(5))
              for v in permutations(range(5))}
    assert len(cycles) == 12
    all_cuts, all_cycles = set(), set()
    for layer in SEEDS:
        minority = []
        for word in layer:
            ones = tuple(i for i in range(5) if word >> i & 1)
            minority.append(ones if len(ones) == 2 else tuple(i for i in range(5) if i not in ones))
        counts = Counter(minority)
        assert max(counts.values()) <= 2 and sum(n == 2 for n in counts.values()) <= 1
        for cut in EDGES:
            all_cuts.add(sum(len(set(cut).intersection(edge)) == 1 for edge in minority))
        all_cycles.update(sum(edge in cycle for edge in minority) for cycle in cycles)
    assert all_cuts == {3, 4, 5} and all_cycles == {2, 3, 4, 5}


def verify_column_words():
    examples = (
        (0, 0, (3, 12, 12, 21, 25, 22, 26)),
        (0, 1, (3, 26, 22, 14, 25, 20, 5)),
        (0, 2, (3, 26, 26, 21, 12, 9, 6)),
        (0, 3, (3, 5, 9, 14, 18, 20, 25)),
        (1, 1, (3, 26, 25, 19, 20, 14, 13)),
        (1, 2, (3, 26, 19, 25, 20, 14, 5)),
        (1, 3, (3, 3, 12, 21, 22, 25, 26)),
    )
    for minority, majority, layer in examples:
        rectangles = []
        for p, (i, j) in enumerate(EDGES):
            for a, b in combinations(range(7), 2):
                bits = [(layer[k] >> row) & 1 for k in (a, b) for row in (i, j)]
                if len(set(bits)) == 1:
                    rectangles.append((a, b, 2*p+bits[0]))
        at_first = {label for a, b, label in rectangles if a == 0}
        assert len(rectangles) == 8
        assert (1 in at_first) == bool(minority)
        assert len(at_first - {1}) == majority


@lru_cache(None)
def matching_size(residual):
    red = [e for e in range(10) for _ in range(residual[2*e+1])]
    blue = [e for e in range(10) for _ in range(residual[2*e])]
    partners = {}

    def augment(i, seen):
        for k, e in enumerate(blue):
            if e not in DISJOINT[red[i]] or k in seen:
                continue
            seen.add(k)
            if k not in partners or augment(partners[k], seen):
                partners[k] = i
                return True
        return False

    return sum(augment(i, set()) for i in range(len(red)))


def projected_layers(residual, first=0):
    best = sum(residual) - matching_size(residual)
    for i in range(first, len(FOUR_BLOCKS)):
        block = FOUR_BLOCKS[i]
        if all(residual[e] for e in block):
            rest = list(residual)
            for e in block:
                rest[e] -= 1
            best = min(best, 1 + projected_layers(tuple(rest), i))
    return best


def main():
    verify_layer_types()
    verify_column_words()
    for n in range(5):
        for doubles in combinations(DUPLICATE_LABELS, n):
            demand = tuple(1 + (i in doubles) for i in range(20))
            expected = 6 if n == 0 or (n == 2 and 18 not in doubles) else 7
            assert projected_layers(demand) == expected
    print("Verified six minority graphs, seven single-column witnesses, and 16 two-column optima.")


if __name__ == "__main__":
    main()
