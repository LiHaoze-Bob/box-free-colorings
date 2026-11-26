"""Check single-orbit lower bounds for N(5,9) and N(5,10) by coordinates."""

from itertools import combinations


def orbit(seed, generators):
    first = tuple(seed.split())
    layers = {first}
    pending = [first]
    while pending:
        layer = pending.pop()
        for rows, columns, flip in generators:
            moved = [[""] * len(columns) for _ in rows]
            for i, r in enumerate(rows):
                for j, c in enumerate(columns):
                    moved[r][c] = str(int(layer[i][j]) ^ flip)
            image = tuple("".join(row) for row in moved)
            if image not in layers:
                layers.add(image)
                pending.append(image)
    return layers


def check(n, seed, generators, expected_layers, expected_rectangles):
    layers = orbit(seed, generators)
    if len(layers) != expected_layers:
        raise ValueError("Unexpected orbit size")
    occupied = set()
    for layer in layers:
        count = 0
        for a, b in combinations(range(5), 2):
            for i, j in combinations(range(n), 2):
                color = layer[a][i]
                if color == layer[a][j] == layer[b][i] == layer[b][j]:
                    slot = a, b, i, j, color
                    if slot in occupied:
                        raise ValueError(f"Repeated colored rectangle {slot}")
                    occupied.add(slot)
                    count += 1
        if count != expected_rectangles:
            raise ValueError("Unexpected rectangle count in a layer")
    print(f"5 x {n} x {len(layers)}: {len(occupied)} distinct slots, zero boxes")


def main():
    # Destinations of the original indices. Entries after the indicated
    # finite-field coordinates are fixed by the corresponding generator.
    check(9, "110000011 101101001 011001110 001110010 000011101", [
        (range(5), [(j + 1) % 7 for j in range(7)] + [7, 8], 0),
        ([1, 2, 0, 3, 4], [3 * j % 7 for j in range(7)] + [7, 8], 1),
    ], 42, 16)
    check(10, "1001011010 1011100001 0010111100 0101001101 0100110011", [
        ([(r + 1) % 5 for r in range(5)], range(10), 0),
        ([2 * r % 5 for r in range(5)], [(j + 1) % 8 for j in range(8)] + [8, 9], 1),
    ], 40, 20)


if __name__ == "__main__":
    main()
