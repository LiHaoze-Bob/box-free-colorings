# Row cuts for partial stacks at height 53

Write a *slot* for a row pair, a column pair and a bit. A minimum layer
occupies eight slots. A four-box stack uses every slot once and doubles
one slot on each of the four row pairs inside the two weight classes
of sizes two and three. Write $\delta_{ij}=1$ on those four pairs and
zero elsewhere. The total demand on row pair $ij$ is $42+\delta_{ij}$.
The two global row weights are 185 and 186.
[Equality conditions](first_forced_height.md)

There is also a convenient converse for searches. A stack of 53 minimum
layers that covers all 420 slots has four boxes. Indeed there are just
four excess incidences. If $w_i$ is the global row weight, the difference
of the two color totals on $ij$ is $w_i+w_j-371$. This difference is odd
on at least four pairs. Each requires its own excess incidence, so all
four excesses are distinct doubles. Thus a search may use only coverage
constraints once it enforces the minimum on every layer.

## A family of residual inequalities

In a minimum layer every colored row pair agrees in one or two columns.
Its number of rectangles is the agreement count minus one.
If $v_i$ is a single row's weight, the difference of the two colored
counts is $v_i+v_j-7$, lying in $\{-1,0,1\}$. Every row has weight
three or four. In fact, if one row had weight at most two, the other
four would each have weight at least four. Their pair sums are at most
eight, so all four have weight four and the first has weight two.
All ten row pairs would then have a nonzero color difference and would
supply at least ten rectangles. Complementing the layer excludes
weights of at least five.

Consider a partial stack with $n$ layers left to choose and let $t_{ij}$
be the outstanding uncolored demand on $ij$. For each row $i$ let $a_i$
be the number of the remaining layers where its weight must be four.
It equals the target weight of row $i$ minus its retained weight minus
$3n$. An $a_i$ outside $[0,n]$ already rules out completion.

**Proposition.** In any completion there are five binary words of length
$n$, of weights $a_i$, whose pairwise Hamming distances satisfy
$$
 |t_{ij}-n|\le d_{ij}\le \min(a_i+a_j,\,2n-a_i-a_j).
$$
Consequently for any nonnegative weights $\lambda_{ij}$,
$$
 \sum_{i<j}\lambda_{ij}|t_{ij}-n|
 \ \le\ n\max_{S\subseteq[5]}\sum_{|\{i,j\}\cap S|=1}\lambda_{ij}.
$$

To prove it, record a one in word $i$ whenever row $i$ has weight four.
If the two recorded bits agree, the rows have weights $(3,3)$ or
$(4,4)$, the two color counts differ by one, and the pair supplies
exactly one rectangle. If the bits differ the counts are equal and
the pair supplies zero or two rectangles. Only the $d_{ij}$ differing
bits can move $t_{ij}$ away from $n$. The upper bound is the maximum
Hamming distance at the given word weights. Each coordinate of the
five words cuts the row set in two, proving the weighted inequality.
In particular, for any three rows the sum of their three deviations
$|t_{ij}-n|$ is at most $2n$.

## A 42-layer obstruction without a symmetry hypothesis

**Theorem.** No four-box stack contains 42 layers in which the
rectangle count on each of the 20 colored row pairs is a multiple of
seven. In particular it cannot contain six disjoint groups of seven
layers with constant colored row-pair counts within each group. The
groups may have different profiles and different column actions.

Let $u_i$ be the total weight of row $i$ in the 42 retained layers.
Subtracting the two color counts gives $u_i+u_j-7\cdot42\equiv0\pmod7$.
Using any three rows gives $2u_i\equiv0\pmod7$, so every $u_i$ is a
multiple of seven. Each of the eleven remaining layers contributes three
or four to each row weight. The only multiple of seven compatible with
185 or 186 after these contributions is 147. Thus the two retained
color counts are equal on every row pair.

A colored row pair has final count 21 or 22 and can gain at most eleven.
Its retained count must therefore be 14 or 21. Of the ten row pairs,
exactly four have count 21 in both colors, since the retained layers
contribute $42\cdot8=336$ incidences. Call these four edges saturated.
Their residual demands are zero or one, giving deviation at least ten
from the mean of eleven. On every other edge the demand is 14 or 15,
giving deviation at least three. Two incident saturated edges would
therefore give a triangle with total deviation at least $10+10+3=23$,
exceeding $2\cdot11=22$. Four edges on five vertices cannot be a
matching. This proves the theorem.

## Searching first for uncolored rectangles

Every minimum layer is determined up to global color exchange by the
eight geometries of its rectangles. Here a geometry consists of the
row pair and the column pair alone. To verify the assertion, fix one
of the six minimum-layer representatives. Try both possible colors on
each of its eight geometries and list the minimum layers containing
these signed slots. For each of the six representatives the only two
results are the representative and its complement.
[Reconstruction and orientation checker](check_layer_orientations.py)

This gives exactly 2,192,400 different geometric supports. A search
can select a multiset of them first, retaining a single flip variable
$x_i$ for each occurrence $i$. Fix four proposed doubled slots in
the prescribed pattern. An ordinary geometry may occur at most twice,
and an exceptional one at most three times. If an ordinary geometry
occurs in candidates $i,j$ with reference colors $a,b$, its two slots
are compatible precisely when
$$
 x_i\mathbin\oplus x_j=1\mathbin\oplus a\mathbin\oplus b .
$$
Propagating these equations on a graph either finds an inconsistent cycle
or fixes all flip bits up to one common choice per connected component.

Only components meeting one of the four exceptional geometries with
at least two occurrences can still impose a constraint. There are at most
twelve such components. Try their flip bits and count the two colors
at each exceptional geometry, with capacities two in the designated
color and one in the other. All untouched components can take either
orientation. This decides *exactly* whether an arbitrary partial
selection respects the colored capacities. With 53 layers the total
demand and capacity both equal 424, so feasibility of these tests
already produces a four-box coloring. For a shorter partial selection
a failed test certifies that no extension to the prescribed target exists.
