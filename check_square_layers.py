"""Verify the extremal square colorings in square_layers.md with Python 3.9+."""

from itertools import combinations
from math import comb


def rotate_blocks(row, width, shift):
    """Shift each full block right, leaving a possible final point fixed."""
    full = len(row) // width * width
    blocks = [row[i:i + width] for i in range(0, full, width)]
    return "".join(block[-shift:] + block[:-shift] if shift else block
                   for block in blocks) + row[full:]


def explicit_rows(n):
    circulants = {
        10: "1111001000",
        12: "111101001000",
        16: "1111100101001000",
        18: "111110100100011000",
        20: "11111010100100110000",
    }
    if n in circulants:
        return [rotate_blocks(circulants[n], n, s) for s in range(n)]
    if n == 14:
        seeds = ["11010001110100", "11101001000101"]
        return [rotate_blocks(seed, 7, s) for seed in seeds for s in range(7)]
    if n == 21:
        seeds = ["110010010100101100011", "001010001100111010101",
                 "100110101010101111000", "110101110000111010100"]
        return [rotate_blocks(seed, 5, s) for seed in seeds for s in range(5)] + [
            "000001111100000111111"]
    if n == 15:
        return ["".join(str(int(bin(i & j).count("1") % 2 == 0))
                        for j in range(1, 16)) for i in range(1, 16)]
    if n == 9:
        # The 3-by-3 rook graph is a conference graph on nine vertices.
        def positive(i, j):
            return i // 3 == j // 3 or i % 3 == j % 3
    elif n in (11, 13, 17, 19):
        residues = {x * x % n for x in range(1, n)}

        def positive(i, j):
            return (i - j) % n in residues
    else:
        raise ValueError("Expected an order from 9 through 21")
    return ["".join(str(int((n % 4 == 1 and i < n // 2) if i == j
                            else positive(i, j))) for j in range(n))
            for i in range(n)]


def lower_bound(n):
    if n % 4 == 1:
        t = n // 4
        return n * (n - 1) * comb(t, 2) + 2 * t * t
    if n % 4 == 3:
        return comb(n, 2) * (n // 4) ** 2
    half = n // 2
    slope = half * (half - 1) // (n - 1)
    return n * slope * half * (half - 1) - n * (n - 1) * comb(slope + 1, 2)


def check(n):
    rows = explicit_rows(n)
    if len(rows) != n or any(len(r) != n or set(r) - {"0", "1"} for r in rows):
        raise ValueError(f"Malformed square of order {n}")
    slots = list(combinations(range(n), 2))
    count = sum(rows[i][a] == rows[i][b] == rows[j][a] == rows[j][b]
                for i, j in slots for a, b in slots)
    expected = lower_bound(n)
    if count != expected:
        raise ValueError(f"{n}: observed {count}, expected {expected}")
    return count


if __name__ == "__main__":
    for size in range(9, 22):
        print(f"{size} x {size}: {check(size)}")
