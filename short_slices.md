# Exact rectangle multiplicities in the range \(c\le b\le2c\)

Write \(R_c(b,h)\) for the minimum number of monochromatic rectangles in a
\(c\)-coloring of a \(b\times h\) grid. A rectangle uses two distinct rows
and two distinct columns. Write \(B_a(b,h)\) for the corresponding minimum
number of monochromatic boxes in a binary \(a\times b\times h\) grid. In
particular \(N(a,b)\) is the largest \(h\) for which \(B_a(b,h)=0\), with
value infinity when the heights are unbounded.

## The rectangle theorem

**Theorem 1.** Suppose \(c\le b\le2c,\ b\ge2\), and \(h\ge1\). Put
\(r=b-c,\ E=\binom b2,\ M=cE\), and write \(rh=QM+e\), with \(0\le e<M\).
Then
\[
R_c(b,h)=M\binom Q2+eQ .
\]
Consequently, for \(c<b\le2c\), the maximum rectangle-free height is
\(\lfloor c\binom b2/(b-c)\rfloor\). For \(b\le c\) every height is
rectangle-free.

**Lower bound.** Each column has at least \(r\) monochromatic pairs of rows.
Indeed \(\binom d2\ge d-1\) for each color-class size \(d\).
For each of the \(M\) choices of a row pair and a color, count the columns in
which the two rows have that color. Write \(n_i\) for the counts. They satisfy
\(\sum_i n_i\ge rh\), and the number of monochromatic rectangles is
\(\sum_i\binom{n_i}2\). Moving one unit from an entry to another smaller by
at least two decreases this sum. The lower bound follows.

**Construction.** We may suppose \(r>0\). Write \(rh=qE+R,\ 0\le R<E\)
and put \(\nu=\lfloor b/2\rfloor\). Partition the edges of \(K_b\) into
\(E/\nu\) matchings of size \(\nu\). For even \(b\), use the vertices
\(\{\infty\}\cup\mathbb Z_{b-1}\) and the matching with the edge
\(\{\infty,x\}\) and the pairs \(\{x-i,x+i\}\) for \(1\le i\le (b-2)/2\),
one matching for each \(x\). For odd \(b\), delete a single vertex from the
even construction on \(b+1\) vertices.

Take \(q\) complete copies of this partition and then the first \(R\) edges
of one more copy, traversing its matchings consecutively. Every row pair now
has \(q\) or \(q+1\) occurrences. These occurrences come in
\(\lceil rh/\nu\rceil\le h\) matchings since \(r\le\nu\). Add empty
matchings until there are \(h\). We can give them all size \(r\). Whenever
the sizes of two matchings differ by at least two, their two-colored union
is a disjoint union of alternating paths and even cycles, counting a common
edge as a doubled edge. Some path has one more edge from the larger
matching. Exchanging its two colors maintains both matchings and strictly
decreases the sum of their squared sizes. At termination the sizes differ by
at most one and their mean is the integer \(r\).

Form a bipartite graph with the \(h\) matchings on the left and the \(E\)
row pairs on the right. An edge records the presence of that pair in that
matching. Split a right vertex of degree \(m\) into \(\lfloor m/c\rfloor\)
vertices of degree \(c\) and, if necessary, one vertex of degree \(m\bmod c\),
partitioning its incident edges arbitrarily. The maximum degree is at most
\(c\) because \(r\le c\). By the bipartite edge-coloring theorem its edges
admit a proper coloring with \(c\) colors. One short proof pads the graph
with vertices and parallel edges to a \(c\)-regular bipartite multigraph with
equally large parts. Hall's theorem supplies a perfect matching, and removing
perfect matchings successively gives the coloring.

An original right vertex of degree \(m\) now sees each color either
\(\lfloor m/c\rfloor\) or \(\lceil m/c\rceil\) times. As \(m\in\{q,q+1\}\),
all the resulting \(cE\) counts differ by at most one. Build one grid
column for each matching. Give its \(r\) disjoint pairs the \(r\) distinct
colors on their incidence edges. Give its \(b-2r=c-r\) remaining entries
the remaining colors singly. This realizes exactly the prescribed colored
pairs, attaining the lower bound. \(\square\)

## Exact transfer to binary boxes

**Theorem 2.** For all positive \(b,h\),
\[
B_3(b,h)=R_6(b,h),\qquad B_4(b,h)=2R_6(b,h).
\]

**Proof.** At a position in a \(b\times h\) array of three-bit words,
changing one bit of a constant word leaves a single equal pair of bits in
the old color and creates no new equal pair. Thus a minimizing three-row
array can be taken to use only the six nonconstant words. Each word has
one equal pair, whose row indices and color determine the word. A
monochromatic box is then exactly a monochromatic rectangle in the array
of these six symbols. Conversely any six-symbol array gives such a
three-row realization.

Extend each of the six words to four bits by appending its minority bit.
Each extended word determines two equal pairs, one in each color. Their
indices are complementary, and specifying either index pair and its color
recovers the extended word uniquely. Thus in this extension precisely two
boxes arise from every six-symbol monochromatic rectangle. For the reverse
inequality, delete each row of an arbitrary four-row array in turn. Every
box occurs in two of the four deletions, whose total box count is at least
\(4B_3(b,h)\). \(\square\)

**Consequences.** The common thresholds \(N(3,b)=N(4,b)\) are infinite for
\(b\le6\). For larger widths in the band of Theorem 1 they are as follows.

| \(b\) | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|
| \(N(3,b)=N(4,b)\) | 126 | 84 | 72 | 67 | 66 | 66 |

The two rows of thresholds agree with the upper bounds in Table 2 of
Cooper, Fenner and Purewal, obtained by subtracting one from their
uncolorability thresholds. Their paper reports matching lower bounds in
many cases without identifying every such entry. The construction here
realizes all twelve entries.
[Monochromatic Boxes in Colored Grids, §7](https://www.cse.sc.edu/~fenner/papers/boxes.pdf).

For example the \(3\times10\times68\) and \(4\times10\times68\) minimum
box counts are respectively two and four.

## Relation to previous work

Fenner, Gasarch, Glover and Purewal give a rectangle-free construction of
height \(\lfloor c/r\rfloor\binom{c+r}{2}\) and an upper bound
\(\lfloor c\binom{c+r}{2}/r\rfloor\) for \(1\le r\le c\). They match
whenever \(r\mid c\). The equitable matching construction above attains
the upper expression throughout this interval, and counts the collisions
at every greater height. See Corollary 2.12 and Theorem 3.6, as summarized at the start of the proof of Theorem 4.5 in the
[authors' manuscript](https://www.cs.umd.edu/~gasarch/papers/gridpaper.pdf)
and its [arXiv record](https://arxiv.org/abs/1005.3750).

O'Neill, Davidson, Ruiz-Navarro and Wilbur announced exact thresholds
for the first three offsets and several fixed ratios, and results on
minimum multiplicity, at the 2025 Joint Mathematics Meetings. Their
abstract gives no explicit multiplicity formula. Davidson lists a
related manuscript in preparation. The comparison above concerns the
published bounds and the statements of the available abstract.
[AMS abstract](https://meetings.ams.org/math/jmm2025/meetingapp.cgi/Paper/41246);
[author's manuscript listing](https://jjdavidson.github.io/research/ramsey-theory/).

The companion [constructive check](check_short_slices.py) builds grids by
the proof, counts their monochromatic rectangles, and counts binary boxes
after the three- and four-row lifts at six colors. Run
`python3 check_short_slices.py` to check 200 parameter triples.
