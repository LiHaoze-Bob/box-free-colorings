"""Verify the five-box 53-layer certificate and its box-free 52-layer prefix."""

from collections import Counter
from itertools import combinations
from pathlib import Path


def read_layers(filename="5x7x53_five_box_certificate.txt"):
    path = Path(__file__).with_name(filename)
    blocks = path.read_text().strip().split("\n\n")
    if len(blocks) != 53:
        raise ValueError("Expected 53 layers")
    layers = []
    for i, block in enumerate(blocks, 1):
        header, *rows = block.splitlines()
        if header != f"Layer {i}" or len(rows) != 5:
            raise ValueError(f"Invalid block for layer {i}")
        if any(len(row) != 7 or set(row) - {"0", "1"} for row in rows):
            raise ValueError(f"Invalid row in layer {i}")
        layers.append(tuple(rows))
    return layers


def main():
    layers = read_layers()
    slots = Counter()
    for i, layer in enumerate(layers, 1):
        rectangles = 0
        for r, s in combinations(range(5), 2):
            for a, b in combinations(range(7), 2):
                color = layer[r][a]
                if color == layer[r][b] == layer[s][a] == layer[s][b]:
                    slots[r, s, a, b, color] += 1
                    rectangles += 1
        if rectangles != 8:
            raise ValueError(f"Layer {i} has {rectangles} monochromatic rectangles")
        if i == 52 and Counter(slots.values()) != {1: 416}:
            raise ValueError("The 52-layer prefix is not a packing of 416 slots")
    multiplicities = Counter(slots.values())
    multiplicities[0] = 420 - len(slots)
    boxes = sum(k * (k - 1) // 2 for k in slots.values())
    if multiplicities != {0: 1, 1: 414, 2: 5} or boxes != 5:
        raise ValueError(f"Unexpected slot multiplicities {dict(multiplicities)}")
    print("52-layer prefix: 416 distinct slots, zero monochromatic boxes")
    print(f"{len(layers)} layers, {sum(slots.values())} rectangle occurrences, "
          f"{boxes} monochromatic boxes")
    print(f"Unused slots: {multiplicities[0]}; single: {multiplicities[1]}; "
          f"double: {multiplicities[2]}")


if __name__ == "__main__":
    main()
