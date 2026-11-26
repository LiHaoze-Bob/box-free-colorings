"""Construct and directly verify the extremal grids in short_slices.md."""

from collections import Counter
from itertools import combinations
from math import comb


def round_robin(width):
    modulus = width if width % 2 else width - 1
    for center in range(modulus):
        pairs = [tuple(sorted(((center - i) % modulus, (center + i) % modulus)))
                 for i in range(1, (modulus + 1) // 2)]
        if modulus < width:
            pairs.append((center, modulus))
        yield pairs


def balance_matchings(matchings):
    while True:
        larger = max(matchings, key=len)
        smaller = min(matchings, key=len)
        if len(larger) - len(smaller) <= 1:
            return
        neighbors = [{v: w for edge in matching for v, w in (edge, edge[::-1])}
                     for matching in (larger, smaller)]
        for start in neighbors[0].keys() - neighbors[1].keys():
            side = 0
            vertex = start
            path = set()
            while vertex in neighbors[side]:
                other = neighbors[side][vertex]
                path.add(tuple(sorted((vertex, other))))
                vertex = other
                side = 1 - side
            if side == 1:
                larger.symmetric_difference_update(path)
                smaller.symmetric_difference_update(path)
                break
        else:
            raise AssertionError("The two matchings contain no improving path")


def color_incidences(matchings, colors):
    """Apply alternating-path bipartite edge coloring to the split graph."""
    by_vertex = {}
    count = Counter()
    for round_index, matching in enumerate(matchings):
        for pair in sorted(matching):
            clone = (pair, count[pair] // colors)
            count[pair] += 1
            left = by_vertex.setdefault(round_index, {})
            right = by_vertex.setdefault(clone, {})
            alpha = next(c for c in range(colors) if c not in left)
            beta = next(c for c in range(colors) if c not in right)
            if beta in left:
                path = []
                vertex = round_index
                col = beta
                while col in by_vertex[vertex]:
                    other = by_vertex[vertex][col]
                    path.append((vertex, other, col))
                    vertex = other
                    col = alpha if col == beta else beta
                assert vertex != clone
                for u, v, old in path:
                    del by_vertex[u][old], by_vertex[v][old]
                for u, v, old in path:
                    new = alpha if old == beta else beta
                    by_vertex[u][new], by_vertex[v][new] = v, u
            left[beta], right[beta] = clone, round_index
    return by_vertex


def construct(colors, width, height):
    if width <= colors:
        return [tuple(range(width))] * height
    assert colors < width <= 2 * colors and height > 0
    pairs_per_round = width - colors
    blocks = list(round_robin(width))
    copies, remainder = divmod(pairs_per_round * height, comb(width, 2))
    matchings = [set(block) for _ in range(copies) for block in blocks]
    for block in blocks:
        if not remainder:
            break
        take = min(len(block), remainder)
        matchings.append(set(block[:take]))
        remainder -= take
    matchings.extend(set() for _ in range(height - len(matchings)))
    balance_matchings(matchings)
    incidences = color_incidences(matchings, colors)
    grid = []
    for t in range(height):
        row = [None] * width
        for color, (pair, _) in incidences[t].items():
            i, j = pair
            row[i] = row[j] = color
        unused_colors = (c for c in range(colors) if c not in incidences[t])
        grid.append(tuple(v if v is not None else next(unused_colors) for v in row))
    return grid


def count_rectangles(grid):
    counts = Counter()
    for row in grid:
        for i, j in combinations(range(len(row)), 2):
            if row[i] == row[j]:
                counts[i, j, row[i]] += 1
    return sum(comb(n, 2) for n in counts.values())


def count_lifted_boxes(grid, rows):
    words = [tuple((mask >> i) & 1 for i in range(3)) for mask in range(1, 7)]
    if rows == 4:
        words = [word + (int(sum(word) == 1),) for word in words]
    slots = Counter()
    for layer in grid:
        for i, j in combinations(range(rows), 2):
            for color in (0, 1):
                agreed = [k for k, symbol in enumerate(layer)
                          if words[symbol][i] == words[symbol][j] == color]
                for x, y in combinations(agreed, 2):
                    slots[i, j, color, x, y] += 1
    return sum(comb(n, 2) for n in slots.values())


def verify():
    tested = 0
    for colors in range(1, 8):
        for width in range(max(2, colors), 2 * colors + 1):
            slots = colors * comb(width, 2)
            pairs = width - colors
            # Include the zero threshold and cases with several collisions per slot.
            threshold = slots // max(1, pairs)
            heights = {1, 2, 3, threshold, threshold + 1, 2 * threshold + 3}
            for height in sorted(heights):
                q, e = divmod(pairs * height, slots)
                expected = slots * comb(q, 2) + e * q
                grid = construct(colors, width, height)
                assert len(grid) == height
                assert all(len(row) == width and set(row) <= set(range(colors))
                           for row in grid)
                actual = count_rectangles(grid)
                assert actual == expected, (colors, width, height, expected, actual)
                if colors == 6:
                    assert count_lifted_boxes(grid, 3) == expected
                    assert count_lifted_boxes(grid, 4) == 2 * expected
                tested += 1
    print(f"Verified {tested} constructed grids by direct rectangle counting.")


if __name__ == "__main__":
    verify()
