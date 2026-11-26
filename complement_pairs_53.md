# How many complementary pairs can a four-box stack contain?

**Theorem.** A four-box coloring of the binary $5\times7\times53$ grid
has at most 24 disjoint pairs of layers related by bitwise complementation.
The conclusion also holds if each pair is only required to have opposite
colors on identical rectangle supports. In particular a construction by
global color pairing must leave at least five layers unpaired.

A *geometry* specifies a row pair and a column pair, omitting the color.
There are 210 geometries. A minimum layer has eight different geometries.
The [four-box equality conditions](first_forced_height.md) prescribe
a single doubled slot on each of four different row pairs. All other
colored slots occur once.

Suppose there are 25 complementary pairs. Two of these pairs cannot use
the same geometry, since that would double both colors on one row pair.
Choose one representative per pair. Their 200 geometries are distinct.
Let $H$ consist of the ten omitted geometries, and let $h_{ij}$ count
those with row pair $ij$.

**Parity test.** On $ij$ the 25 representatives supply $21-h_{ij}$
rectangles. In each minimum layer the agreement count of a colored
row pair equals one plus its rectangle count. The distance between the
two length-175 rows of the representatives is consequently
$$
 175-(2\cdot25+21-h_{ij})=104+h_{ij}.
$$
The sum of the three Hamming distances in any triangle is even, since
each coordinate contributes zero or two. Thus every triangle sum of the
$h_{ij}$ must be even. More generally, for any $k$ complementary pairs
in such a stack the analogous distance is $5k-21+h_{ij}$. This gives
a test at any stage of a search that has chosen the unpaired layers.

## Exhausting the three remaining layers

Assign a minimum layer the signed vector $s$ on geometries with values
$+1$ on red rectangles, $-1$ on blue rectangles and zero elsewhere.
For the three remaining layers $X,Y,Z$, the sum of their signed vectors
has four nonzero entries, each of absolute value one. Their colors and
row pairs are exactly the within-class pairs in the equality conditions.
At each geometry with both signs among the three layers the paired
layers must be absent; at each geometry without both signs they must
be present. Hence $H$ is determined by the triple. The triple has
$(24-4)/2=10$ opposite-sign cancellations, counting at a geometry
the lesser of its two color multiplicities.

Some two layers have at least four opposite-sign coincidences. Indeed
each cancellation gives at least one incidence in the sum of such
coincidences over the three unordered layer pairs. Choose $X,Y$ to be
such a pair and write $k$ for its coincidence count. The norm
$\lVert s_X+s_Y\rVert_1=16-2k$, while $\lVert s_Z\rVert_1=8$ and
the final norm is four. The triangle inequality gives $k\le6$.
Adding a sign opposite the nonzero partial sum reduces its norm by one;
all other additions increase it by one. Thus $Z$ must oppose the
partial sum at exactly $10-k$ different geometries.

The [standard-library enumeration](check_complement_pairs.py) implements
the following finite check.

1. Use row permutations, column permutations and a common color exchange
   to fix $X$ to one of the six [minimum-layer representatives](classify_minimal_layers.py).
2. For each four-element subset of its eight slots, list every minimum
   layer containing the four reversed slots. This includes every eligible
   $Y$. Keep $4\le k\le6$.
3. For each subset of $10-k$ possible opposite signs for $Z$, list all
   minimum layers containing it. Check the signed sum directly, including
   the prescribed row pairs and colors, and record $H$.
4. Reduce $H$ by row and column relabeling and test the ten triangles.
   To generate constrained layers in steps 2 and 3, the checker enforces
   the required cell bits and adds column words only while their multiset
   extends to one of the 900 classified minimum column multisets.

There are 18 distinct leaves after fixing $X$ and six up to relabeling.
The table gives each orbit representative and one triangle with odd sum.
Row and column pairs are indexed lexicographically from zero, and a
geometry with respective indices $p,q$ is encoded by $10q+p$.

| Omitted geometries | Odd triangle |
|---|---|
| 5, 49, 109, 114, 138, 153, 155, 198, 200, 207 | 013 |
| 6, 18, 109, 110, 127, 166, 167, 193, 194, 202 | 023 |
| 13, 26, 74, 85, 139, 142, 168, 191, 196, 207 | 014 |
| 25, 28, 85, 88, 135, 138, 172, 199, 203, 204 | 012 |
| 56, 61, 66, 77, 129, 163, 164, 190, 197, 209 | 012 |
| 65, 79, 98, 142, 148, 158, 175, 183, 185, 204 | 012 |

All six fail the parity test. The classification and the constrained
enumeration can be reproduced with `python3 classify_minimal_layers.py`
and `python3 check_complement_pairs.py`.

## The next case gives explicit exact-cover instances

With 24 complementary pairs, five layers remain. A [stability
calculation](near_complements.md) excludes seven or eight opposite-color
coincidences between any two of these five. Allowing six gives viable
five-layer tails. One example, written as seven column masks per layer, is

```text
 3  5 10 13 19 22 24
20  3 22 17 12 13 26
25 26 13 22  3 17 12
 9 14  7 28  9 18 21
22 24 17 10 22 13  3
```

Let $H$ denote the geometries where both colors already occur in the tail.
For this example their indices are
$9,12,18,30,32,34,36,38,64,71,76,77,141,146,147,178,186,187$.
The five layers supply both colors once on $H$, plus four excess colored
slots in the prescribed pattern (an excess may itself lie on $H$).
Every triangle sum of $99+h_{ij}$ is even, as required for 24 pairs.

Completion of this tail by complementary pairs is **equivalent** to
partitioning the other 192 geometries into 24 uncolored eight-rectangle
supports of minimum layers. Given a partition, take a witnessing layer
for each tile, add its complement and append the five displayed layers.
Conversely, the paired layers in a completion cover each of those 192
geometries once per color. This removes all color choices from the
remaining search.

A [data file](complement_tails_53.txt) gives 486 such tails with pairwise
inequivalent hole sets. Each line contains five layers. Each layer is
seven base-32 digits giving the column masks in order, with row zero in
the low bit. The [verifier](check_complement_tails.py) counts all
rectangles directly, tests the four exceptional labels and the ten
triangle parities, and distinguishes the 486 sets up to row and column
permutations. A partition of any one of these complements would give a four-box
construction with 24 complementary pairs. The [known four-box
construction](four_box_construction.md) uses a different family of layers.
