"""Exclude 25 complementary layer pairs at height 53. Python 3.9+, no data files."""

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations

from check_column_projections import EDGES, SEEDS
from verify_fractional_53 import multisets


COLUMN_PAIRS = tuple(combinations(range(7), 2))
ROW_MASKS = tuple((1 << i) | (1 << j) for i, j in EDGES)
VALID_DOUBLES = {
    frozenset(2*p + int(i in high) for p, (i, j) in enumerate(EDGES)
              if (i in high) == (j in high))
    for size in (2, 3) for high in combinations(range(5), size)
}


def column_extensions():
    """All ways of appending a word to a submultiset of a minimum layer."""
    layers = set.union(*(multisets(seed) for seed in SEEDS))
    assert len(layers) == 900
    options = defaultdict(set)
    for layer in layers:
        # Encode a column multiset by independent two-bit multiplicities.
        # No word occurs three times in any of the six orbits.
        assert max(Counter(layer).values()) <= 2
        for j, word in enumerate(layer):
            others = layer[:j] + layer[j+1:]
            for n in range(7):
                for subset in combinations(others, n):
                    options[sum(1 << (2*v) for v in subset)].add(word)
    return options


@lru_cache(maxsize=8192)
def support(layer):
    slots = set()
    for c, (a, b) in enumerate(COLUMN_PAIRS):
        for color, common in enumerate((31 ^ (layer[a] | layer[b]), layer[a] & layer[b])):
            for p, mask in enumerate(ROW_MASKS):
                if common & mask == mask:
                    slots.add(20*c + 2*p + color)
    assert len(slots) == 8
    return frozenset(slots)


def realizing(required, extensions):
    ones, zeros = [0]*7, [0]*7
    for slot in required:
        c, label = divmod(slot, 20)
        mask = ROW_MASKS[label//2]
        bits = ones if label % 2 else zeros
        for j in COLUMN_PAIRS[c]:
            bits[j] |= mask
            if ones[j] & zeros[j]:
                return
    allowed = [{w for w in extensions[0] if (w & ones[j]) == ones[j] and not w & zeros[j]}
               for j in range(7)]
    order = sorted(range(7), key=lambda j: len(allowed[j]))
    words = [0]*7

    def visit(depth, counts):
        if depth == 7:
            yield tuple(words)
            return
        j = order[depth]
        for w in allowed[j] & extensions[counts]:
            words[j] = w
            yield from visit(depth+1, counts + (1 << (2*w)))

    yield from visit(0, 0)


def leaves_from(first, extensions):
    x = support(first)
    opposite = sorted(s ^ 1 for s in x)
    seconds = {layer for four in combinations(opposite, 4)
               for layer in realizing(four, extensions)}
    leaves = set()
    for second in seconds:
        y = support(second)
        k = sum((s ^ 1) in x for s in y)
        if k > 6:
            continue
        # Signs that reduce the l1 norm of the first two layers at a geometry.
        occupied = x | y
        reverse = sorted(s ^ 1 for s in occupied if (s ^ 1) not in occupied)
        need = 10-k
        thirds = {layer for hits in combinations(reverse, need)
                  for layer in realizing(hits, extensions)}
        for third in thirds:
            counts = Counter((*x, *y, *support(third)))
            geometries = {s//2 for s in counts}
            diff = {q: counts[2*q+1] - counts[2*q] for q in geometries}
            exceptional = [(q, d) for q, d in diff.items() if d]
            if len(exceptional) != 4 or any(abs(d) != 1 for q, d in exceptional):
                continue
            labels = frozenset(2*(q % 10) + int(d > 0) for q, d in exceptional)
            if labels in VALID_DOUBLES:
                holes = tuple(sorted(q for q in geometries if counts[2*q] and counts[2*q+1]))
                assert len(holes) == 10
                leaves.add(holes)
    return leaves


def edge_maps(pairs, degree):
    # Any isomorphism preserves degrees. Map vertex degrees to increasing order.
    n = max(max(e) for e in pairs)+1
    ordered = sorted(degree)
    for perm in permutations(range(n)):
        if all(degree[i] == ordered[perm[i]] for i in range(n)):
            yield [pairs.index(tuple(sorted((perm[a], perm[b])))) for a, b in pairs]


def canonical(holes):
    rows = [0]*5
    cols = [0]*7
    for q in holes:
        for i in EDGES[q % 10]:
            rows[i] += 1
        for j in COLUMN_PAIRS[q//10]:
            cols[j] += 1
    cmaps = list(edge_maps(COLUMN_PAIRS, cols))
    return min(tuple(sorted(10*c[q//10] + r[q % 10] for q in holes))
               for r in edge_maps(EDGES, rows) for c in cmaps)


def odd_triangle(holes):
    h = Counter(q % 10 for q in holes)
    return next((v for v in combinations(range(5), 3)
                 if sum(h[EDGES.index(e)] for e in combinations(v, 2)) % 2), None)


def main():
    extensions = column_extensions()
    leaves = set()
    for seed in SEEDS:
        leaves.update(leaves_from(seed, extensions))
    shapes = sorted(set(map(canonical, leaves)))
    assert len(leaves) == 18 and len(shapes) == 6
    for h in shapes:
        triangle = odd_triangle(h)
        assert triangle is not None
        print("Geometric holes", h, "odd triangle", triangle)
    print("18 labeled leaves after fixing the first layer, 6 orbits, 0 pass parity.")


if __name__ == "__main__":
    main()
