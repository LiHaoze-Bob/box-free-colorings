"""Test candidate layer pools for a 53-layer, four-box substack over GF(2)."""

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations

from verify_fractional_53 import SEEDS, multisets
from verify_height_multiplicity import slots, witnesses


ALL_SLOTS = (1 << 420) - 1
ROWS = tuple(combinations(range(5), 2))


@lru_cache(None)
def incidence(layer):
    return sum(1 << s for s in slots(layer))


def switch_pool(layers):
    """Permit one column transposition moving at most one occupied slot."""
    result = set(layers)
    for layer in layers:
        before = incidence(layer)
        for i, j in combinations(range(7), 2):
            alternate = list(layer)
            alternate[i], alternate[j] = alternate[j], alternate[i]
            alternate = tuple(alternate)
            difference = before ^ incidence(alternate)
            if bin(difference).count("1") <= 2:
                result.add(alternate)
    return result


def verify_all_single_slot_trades():
    edges = tuple(combinations(range(7), 2))
    index = {e: i for i, e in enumerate(edges)}
    actions = [(perm, [index[tuple(sorted((perm[a], perm[b])))] for a, b in edges])
               for perm in permutations(range(7))]
    catalog = set.union(*(multisets(seed) for seed in SEEDS))
    patterns = {layer: tuple(divmod(s, 21) for s in slots(layer)) for layer in catalog}
    degrees = []
    for seed in SEEDS:
        target = set(slots(seed))
        labels = {s//21 for s in target}
        found = set()
        for layer, pattern in patterns.items():
            if len(labels.intersection(p for p, e in pattern)) < 7:
                continue
            for perm, edge_perm in actions:
                missing = 0
                for p, e in pattern:
                    if 21*p + edge_perm[e] not in target:
                        missing += 1
                        if missing > 1:
                            break
                if missing <= 1:
                    moved = [0]*7
                    for i, j in enumerate(perm):
                        moved[j] = layer[i]
                    found.add(tuple(moved))
        assert found == switch_pool({seed})
        assert all(len(target.intersection(slots(other))) == 7 for other in found - {seed})
        degrees.append(len(found)-1)
    assert degrees == [0, 0, 1, 0, 2, 0]
    for i, size in ((2, 2), (4, 4)):
        first = switch_pool({SEEDS[i]})
        closed = switch_pool(first)
        assert len(closed) == size and switch_pool(closed) == closed
        assert all(tuple(sorted(w)) == SEEDS[i] for w in closed)


def parity_test(layers):
    basis = {}
    for layer in layers:
        x = incidence(layer)
        while x:
            k = x.bit_length() - 1
            if k not in basis:
                basis[k] = x
                break
            x ^= basis[k]
    pivots = sorted(basis, reverse=True)

    def residue(x):
        for k in pivots:
            if x >> k & 1:
                x ^= basis[k]
        return x

    target = residue(ALL_SLOTS)
    units = [residue(1 << s) for s in range(420)]
    surviving = 0
    for size in (2, 3):
        for high in combinations(range(5), size):
            labels = [2*i + int(a in high) for i, (a, b) in enumerate(ROWS)
                      if (a in high) == (b in high)]
            a, b, c, d = [units[21*p:21*(p+1)] for p in labels]
            first_half = Counter(i ^ j for i in a for j in b)
            surviving += sum(first_half[target ^ k ^ l] for k in c for l in d)
    return len(basis), surviving


def main():
    verify_all_single_slot_trades()
    bound = 20*21**4
    cases = {54: (72, 72), 104: (136, 132), 105: (169, 169), 106: (166, 166)}
    records = list(witnesses())
    for height in (*cases, 263):
        layers = next(set(stack[:height]) for a, b, stack in records if a <= height <= b)
        augmented = switch_pool(layers)
        assert len(layers) == height
        original = parity_test(layers)
        switched = parity_test(augmented)
        if height == 263:
            counts = Counter(s for layer in layers for s in slots(layer))
            assert Counter(counts.values()) == {5: 416, 6: 4}
            double_labels = {s//21 for s, n in counts.items() if n == 6}
            assert any(double_labels == {
                2*i + int(a in high) for i, (a, b) in enumerate(ROWS)
                if (a in high) == (b in high)}
                for k in (2, 3) for high in combinations(range(5), k))
            assert original == (263, 1)
            assert len(augmented) == 709 and switched == (414, bound)
        else:
            pool_size, rank = cases[height]
            assert original == (height, 0)
            assert len(augmented) == pool_size and switched == (rank, 0)
        print(f"{height} original: rank {original[0]}, profiles {original[1]}; "
              f"{len(augmented)} after switches: rank {switched[0]}, profiles {switched[1]}")


if __name__ == "__main__":
    main()
