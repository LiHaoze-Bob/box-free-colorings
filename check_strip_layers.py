"""Verify the finite constructions and block identity for strips of height 5 and 6."""

from itertools import combinations
from math import comb


BLOCK = (35, 26, 22, 49, 38, 21, 13, 44, 11, 56)
REMAINDERS = ((), (0,), (0, 1), (0, 1, 5), (0, 1, 5, 7), (0, 1, 2, 3, 6),
              (0, 1, 2, 3, 6, 7), (0, 1, 2, 3, 4, 6, 7), tuple(range(8)),
              tuple(range(9)))


def rectangle_count(columns, height):
    count = 0
    for a, b in combinations(columns, 2):
        for i, j in combinations(range(height), 2):
            bits = {(word >> row) & 1 for word in (a, b) for row in (i, j)}
            count += len(bits) == 1
    return count


def check(height):
    slots = height * (height - 1)
    for i, j in combinations(range(height), 2):
        for color in (0, 1):
            if sum((v >> i) & 1 == (v >> j) & 1 == color for v in BLOCK) != 2:
                raise ValueError('Invalid agreement count in the ten-column block')
    for copies in (0, 1, 2):
        for r, indices in enumerate(REMAINDERS):
            columns = BLOCK * copies + tuple(BLOCK[index] for index in indices)
            n = copies * 10 + r
            if len(columns) != n:
                raise ValueError('Remainder has incorrect width')
            q, s = divmod(n, 5)
            expected = slots * comb(q, 2) + slots // 5 * s * q
            if n % 10 == 5:
                expected += 2 if height == 5 else 4
            if rectangle_count(columns, height) != expected:
                raise ValueError(f'Incorrect rectangle count at {height} by {n}')
    print(f'{height} rows: block agreements and rectangle counts for widths 0 through 29 verified')


if __name__ == '__main__':
    for m in (5, 6):
        check(m)
