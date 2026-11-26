# Box-free colorings with 5 × 7 layers

How many red-and-blue 5 × 7 layers can you stack without forming a monochromatic box? Choose any two rows, two columns, and two layers. Their eight intersections form the corners of a box. A stack is box-free if every such box has corners of both colors. Write $N(5,7)$ for the maximum number of layers in a box-free stack.

## Known bounds and references

As of November 26, 2026, the published bounds are $50 \le N(5,7) \le 52$. Alm and Miller conjecture that $N(5,7) = 50$. A box-free stack of 51 layers would disprove the conjecture. Ruling out 52 layers would lower the upper bound to 51. Together, those two results would establish $N(5,7) = 51$.

- [Section 6 of Alm and Miller's paper](https://arxiv.org/html/2611.19635v1#S6)
- [Alm and Miller's 50-layer coloring](https://github.com/algorithmachine/box-free-colorings/blob/main/5x7x50_exact_zero_certificate.txt)
- [Cooper, Fenner, and Purewal, *Monochromatic Boxes in Colored Grids*](https://epubs.siam.org/doi/10.1137/080740702)

## Computational results

Each local search starts from Alm and Miller's published 50-layer coloring.

| Check | Result |
| --- | --- |
| Verify the 50-layer coloring | Each layer contains exactly 8 monochromatic rectangles. The stack contains 0 monochromatic boxes. |
| Append one layer | No layer can be added. |
| Remove one layer and insert two | None of the 50 choices of layer to remove admits a compatible pair of replacements. |
| Remove two layers and insert three | For each of the 1,225 choices of two layers to remove, between 2 and 14 candidate layers fit the remaining 48. No choice admits three pairwise compatible candidates. |
| Enumerate single layers with exactly 8 monochromatic rectangles | There are 900 layers up to column permutations. Allowing row permutations and a global swap of red and blue groups them into 6 classes of sizes 60, 120, 120, 120, 240, and 240. |

The exhaustive local searches rule out only the listed moves from this particular coloring. The six classes describe individual layers. When stacking layers, different arrangements from the same class can occupy different colored rectangle positions. Whether this classification has appeared in the literature remains an open question for this project.

## Reproducing the results

Run the following commands from the repository root with Python 3.9 or later. The scripts use only the standard library.

```sh
python3 check_box_layers.py 5x7x50_exact_zero_certificate.txt
python3 check_two_deletions.py
python3 classify_minimal_layers.py
```

## A possible route to a tighter upper bound

A color, a pair of rows, and a pair of columns together specify one of $2 \binom{5}{2} \binom{7}{2} = 420$ colored rectangle positions. In a box-free stack, each position can occur in at most one layer. Each layer contains at least 8 monochromatic rectangles, so 52 layers would occupy at least 416 positions. That leaves room for only 4 rectangles above the minimum, so at least 48 of the layers would have exactly 8 rectangles each.

Comparing how the six classes use each row pair, column pair, and color may reveal necessary conditions beyond the total count. This approach has yet to yield a tighter global upper bound.
