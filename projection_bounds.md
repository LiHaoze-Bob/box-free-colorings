# Row-pair projections and narrow width-ten stacks

Write \(N(a,b)\) for the maximum box-free height of the binary \(a\times b\)
grid. Use \(d=\binom{\lfloor a/2\rfloor}{2}+\binom{\lceil a/2\rceil}{2}\)
and \(T=2\binom a2\). A balanced \(a\)-bit word has its two weights as
close as possible, hence has exactly \(d\) agreeing row pairs.

## Projection bound

Let \(z(b,h)\) be the maximum number of edges in a simple bipartite
graph with parts of sizes \(b,h\) and no four-cycle. Every box-free
\(a\times b\times h\) satisfies
\[
 d\bigl(bh+\mathbf1_{bh\ {\rm odd}}\bigr)\le Tz(b,h).                 \tag{1}
\]
For every row pair \(p=ij\) and color \(c\), project the positions
\((j',\ell)\) where both rows have color \(c\) to a bipartite graph;
any four-cycle in this graph would be a box. Write \(m_{p,c}\) for its
size and \(A_i\) for the total red weight of row \(i\). Then
\[
 m_{p,R}-m_{p,B}=A_i+A_j-bh,\qquad
 m_{p,R}+m_{p,B}\le2z(b,h)-|A_i+A_j-bh|.
\]
On the other hand \(\sum_{p,c}m_{p,c}\ge dbh\). For odd \(bh\), divide
the \(A_i\)'s into those below and above \(bh/2\). At least \(d\) pairs
lie on the same side and each contributes at least one to the absolute
sum, proving (1).

Here is a convenient version with an elementary integer parameter \(s\ge1\).
Set \(E=\binom b2,\ C=\binom{s+1}2,\ F=sbd-TC\) and let
\(\rho=(E+hC)\bmod s\) denote the least nonnegative residue. Then
\[
 TE-hF\ \ge\ T\rho+sd\,\mathbf1_{bh\ {\rm odd}}.                    \tag{2}
\]
For fixed \(p,c\), let \(k_\ell\) be its agreeing columns in layer
\(\ell\). The box-free condition gives \(L=E-\sum_\ell\binom{k_\ell}{2}
\ge0\), since the pairs of columns used in distinct layers are disjoint.
Put \(W=\sum_\ell(k_\ell-s)(k_\ell-s-1)/2\). Thus
\[
 J_{p,c}=L+W=E+hC-sm_{p,c}\ge0,\qquad J_{p,c}\equiv\rho\pmod s.
\]
Writing \(U=\sum m_{p,c}-dbh\ge0\), we have the identity
\(TE-hF=\sum J_{p,c}+sU\).
The difference of the two \(J\)'s at \(p=ij\) is, in absolute value,
\(s|A_i+A_j-bh|\). Their sum is at least twice the residue plus this
difference, proving (2). Equivalently, substitute the rounded bound
\(z(b,h)\le\lfloor(E+hC)/s\rfloor\) into (1). Without the parity term,
this bound on \(z\) is the classical Roman bound.

Some grid dimensions excluded by (2) are listed below. Entries in the
last two columns are the respective sides of (2); all violate its necessary
inequality. Deletion gives the same obstruction at every larger height.

| \(a\) | \(b\) | \(h\) | \(s\) | \(TE-hF\) | required minimum |
|---:|---:|---:|---:|---:|---:|
| 5 | 13 | 35 | 2 | 20 | 28 |
| 6 | 13 | 35 | 2 | 30 | 42 |
| 5 | 28 | 29 | 5 | 20 | 60 |
| 6 | 28 | 29 | 5 | 30 | 90 |
| 7 | 11 | 32 | 2 | 6 | 42 |
| 8 | 11 | 32 | 2 | 8 | 56 |
| 7 | 19 | 27 | 4 | 54 | 78 |
| 8 | 19 | 27 | 4 | 72 | 104 |

One can also substitute sharper bounds for \(z\) directly in (1).
For example Theorem 1.1 of Chen, Horsley and Mammoliti, with
\((m,n,k)=(14,30,3),(18,27,4),(17,25,4)\), gives respectively upper
bounds \(89,104,94\). Consequently \(N(7,14),N(8,14)\le29\),
\(N(7,18),N(8,18)\le26\), and \(N(9,17),N(10,17)\le24\).
The paper also records the Roman bound and its degree-sum derivation.
[Exact values for some unbalanced Zarankiewicz numbers](https://doi.org/10.1002/jgt.23068).

## Necessary conditions at height 44

Suppose \(a\in\{5,6\},\,b=10,\,h=44\) and the stack is box-free. In
(2) take \(s=2\). Since \(d=T/5\), we have \(F=T,\ \rho=1\), and
equality gives \(U=0,\ J_{p,c}=1\) for all \(p,c\). Thus every column
word is balanced, every \(m_{p,c}=88\), and every \(A_i=220\). For
each \(p,c\) the multiset of the forty-four \(k_\ell\)'s is exactly one
of the following.

- All forty-four values are two. The projected graph omits one of the
  45 pairs of columns.
- Forty-two values are two, one is one and one is three. All 45 pairs
  occur.

Indeed \(W\le1\) forces all values into \(\{2,3\}\) apart from at most
one value in \(\{1,4\}\), and their mean is two.

**A gap for six rows.** At least 37 layers of a hypothetical
\(6\times10\times44\) stack have exactly 30 monochromatic rectangles.
In a given layer write \(e_{p,c}=k_{p,c}-2\in\{-1,0,1\}\).
Balanced column words give \(\sum_{p,c}e_{p,c}=0\). The layer contains
\(30+\frac12\sum e_{p,c}^2\) rectangles. Let \(x_i\) be its \(i\)-th
row's red weight minus five, so \(\sum x_i=0\) and
\(e_{ij,R}-e_{ij,B}=x_i+x_j\). If some \(x_i>0>x_j\), summing
\(|x_i+x_k|+|x_j+x_k|\) over the other four rows gives at least eight,
hence \(\sum e_{p,c}^2\ge8\). Otherwise all \(x_i=0\). Then
\(e_{p,R}=e_{p,B}\) and the signed row-pair weights \(e_{p,R}\) sum to
zero around each vertex, since each red position of row \(i\) has two red
partners. Any nonempty support has at least four edges. Indeed its minimum
nonisolated degree is two, and a triangle cannot have opposite signs on
the two incident edges at all its vertices. Again \(\sum e_{p,c}^2\ge8\).
Each nonminimal layer therefore has at least 34 rectangles. Across the
stack at most \(30\cdot45\) slots are occupied versus the baseline
\(44\cdot30\), proving the claim.

**If all layers have 30 rectangles.** Each row pair and color omits one
column pair. Fix a column \(j\), write \(H_p\in\{0,1,2\}\) for the number
of these two missing edges incident with \(j\), and let \(d_p^j\) be the
Hamming distance of rows \(p\) down this column. Each agreement at \(j\)
uses one other column, so \(d_p^j=44-(18-H_p)=26+H_p\).
Since a \(3+3\) column word contributes nine disagreements,
\(\sum_p H_p=44\cdot9-15\cdot26=6\). The pairs with odd \(H_p\)
form the cut of the two parity classes of the six row weights at \(j\).
Its possible nonzero sizes are \(5,8,9\), inconsistent with an even
total of six. Thus \(H_p\) is even at every \(j\), and the red and blue
missing edges coincide for each \(p\).

Let \(F_j\) be the three row pairs whose common missing edge uses \(j\).
For each row, the sum of its distances to the other five rows is
\(3\cdot44=132=5\cdot26+2\). Thus \(F_j\) is a perfect matching.
Every pair of rows occurs in two of the ten matchings \(F_j\).

There are ten unordered \(3+3\) cuts of the rows. Let \(D_{p,S}\)
indicate whether cut \(S\) separates pair \(p\), and let \(n_S\) be its
frequency at column \(j\). The Gram matrix of these columns is
\(D^\mathsf{T}D=4I+5\mathbf J\), since a cut crosses nine edges and
two distinct cuts cross five common edges. Multiplying
\(Dn=26\mathbf1+2\mathbf1_{F_j}\) by \(D^\mathsf{T}\) gives
\(4n_S+220=234+2|\{p\in F_j:D_{p,S}=1\}|\).
Thus \(n_S=5\) when \(F_j\) crosses this cut three times and \(n_S=4\)
when it crosses once. A perfect matching has cuts of the first kind,
so an all-minimal stack of height 44 cannot be closed under global
color complementation, which would give even frequencies. These
conditions do not decide whether a general height-44 stack exists.

## Unavoidable boxes at height 45

Any binary \(5\times10\times45\) array contains at least seven boxes.
Any binary \(6\times10\times45\) array contains at least fourteen.

**Proof.** Put \(a=5\) or \(6\) and denote the box count by \(B\).
For each of the \(45T\) colored rectangle slots, let \(t\) be its
occupancy across layers. Set \(O=\sum(t-1)_+\), let \(L\) be the number
of empty slots, and put \(D=O-L\). Then
\(B=\sum\binom t2\ge O\ge D\). As above \(k\) is the number of agreeing
columns for a colored row pair in one layer, and \(e=k-2\). Summing
over all layers and colored row pairs gives \(\sum e=U\ge0\), since
\(10d=2T\). Comparing \(\sum\binom k2=45T+D\) with the expansion
of \(\binom{2+e}2\) yields \(\sum e^2=2D-3U\).

For each row pair \(p\) and column \(j\), write \(d_p^j\) for its
Hamming distance along 45 layers. The 18 slots of its two colors
involving \(j\) have total occupancy
\[
 \sum_{\text{18 slots}}t
 = (45-d_p^j)+\sum_{\text{agreements at }j} e.
\]
The sum on the right selects the corresponding row pair, layer and
agreement color. The triangle inequality therefore bounds
\(|d_p^j-27|\) by \(\sum_{\text{18 slots}}|t-1|
+\sum_{\text{agreements at }j}|e|\). On summing in \(j,p\), each
slot is counted twice and each \(e\) is counted \(k\) times. For an
integer \(e\ge-2\), \((2+e)|e|\le2e^2+e\); hence
\[
 \sum_{p,j}|d_p^j-27|
 \le 2(L+O)+2\sum e^2+U
 \le 4B+2D-5U.                                                     \tag{3}
\]

At a fixed column every pair of row words with the same weight parity
has even distance, and contributes at least one to the left side.
For five rows there are at least four such pairs per column, so
\(40\le4B+2D\le6B\), giving \(B\ge7\).

For six rows every column contributes at least six. If all its six-bit
words are balanced, the incident sum of the five distances at any row
is 135, so the incident sum of \(\delta_p=d_p^j-27\) is zero. At any
row an odd number of distances are odd, forcing both weight-parity
classes to have odd size. A \(1+5\) split gives at least ten units. For
a \(3+3\) split the six same-class pairs are two triangles. A total of
six would give \(\delta_p=\pm1\) on their edges and zero elsewhere,
inconsistent with zero incident sums. Since \(\sum_p\delta_p=0\), the
total absolute sum is even and at least eight. There are at most \(U\)
columns with some unbalanced six-bit word, each such word contributing
at least one unit of excess agreement. Thus the left side of (3) is
at least \(80-2U\), giving \(80+3U\le4B+2D\le6B\), or \(B\ge14\).
\(\square\)
