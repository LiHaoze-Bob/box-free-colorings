"""Lift uncolored minimum-layer supports to a prescribed set of doubled slots."""

from collections import Counter, defaultdict
from itertools import product

from check_complement_pairs import SEEDS, column_extensions, realizing, support
from verify_first_forced import read_layers


def orient_partial(layers, doubles):
    """Return one flip bit per layer, or None if the color capacities are impossible.

    layers contains arbitrarily oriented minimum layers, given as column masks.
    A geometry index is 10 * column-pair index + row-pair index. Indices of
    unordered pairs are lexicographic. doubles maps a geometry to the color
    of its permitted second copy. Every other colored slot has capacity one.
    """
    occurrences = defaultdict(list)
    for i, layer in enumerate(layers):
        for slot in support(layer):
            occurrences[slot//2].append((i, slot % 2))

    graph = [[] for _ in layers]
    exceptional = []
    for q, hits in occurrences.items():
        if len(hits) > 2 + int(q in doubles):
            return None
        if len(hits) < 2:
            continue
        if q in doubles:
            exceptional.append((hits, doubles[q]))
        else:
            (i, a), (j, b) = hits
            parity = 1 ^ a ^ b
            graph[i].append((j, parity))
            graph[j].append((i, parity))

    component = [-1]*len(layers)
    offset = [0]*len(layers)
    for root in range(len(layers)):
        if component[root] >= 0:
            continue
        component[root] = root
        queue = [root]
        while queue:
            i = queue.pop()
            for j, parity in graph[i]:
                want = offset[i] ^ parity
                if component[j] < 0:
                    component[j], offset[j] = root, want
                    queue.append(j)
                elif offset[j] != want:
                    return None

    free = sorted({component[i] for hits, _ in exceptional for i, _ in hits})
    for bits in product((0, 1), repeat=len(free)):
        flip = dict(zip(free, bits))
        for hits, majority in exceptional:
            n = sum((bit ^ offset[i] ^ flip[component[i]]) == majority for i, bit in hits)
            if n > 2 or len(hits)-n > 1:
                break
        else:
            return [offset[i] ^ flip.get(component[i], 0) for i in range(len(layers))]
    return None


def verify_reconstruction():
    extensions = column_extensions()
    for seed in SEEDS:
        geometries = sorted(s//2 for s in support(seed))
        completions = set()
        for bits in product((0, 1), repeat=8):
            required = [2*q+b for q, b in zip(geometries, bits)]
            completions.update(realizing(required, extensions))
        assert completions == {seed, tuple(31-w for w in seed)}


def main():
    verify_reconstruction()
    layers = [tuple(sum(int(row[j]) << i for i, row in enumerate(layer))
                    for j in range(7)) for layer in read_layers()]
    # Flip input representatives arbitrarily, then check actual capacities.
    representatives = [tuple(w ^ (31 if i % 3 else 0) for w in layer)
                       for i, layer in enumerate(layers)]
    counts = Counter(s for layer in layers for s in support(layer))
    allowed = {s//2: s % 2 for s, k in counts.items() if k == 2}
    assert len(allowed) == 5
    for n, doubles in ((52, {}), (53, allowed)):
        flips = orient_partial(representatives[:n], doubles)
        assert flips is not None
        restored = Counter(s ^ f for layer, f in zip(representatives[:n], flips)
                           for s in support(layer))
        assert all(k <= 1 + int(doubles.get(s//2) == s % 2) for s, k in restored.items())
    assert orient_partial([SEEDS[0]]*3, {}) is None
    print("All six geometric supports determine their layer up to complement.")
    print("Recovered orientations of the 52-layer packing and the five-box witness.")


if __name__ == "__main__":
    main()
