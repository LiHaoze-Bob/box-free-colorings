# A stability bound for complementary layers

**Proposition.** Suppose a binary $5\times7\times53$ coloring has four monochromatic boxes and contains 24 disjoint pairs of complementary layers. Among any two of the five remaining layers, at most six monochromatic rectangles of one occur with the opposite color in the other.

The [four-box equality conditions](first_forced_height.md) give four doubled slots, red on the triangle of high rows and blue on the edge of low rows, up to a global color exchange. Write $H$ for the rows of weight 186. The other rows have weight 185. Every layer uses eight distinct colored row-pair labels.

Color a geometric rectangle $q$ by assigning it sign $+1$ for red and $-1$ for blue. Thus a layer gives a signed vector on the 210 geometric rectangles. The sum over the stack has norm four, with one unit on each of the four prescribed row-pair labels. An exact complementary pair contributes zero. The [25-pair obstruction](complement_pairs_53.md) also excludes eight opposite matches between two remaining layers. Indeed, even if two layers have opposite rectangle slots but differ at some cells from exact complements, one can replace one layer by the complement of the other without changing the rectangle counts.

Suppose two remaining layers have seven opposite matches. Denote these layers by $A,\overline B$, so that $A$ and $B$ share seven of their eight colored slots. The finite calculation below checks that their eighth slots have the same colored row-pair label and use two **intersecting** column edges. In particular the signed vector of $A,\overline B$ is a difference of two units on the same row pair. Its addition can cancel a positive and a negative defect only on intersecting column edges.

Let $T$ be the three remaining layers. Replacing $\overline B$ by $\overline A$ preserves the inventory on each colored row-pair label. Each complementary pair supplies 7 red cells in every row. The replacement also preserves row weights since the colored label inventory of a minimum layer determines every row weight from their pairwise sums. Thus the row weights of $T$ are 11 on $H$ and 10 elsewhere.

Choose one representative of each of the resulting 25 pairs. For row pair $p$, define $h_p$ as 21 minus the number of geometric rectangles on $p$ in these representatives, counted with multiplicity. Then $h_p$ equals the number of blue rectangle incidences on $p$ in $T$, less one if both endpoints of $p$ lie outside $H$. No geometric disjointness assumption on the artificial representatives is needed. In each representative the two rows agree in $2$ plus its number of rectangles on $p$ columns. Their Hamming distance across all representatives is therefore $175-(50+21-h_p)=104+h_p$. The odd $h_p$ form a cut of $K_5$, given by the parities of the five row weights in the representatives.

The signed vector of $T$ has norm at least four by its prescribed row-pair totals, and at most six by the triangle inequality. The norm is even. The [standalone enumeration](check_near_complements.cpp) checks the following counts.

| Three-layer signed norm | Distinct triples encountered after fixing a first-layer representative, subject to row weights and cut parity |
| --- | ---: |
| 4 | 0 |
| 6 | 64 |

In every norm-six triple, every possible positive-negative pair on the same row pair uses **disjoint** column edges. A single-slot switch cannot reduce its norm to four.

## Reproducing the enumeration

```sh
c++ -O3 -std=c++17 check_near_complements.cpp -o /tmp/check-near-complements
/tmp/check-near-complements
```

The program enumerates all 900 balanced column multisets with eight rectangles, computes the six representatives under row permutations and color exchange, and expands the 900 multisets into 4,384,800 labeled layers. Comparing each representative against every layer gives three seven-slot switches with the first layer normalized. All three change one fixed colored row pair between intersecting column edges.

For three layers of signed norm at most six, at least nine of their 24 rectangle incidences must be canceled in pairs of opposite signs. Some two layers consequently have at least three opposite matches. Fix the first as one of the six representatives and let the second have $k$ opposite matches. The case $k=8$ leaves the full norm eight of the third layer. Otherwise the signed norm of the first two is $16-2k$. The third must hit opposite signs at least $9-k$ times, since each of its eight incidences changes the norm by one. The verifier searches precisely these candidates using lists of layers containing each colored slot. It checks both possible sizes of $H$, the cut condition, and the signed norm, then tests all opposing signs on each row pair. The reported triples are deduplicated as unordered labeled triples after normalizing the first layer.
