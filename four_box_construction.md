# Four monochromatic boxes at height 53

The binary $5\times7\times53$ grid has minimum box count **four**. Each layer supplies at least eight monochromatic rectangles. Across 53 layers there are at least 424 occurrences among the 420 colored rectangle slots. For every slot used $k$ times, the box count $\binom{k}{2}$ is at least $k-1$. Summation gives the lower bound four. The construction below attains it.

## Fifteen seeds

Number rows from 0 to 4 and columns from 0 to 6. A layer is a tuple of seven column words, with row $i$ stored in bit $i$. Let $g$ act by the row permutation $(0\,1)(2\,3\,4)$ and the column permutation $(0\,3\,4\,1\,2\,5)$. Move the cell at $(i,j)$ to its image and preserve the bit. Write $h=g^3$, which interchanges rows 0 and 1 and column pairs $01,23,45$.

| Copies | Column words |
|---:|---|
| 1 | 18, 17, 9, 10, 28, 28, 7 |
| 1 | 18, 17, 11, 11, 6, 5, 28 |
| 1 | 5, 6, 28, 28, 10, 9, 19 |
| 1 | 10, 9, 5, 6, 19, 19, 28 |
| 1 | 28, 28, 18, 17, 5, 6, 11 |
| 2 | 7, 11, 9, 14, 21, 18, 28 |
| 2 | 7, 22, 10, 25, 18, 5, 28 |
| 2 | 14, 5, 19, 9, 25, 18, 28 |
| 6 | 28, 19, 21, 6, 13, 11, 24 |
| 6 | 19, 24, 13, 6, 26, 20, 11 |
| 6 | 6, 20, 9, 26, 24, 13, 19 |
| 6 | 10, 6, 11, 22, 28, 17, 5 |
| 6 | 12, 21, 3, 25, 10, 22, 5 |
| 6 | 18, 14, 20, 3, 9, 5, 25 |
| 6 | 14, 26, 19, 20, 9, 7, 5 |

Take each one-copy layer once, each two-copy seed together with its $h$ image, and all six $g$ images of each remaining seed. The expansion has $5+3\cdot2+7\cdot6=53$ distinct layers. Every layer has eight rectangles, every colored slot occurs, and exactly four occur twice. The full symmetry group has order two by the [row-action bound](first_forced_height.md).

The [expanded coloring](5x7x53_four_box_certificate.txt) orders the six images of a seed by powers $0,3,1,4,2,5$. Its four boxes are

| Layers, one-based | Rows, zero-based | Columns, zero-based | Bit |
|---|---|---|---:|
| 1, 2 | 2, 3 | 0, 1 | 0 |
| 1, 2 | 2, 4 | 2, 3 | 0 |
| 2, 5 | 3, 4 | 4, 5 | 0 |
| 6, 7 | 0, 1 | 0, 1 | 1 |

Run `python3 verify_four_box_53.py` to regenerate the layers and compare them with the expanded file. The verifier counts slot multiplicities and directly checks all $\binom{53}{2}\binom52\binom72=289{,}380$ possible boxes using their eight corner bits. [Independent certificate verifier](verify_four_box_53.py)

## A second coloring and the possible double slots

An inequivalent completion has the same first eleven layers. Among the 53 layers, the number with either 16 or 19 red cells is 14 for the first coloring and two for the second. Coordinates have distinct dimensions. An independent permutation on any coordinate preserves the layer-weight multiset, and global color interchange exchanges weights 16 and 19. The colorings are therefore inequivalent. The same verifier checks both the four-box property and this invariant. [Second expanded coloring](5x7x53_four_box_second_certificate.txt)

Fix the labels and colors of the two row-weight classes, with the two heavier rows red on their double slot. Among colorings admitting a single row transposition, there are exactly **1,890** assignments of column pairs to the four labeled double slots. The three labeled edges of the blue row triangle must use pairwise disjoint column pairs. These can be chosen in $21\cdot10\cdot3$ ways. The double on the red row pair must coincide geometrically with one of those three column pairs, giving three choices. Conversely, start with the displayed coloring, use a permutation of the three fixed rows to choose which edge of the triangle shares a column pair with the red double, and use a column permutation to send the three disjoint pairs to any prescribed triple. This realizes all $21\cdot10\cdot3\cdot3=1{,}890$ assignments. The count fixes row labels and permits the column involution to vary.

## How the certificate was found

The [fixed-layer classification](four_box_involutions.md) reduces this row action to an exact cover of 198 ordinary two-element $h$-orbits. Five fixed layers together supply seven ordinary orbits, the pair supplying the red double contributes another seven, and 23 other pairs supply eight each. On the 198 ordinary orbits the induced action of $g$ has 66 cycles of length three.

The search reserved seven complete $g$-orbits of layers, accounting for 42 layers. This left the five fixed layers, the exceptional red-double pair, and two more pairs. Together these eleven layers had to occupy $7+7+8+8=30$ ordinary orbits and cover ten complete cycles in the 66-cycle quotient. Only their combined ordinary-slot support was required to be invariant under $g$.

For each proposed disjoint pair of seven-element supports, the search took their union and all its $g$ images. When this had size 30, it remained to partition the 16 missing ordinary slots into two realizable eight-element supports. Two slots that occur together in no admissible eight-element support must go to opposite parts. The search tested these constraints by two-coloring their incompatibility graph, then checked both resulting parts against the catalog of supports. The seven complete six-layer orbits cover the other 56 cycles in seven disjoint eight-element sets. An exact-cover search completed this last step. The seed table above provides a direct verification independent of these search choices.

The [standalone C++17 search](search_four_box_core.cpp) reproduces the second completion starting from only the eleven-layer prefix. It enumerates row, column and color images of the six minimum-layer types. After retaining only seeds whose six translates use distinct residual slots, it finds 89,720 different eight-element supports on the remaining 56 cycles. It solves their exact-cover problem and checks all slot multiplicities of the resulting 53 layers. From the repository root, run

```sh
c++ -O3 -std=c++17 search_four_box_core.cpp -o /tmp/search_four_box_core
/tmp/search_four_box_core
```

## At least 15,907 inequivalent optimal colorings

Keep the first eleven layers and the two six-layer orbits whose seeds are
$(6,20,9,26,24,13,19)$ and $(10,6,11,22,28,17,5)$. The other five
six-layer orbits must partition 40 six-element orbits of colored slots.
The catalog contains 9,007 different eight-element supports within these
40 positions. It gives **15,907** different partitions into five supports.
Retain one witnessing seed for each catalog entry. Each partition now
gives a 53-layer coloring with the same four doubled slots.

An independent way to count partitions is to fix a position and choose
the unique tile of a partition containing it. On the remaining 32
positions $R$, form $P(S)$, the number of unordered disjoint pairs of
tiles with union $S$. The number of four-tile partitions of $R$ is
$$
 \frac16\sum_{S}P(S)P(R\setminus S).
$$
Each partition contributes six times by choosing its first pair of tiles.
Summing over the choice of the first tile gives 15,907. This is an exact
count of support partitions for the stated subproblem and a lower bound
on the number of inequivalent optimal colorings.

To prove inequivalence, every member of this family admits $h$, and
the [row-action theorem](first_forced_height.md) bounds its full group
by two. An isomorphism must therefore send the five $h$-fixed layers
to the same five layers. Their set is common to the whole family. A
global color exchange cannot preserve the three blue doubles and one
red double. Among color-preserving row and column permutations, only
32 preserve the four colored doubles, and only the identity and $h$
also preserve the five fixed layers. The [certificate checker](verify_four_box_53.py)
tests these permutations directly. Both permutations preserve each
whole stack setwise. Consequently two distinct layer sets in this
family are inequivalent even after height permutations and color
exchange. Distinct partitions give distinct sets, since the fixed
action $g$ recovers the decomposition of the 30 varying layers into
its orbits.

Run the [core search](search_four_box_core.cpp) with a second argument
to reproduce the count.

```sh
c++ -O3 -std=c++17 search_four_box_core.cpp -o /tmp/search_four_box_core
/tmp/search_four_box_core 5x7x53_four_box_certificate.txt --count-family
```
