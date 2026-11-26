# Color-preserving involutions in an optimal stack

**Proposition.** In a box-free 52-layer stack on a $5\times7$ base, a color-preserving involution that interchanges two disjoint pairs of rows must interchange three disjoint pairs of columns.

Let $h$ be the involution and write $A,B$ for its two exchanged row pairs. A colored rectangle slot fixed by $h$ can be occupied only by an $h$-fixed layer. Indeed, the image of the layer uses the same slot, and a second occurrence would give a monochromatic box.

We use the following elementary accounting. In one layer let $k_{P,c}$ count the columns on which both rows of $P$ have color $c$, and let $R$ count the monochromatic rectangles. Then

$$
 R-8=\left(\sum_{P,c}k_{P,c}-28\right)
      +\sum_{P,c}\frac{(k_{P,c}-1)(k_{P,c}-2)}2.
$$

All terms on the right are nonnegative. A column with two or three ones contributes exactly four to $\sum k_{P,c}$, and every other column contributes at least six. Thus $R\le9$ requires every column to be balanced, with at most one pair $(P,c)$ having $k_{P,c}\notin\{1,2\}$. Over 52 layers the rectangle excess $\sum(R-8)$ and the number of unused colored slots sum to four.

If $h$ fixes every column, both row pairs in an $h$-fixed layer consist of identical rows. Each pair already contributes at least $\binom32+\binom42=9$ rectangles, exceeding the per-layer budget of 12 together. Yet $h$ fixes 84 colored slots, of which at most four may be unused.

If $h$ exchanges just one pair of columns, each of $A,B$ agrees in the five fixed columns in an $h$-fixed layer. Each therefore has some $k_{P,c}\ge3$, so $R\ge10$. There can be at most two fixed layers. The involution fixes $2\cdot2\cdot(1+\binom52)=44$ colored slots. The fixed layers and the unused slots together could account for at most $2\cdot8+4=20$ of them.

It remains to exclude exactly two exchanged column pairs $X,Y$. Call the eight colored slots on a row pair in $\{A,B\}$ and a column pair in $\{X,Y\}$ special. They are all fixed by $h$.

**Claim.** An $h$-fixed layer occupying a special slot has at least ten rectangles.

By relabeling, suppose $A\times X$ is red. The rows in $A$ agree in both columns of $X$ and in the three fixed columns. If $R\le9$, one of the two multiplicities on $A$ is at least three, using the entire allowance for exceptions to $k_{P,c}\in\{1,2\}$. Both multiplicities on $B$ must consequently be at most two. Agreement in either exchanged pair of columns would imply agreement in both its columns and would give $B$ at least five agreements, so the two rows of $B$ differ in each column of both $X$ and $Y$. The rows of $A$ differ in each column of $Y$ as well. Otherwise they would be identical, and for a pair of identical seven-bit rows the sum of the two quadratic terms in the display is at least four.

In each fixed column the rows of $A$ have one common color and the rows of $B$ have the opposite color, since the column is balanced. Thus the four row pairs having one row in $A$ and one in $B$ can have common blue entries only in $Y$. Each of its two columns supplies exactly one such incidence, whereas each of the four pairs requires at least one. This proves the claim.

Any layer that occupies a special slot is fixed and therefore costs at least two units of rectangle excess. At most two such layers occur. Each uses at most three special slots. Using four would require every one of the four uncolored blocks to be monochromatic, making the rows identical within both $A$ and $B$ throughout the layer and giving at least 18 rectangles. With at most one such layer, at least five special slots would be unused. With two, all four units of excess would be spent but at least two special slots would be unused. Both violate the budget. This proves the proposition.

## Consequences for automorphisms

Use here the injectivity of the row action and the bound $|G|\mid24$ proved in [the symmetry analysis](stack_symmetry.md).

- $G$ has no element of order four, with either action on colors. Its square would preserve colors, exchange two disjoint pairs of rows, and act on columns as the square of a permutation of order dividing four. On seven columns that square exchanges at most two pairs.
- $G$ contains no copy of $A_4$. Its Klein four subgroup would act by double transpositions on rows, because the sign character is trivial on $A_4$. The color character is trivial for the same reason. The proposition would make all three involutions fix exactly one column. Burnside's lemma would then give $(7+3)/4$ column orbits.
- No subgroup of order eight remains. Such a subgroup of $S_5$ with no order-four element would be elementary abelian. If it acts transitively on a four-point orbit, the action there is faithful and regular, forcing order four. Otherwise it preserves at most two two-point orbits, so it has order at most four.
- Consequently $|G|\le12$. In the order-12 case the row orbits must have sizes three and two. A four-point orbit would put $G$ in $S_4$ as its unique index-two subgroup $A_4$. With orbits of sizes three and two the row action identifies $G$ with $S_3\times S_2$.
- For a group containing a color-reversing element, the symmetry analysis gives $|G|\mid8$. Here $|G|\le4$, and the four-element action in the [52-layer certificate](5x7x52_klein_certificate.txt) attains that bound. In particular its exhibited Klein four group is its full automorphism group, for the row, column, layer and global-color symmetries under consideration.
