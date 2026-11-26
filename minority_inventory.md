# Minority pairs and column projections at height 53

Suppose a binary \(5\times7\times53\) stack has four monochromatic boxes.
Every layer then has exactly eight monochromatic rectangles. Every one of
the 420 colored slots occurs once, and four distinct slots occur one
additional time. After a global color swap and row relabeling, the three
rows in \(H\) have weight 186 and the two rows in \(K\) have weight 185.
The doubled slots are red on the three edges of \(H\) and blue on the
single edge \(K\). These equality conditions are proved in
[first_forced_height.md](first_forced_height.md). We use red for bit one.

## The histogram of minority pairs

Every column word of a minimum layer contains two bits of one color and
three of the other. Call the pair of rows carrying the minority color its
minority edge. Across the 371 column words, each of the ten edges of
\(K_5\) occurs as minority edge exactly 37 times, except \(K\), which
occurs 38 times. The red minority words form an edge multiset in which
every vertex has degree 74. The blue minority degrees are 74 on \(H\)
and 75 on \(K\).

To see the first statement, let \(n_{ij}\) count occurrences of minority
edge \(ij\), and put \(D_i=\sum_{j\ne i} n_{ij}\). A pair \(ij\) agrees
in a column word exactly when it is itself the minority edge, or when the
minority edge is disjoint from it. Its agreement count is therefore
\(371-D_i-D_j+2n_{ij}\). In each layer a particular colored row pair
agrees once plus the number of rectangles it supplies, since it agrees
in either one or two columns. Thus its total agreement count, summed over
both colors, is \(148+\mathbf1_{ij\subset H\ \mathrm{or}\ ij=K}\).
The proposed values \(n_{ij}=37+\mathbf1_{ij=K}\) satisfy these equations.
They are unique by the reconstruction below.

For the orientation, let \(q_{ij}\) count the red minority words
on \(ij\). The red agreements on \(ij\) come from these \(q_{ij}\)
words and the blue minority words on edges disjoint from \(ij\).
Since \(\sum_{e\cap ij=\varnothing}n_e=111+\mathbf1_{ij\subset H}\)
and the required red agreement count is \(74+\mathbf1_{ij\subset H}\),
we obtain
\[
 \sum_{e\cap ij=\varnothing}q_e-q_{ij}=37 .
\]
The sum over the ten edges gives \(\sum q_e=185\). Writing \(f_i\) for
the degrees of \(q\) now gives \(185-f_i-f_j=37\) for every \(ij\).
All degrees equal 74, as claimed.

### Reconstruction for a partially filled stack

The inventory can be used with any remaining number \(t\) of minimum
layers. Write \(r_{ij,c}\) for the number of outstanding rectangles on
row pair \(ij\) and color \(c\), summed over the column pairs. Put
\(r_{ij}=r_{ij,0}+r_{ij,1}\) and \(r_i=\sum_{j\ne i}r_{ij}\).
The required remaining minority-edge counts are forced by
\[
 D_i=6t-r_i,\qquad 2n_{ij}=7t+r_{ij}-r_i-r_j.                    \tag{1}
\]
Indeed \(7t-D_i-D_j+2n_{ij}=2t+r_{ij}\), by the agreement count above.
Sum in \(j\ne i\) and use \(\sum_i D_i=14t\) to obtain (1).

The orientation feasibility test has ten bounded integer variables. Let
\(b_{ij}\) count blue minority words and put \(B=(3t+\sum r_{ij,1})/2\),
the number of such words. Each red minority word contributes one red pair
and each blue minority word contributes three. With
\(g_i=\sum_{j\ne i}b_{ij}\), the test is
\[
 0\le b_{ij}\le n_{ij},\quad \sum b_{ij}=B,\quad
 g_i+g_j=B+n_{ij}-t-r_{ij,1}.                                     \tag{2}
\]
All counts must be integers. Conditions (1) and (2), including nonnegative
\(n_{ij}\) and \(\sum n_{ij}=7t\), characterize the realizability of
the agreement totals by an unordered multiset of \(7t\) balanced words.
Sufficiency follows by taking \(b_{ij}\) blue and \(n_{ij}-b_{ij}\) red
minority words on each edge. Equation (2) gives the red agreements, and
(1) supplies the two-color total.

Layer restrictions give additional inequalities. For example, in each
minimum layer a prescribed \(2+3\) cut of the row vertices is crossed
by three, four or five minority edges, counted with multiplicity. A
prescribed five-cycle contains between two and five. At most one edge can
have multiplicity two, and none has larger multiplicity. Hence the
remaining inventory satisfies
\[
 3t\le n(\delta(S))\le5t\quad(|S|=2),\qquad
 2t\le n(C_5)\le5t,\qquad \sum_e(n_e-t)_+\le t.
\]
These layer assertions follow by testing the six classified column
multisets against the ten cuts and the twelve five-cycles. The accompanying
[projection check](check_column_projections.py) performs these finite tests.

## One physical column

For a fixed balanced word \(w\), write \(F(w)\) for the four colored row
pairs agreeing in it. At a chosen column \(j\) of a minimum layer, the set
\(G\) of colored row pairs giving rectangles incident with \(j\) may be
any subset of \(F(w)\) except the singleton consisting of its minority
edge alone. If the minority pair agrees in that color at another column,
at least two of the other three rows have the opposite color there, so
one majority pair repeats too.

For completeness, the following are seven realizations with first column
word 3, using the low bit for row zero. The middle column counts the
incident pairs among the three majority pairs. Permuting the three majority
rows acts transitively on subsets of each fixed size.

| Minority pair incident | Majority pairs incident | Seven column words |
|---|---:|---|
| No | 0 | 3 12 12 21 25 22 26 |
| No | 1 | 3 26 22 14 25 20 5 |
| No | 2 | 3 26 26 21 12 9 6 |
| No | 3 | 3 5 9 14 18 20 25 |
| Yes | 1 | 3 26 25 19 20 14 13 |
| Yes | 2 | 3 26 19 25 20 14 5 |
| Yes | 3 | 3 3 12 21 22 25 26 |

This yields an exact completion test for the projection onto one column.
Let \(a_{p,c}\) be the outstanding incidences at that column in colored
row pair \(p,c\). They can be realized there by \(t\) minimum layers if and
only if there are nonnegative integers \(z_w\), over the 20 balanced
words, such that
\[
 \sum_w z_w=t,\qquad \sum_{w:(p,c)\in F(w)}z_w\ge a_{p,c}.
\]
For sufficiency, allocate the requested incidences for each label
independently to distinct compatible words. If the assigned set of a
word is only its minority edge, replace that word by one containing
the same colored edge in its majority class. The assigned singleton stays
valid and the seven examples realize all assigned sets. If word counts
have already been fixed, the corresponding test instead has variables
for the 300 allowed pairs \((w,G)\), so the replacement is unnecessary.

## A physical pair of columns

On a fixed column pair, the nonempty set of slots supplied by a single
minimum layer has one of the following forms.

1. A single colored row edge.
2. A red and a blue edge with disjoint row endpoints.
3. The four agreements of one balanced word, comprising a triangle in
   one color and the complementary edge in the other.

Indeed write the rows common in red or in blue in the two columns as
disjoint vertex sets. Each has size at most three. An intersection of
size three forces both words to have exactly those three rows in that
color and hence to coincide. If both intersections have size two, they
give disjoint edges. The other nonempty possibility is a single edge.
All three forms and the empty form occur in minimum layers. The layers
\((3,3,12,21,22,25,26)\) and \((3,5,9,14,18,20,25)\) give examples;
row permutations and a color swap realize all versions of each form.

For a residual red-blue multigraph on the five rows, a block of type 3
uses four specified edge copies. Choose any collection of \(q\) such
blocks respecting the outstanding multiplicities. On the remaining copies
form a bipartite graph, red against blue, joining disjoint pairs of row
edges. Let \(\nu\) be its maximum matching size and \(M\) the original
number of outstanding copies. The least number of layers needed at this
column pair is exactly
\[
 \min_{\text{feasible type-3 collections}}\bigl(M-3q-\nu\bigr).
\]
After choosing the four-edge blocks, each matched pair saves one more
layer and unmatched edges are supplied singly. Every layer decomposition
is counted this way. If the minimum exceeds the number of remaining
layers the partial stack cannot be completed.

For the initial demands, a column pair carrying no doubled slot requires
at least six contributing layers. With one doubled slot it requires seven.
With two doubles both on triangle edges it again requires six. Every
other nonempty set of doubled slots requires seven. The projection check
computes these optima for all 16 subsets of the four distinguished labels.
The optima apply to the indicated column projections. The four-box construction supplies an explicit globally compatible set of projections.
