"""Test all two-deletion, three-insertion moves from the published 50 layers."""

from collections import Counter
from itertools import combinations
from pathlib import Path

from check_box_layers import enumerate_extensions, read_layers, signature


def disjoint(first, second):
    return all((a & b) == 0 for a, b in zip(first, second))


def main():
    certificate = Path(__file__).with_name("5x7x50_exact_zero_certificate.txt")
    layers = read_layers(certificate)
    candidate_counts = Counter()
    compatible_triples = 0
    for i, j in combinations(range(len(layers)), 2):
        fixed = [layer for k, layer in enumerate(layers) if k != i and k != j]
        choices = list(enumerate_extensions(fixed))
        if layers[i] not in choices or layers[j] not in choices:
            raise RuntimeError("A removed layer is missing from the candidates")
        candidate_counts[len(choices)] += 1
        for a, b, c in combinations(map(signature, choices), 3):
            if disjoint(a, b) and disjoint(a, c) and disjoint(b, c):
                compatible_triples += 1
    print("Deletion pairs:", sum(candidate_counts.values()))
    print("Candidate count range:", min(candidate_counts), max(candidate_counts))
    print("Compatible triples:", compatible_triples)


if __name__ == "__main__":
    main()
