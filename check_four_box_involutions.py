"""Enumerate fixed minimum layers for the possible involutions at height 53."""

from collections import Counter
from itertools import combinations, product


ROW_PAIRS = tuple(combinations(range(5), 2))
COLUMN_PAIRS = tuple(combinations(range(7), 2))
COLUMN_ACTION = (1, 0, 3, 2, 5, 4, 6)


def slot(rows, columns, color):
    return 20 * COLUMN_PAIRS.index(columns) + 2 * ROW_PAIRS.index(rows) + color


def fixed_layers(row_action):
    balanced = [v for v in range(32) if bin(v).count("1") in (2, 3)]
    translate = {
        v: sum(((v >> i) & 1) << row_action[i] for i in range(5))
        for v in balanced
    }
    fixed_words = [v for v in balanced if v == translate[v]]
    for a, b, c, t in product(balanced, balanced, balanced, fixed_words):
        columns = (a, translate[a], b, translate[b], c, translate[c], t)
        rects = []
        for rows in ROW_PAIRS:
            r, s = rows
            for color in (0, 1):
                matches = tuple(j for j, v in enumerate(columns)
                                if ((v >> r) & 1) == ((v >> s) & 1) == color)
                if len(matches) == 2:
                    rects.append(slot(rows, matches, color))
                elif len(matches) != 1:
                    break
            else:
                continue
            break
        else:
            yield tuple(rects), t


def fixed_slots(row_action):
    return {slot(rows, columns, color)
            for rows in ROW_PAIRS
            if tuple(sorted(row_action[i] for i in rows)) == rows
            for columns in COLUMN_PAIRS
            if tuple(sorted(COLUMN_ACTION[i] for i in columns)) == columns
            for color in (0, 1)}


def orbit_count(states, maps):
    remaining = set(states)
    count = 0
    while remaining:
        state = remaining.pop()
        images = {tuple(sorted(mapping[v] for v in state)) for mapping in maps}
        remaining.difference_update(images)
        count += 1
    return count


def inequivalent_families(layers, families, supports, ordinary):
    # Swapping the two exchanged rows acts like reversing all three column
    # pairs, because their product is the involution fixing our objects.
    by_rectangles = {tuple(sorted(rects)): i for i, (rects, _) in enumerate(layers)}
    if len(by_rectangles) != len(layers):
        raise ValueError("The fixed-layer rectangle sets must identify the layers")
    family_maps, support_maps = [], []
    for swap, flips in product((0, 1), product((0, 1), repeat=3)):
        row_image = (0, 1, 3, 2, 4) if swap else tuple(range(5))
        pair_image = (0, 2, 1) if swap else (0, 1, 2)
        col_image = tuple(2 * pair_image[i // 2] + ((i % 2) ^ flips[i // 2])
                          for i in range(6)) + (6,)
        mapping = [slot(tuple(sorted(row_image[i] for i in rows)),
                        tuple(sorted(col_image[j] for j in columns)), color)
                   for columns in COLUMN_PAIRS for rows in ROW_PAIRS for color in (0, 1)]
        family_maps.append([by_rectangles[tuple(sorted(mapping[s] for s in rects))]
                            for rects, _ in layers])
        support_maps.append({s: ordinary[mapping[s]] for s in ordinary})
    return orbit_count(families, family_maps), orbit_count(supports, support_maps)


def count_prefixes(layers, fixed):
    # The red two-row class is {0,1}. Its double and the three blue doubles
    # on the other rows use the canonical columns in the analytic proposition.
    doubles = {
        slot((0, 1), (0, 1), 1),
        slot((2, 3), (0, 1), 0),
        slot((2, 4), (2, 3), 0),
        slot((3, 4), (4, 5), 0),
    }
    red_double = slot((0, 1), (0, 1), 1)
    selectors = sorted(s for s in fixed if s % 20 < 2 and s != red_double)
    # Each of these five slots belongs to one fixed layer.
    groups = [[] for _ in selectors]
    ordinary_representatives = {}
    for rows in ROW_PAIRS:
        image_rows = tuple(sorted((1, 0, 2, 3, 4)[i] for i in rows))
        for columns in COLUMN_PAIRS:
            image_columns = tuple(sorted(COLUMN_ACTION[j] for j in columns))
            for color in (0, 1):
                s = slot(rows, columns, color)
                image = slot(image_rows, image_columns, color)
                if image != s:
                    ordinary_representatives[s] = min(s, image)
    supports = set()
    families = set()
    chosen = []
    for layer_id, (rects, t) in enumerate(layers):
        if red_double in rects:
            continue
        label, = set(rects).intersection(selectors)
        regular = sum(1 << s for s in rects if s not in doubles)
        special = sum(1 << s for s in rects if s in doubles)
        ordinary = sum(1 << q for q in {ordinary_representatives[s]
                                         for s in rects if s not in fixed})
        groups[selectors.index(label)].append((regular, special, t, ordinary, layer_id))
    required = sum(1 << s for s in fixed if s not in doubles)
    count = parity_count = 0
    blue_counts = Counter()

    def visit(depth, occupied, seen_once, seen_twice, row_parity, ordinary):
        nonlocal count, parity_count
        if depth == len(groups):
            if (occupied & required) == required and not seen_once:
                count += 1
                blue_counts[bin(seen_twice).count("1")] += 1
                # Rows 2, 3, 4 all have odd total weight 185.
                if (row_parity & 0b11100) == 0b11100:
                    parity_count += 1
                    supports.add(ordinary)
                    families.add(tuple(sorted(chosen)))
            return
        for regular, special, t, new_ordinary, layer_id in groups[depth]:
            if regular & occupied or special & seen_twice:
                continue
            chosen.append(layer_id)
            visit(depth + 1, occupied | regular, seen_once ^ special,
                  seen_twice | (seen_once & special), row_parity ^ t, ordinary | new_ordinary)
            chosen.pop()

    visit(0, 0, 0, 0, 0, 0)
    representatives = sorted(set(ordinary_representatives.values()))
    support_sets = {tuple(s for s in representatives if bits & (1 << s)) for bits in supports}
    allowed = [set(), set(), set()]
    for s in representatives:
        i, j = ROW_PAIRS[(s % 20) // 2]
        a, b = COLUMN_PAIRS[s // 20]
        if i >= 2 or j < 2 or b == 6:
            continue
        if s % 2 == 0 and a // 2 != b // 2:
            allowed[0].add(s)
        elif s % 2 == 1 and (a, b) in ((2, 3), (4, 5)):
            allowed[a // 2].add(s)
    if [len(group) for group in allowed] != [36, 3, 3]:
        raise ValueError("Unexpected size of the 42-orbit support restriction")
    if any([len(group.intersection(support)) for group in allowed] != [5, 1, 1]
           for support in support_sets):
        raise ValueError("Unexpected color or column type in an ordinary support")
    classes = inequivalent_families(layers, families, support_sets, ordinary_representatives)
    return count, parity_count, len(supports), blue_counts, classes


def main():
    for action, expected in (
        ((1, 0, 2, 3, 4), {4: 144, 6: 144}),
        ((1, 0, 3, 2, 4), {2: 480}),
    ):
        fixed = fixed_slots(action)
        layers = list(fixed_layers(action))
        spectrum = Counter(len(fixed.intersection(rects)) for rects, _ in layers)
        if spectrum != expected:
            raise ValueError(f"Unexpected fixed-slot spectrum {spectrum}")
        print(f"Row action {action}, fixed layers {len(layers)}, "
              f"fixed slots per layer {dict(sorted(spectrum.items()))}")
        if action == (1, 0, 2, 3, 4):
            counts = count_prefixes(layers, fixed)
            if counts != (74240, 49664, 26288, {0: 24576, 3: 49664}, (3164, 1681)):
                raise ValueError(f"Unexpected fixed-layer families {counts}")
            print(f"Single-transposition fixed-layer families {counts[0]}, "
                  f"after row-weight parity {counts[1]}, ordinary supports {counts[2]}")
            print(f"Inequivalent fixed-layer families {counts[4][0]}, "
                  f"inequivalent ordinary supports {counts[4][1]}")
        else:
            mask_counts = Counter(tuple(sorted(fixed.intersection(rects))) for rects, _ in layers)
            if len(mask_counts) != 18:
                raise ValueError(f"Unexpected number of fixed-slot pairs {len(mask_counts)}")
            for (a, b), count in mask_counts.items():
                expected_count = 16 if a // 20 == b // 20 else 32
                if a % 2 == b % 2 or count != expected_count:
                    raise ValueError(f"Unexpected opposite-color mask {(a, b)} of size {count}")
            print("Double-transposition fixed-slot pairs 18, multiplicities 16 or 32")


if __name__ == "__main__":
    main()
