# Automorphisms of extremal 52-layer stacks

An automorphism of a box-free binary $5\times7\times52$ coloring consists of permutations of rows, columns and layers, with an optional global color interchange. Denote the resulting group by $G$. We prove that the projection $G\to S_5$ on the row labels is faithful and $|G|$ divides $24$. If any automorphism interchanges colors, then $|G|$ divides $8$. The additional restriction on double transpositions gives $|G|\le12$ in general and $|G|\le4$ in the color-interchanging case. [Involution obstruction](involution_obstruction.md)

## Counting identities

For a row pair $p$ and a color $c$, let $k$ count their common columns of that color in one layer. Put $w(k)=(k-1)(k-2)/2$. Let $W_p^c$ be the sum of $w(k)$ over the 52 layers, and $L_p^c$ the number of unused column pairs in color $c$ on rows $p$. Every used colored slot occurs exactly once. Define $J_p=\sum_c(W_p^c+L_p^c)$. All terms are nonnegative integers.

A five-entry column containing $a$ red cells contributes $f(a)=\binom a2+\binom{5-a}2$ common row pairs. The minimum is four, with excess two for a singleton minority and six for a monochrome column. Let $U$ be the sum of $f(a)-4$ over the 364 columns of the stack. From $\binom k2=k-1+w(k)$, the rectangle count in each layer is eight plus its column excess and the sum of its $w(k)$. Subtracting from the capacity of 420 slots gives
$$\sum_p J_p+U=4. \tag{1}$$
In particular, each layer has between eight and twelve rectangles. Any set of $h$ layers together with all unused slots accounts for at most $8h+4$ slots.

Treat the five rows as binary words of length 364. For a fixed pair $p$, summing $\binom k2=k-1+w(k)$ over the two colors and all layers gives $42-\sum_c L_p^c=\sum k-104+\sum_c W_p^c$. Its Hamming distance is therefore
$$d_p=364-\sum k=218+J_p. \tag{2}$$

## Faithful action on rows

First suppose that an automorphism fixes all row labels and interchanges colors. It permutes the 364 individual column positions, indexed by column and layer. Every cycle has even length since its five-bit word alternates with its complement. Select alternate positions on each cycle. For each row pair the distance on the resulting 182 positions is exactly $d_p/2=109+J_p/2$. Thus every $J_p$ is even, and (1) shows that at least eight of the ten half-distances are odd. In any set of five binary words, odd distance requires opposite weight parity. At most $2\cdot3=6$ pairs have opposite parity. This excludes the automorphism.

The color-preserving kernel of the row action injects into $S_7$ through the column labels. Indeed, if both coordinate permutations are trivial, every layer is preserved because the layers are distinct. Two identical layers would repeat a colored rectangle. A nontrivial kernel would contain an element of prime order $2,3,5$ or $7$.

- An involution on columns with $b$ transpositions has $20(b+\binom{7-2b}2)\ge60$ fixed colored slots. Each occupied fixed slot belongs to a fixed layer by uniqueness. In each fixed layer, the words at a transposed column pair coincide. They use at least four of the same twenty slots available on that pair. Consequently there are at most five fixed layers, which with all unused slots can account for at most 44 slots.
- For odd prime order $3,5$ or $7$, at least one layer is fixed since that prime does not divide 52. Such a layer has at least three identical columns. These contribute at least twelve rectangles by themselves. To avoid a thirteenth, their common five-bit word must be balanced. In its three majority rows, each of the other four columns may have at most one entry of the majority color, as otherwise it forms another rectangle with a repeated column. These four columns each contain an opposite-colored pair on those three rows. Two must use the same row pair, giving another rectangle.

This proves faithfulness. An element of order five must now act as a five-cycle on rows. It preserves colors and fixes at least one layer. It also fixes at least two column labels. On a fixed layer the word in any such column is invariant under a five-cycle and hence monochrome, contributing excess six to (1). Cauchy's theorem and Lagrange's theorem now imply that $|G|$ divides 24.

## Color-interchanging symmetries

Assume an element interchanges colors. If $A_i$ is the red weight of the full row $i$, put $a_i=A_i-182$. Summing the single-layer identity $k_R-k_B=r_i+r_j-7$, where $r_i$ is the red weight of row $i$ in the layer, gives

$$ a_i+a_j=L_p^B+W_p^B-L_p^R-W_p^R,\qquad |a_i+a_j|\le J_p. $$

All entries split equally between the colors, so $\sum_i a_i=0$. If $a_i\ge1$ and $a_j\le-1$, summing $|a_i+a_h|+|a_j+a_h|\ge a_i-a_j$ over the three remaining rows $h$ gives at least six, violating (1). Hence every full row has red weight 182. The displayed identity gives $L_p^B+W_p^B=L_p^R+W_p^R$. Put $j_p=J_p/2$. It is a $G$-invariant, nonnegative integer function with sum at most two.

Let $g$ interchange the colors and have row permutation $\tau$. Its action on individual column positions has only even cycles, since the weight of the five-bit column word alternates between $a$ and $5-a$. Again choose alternating positions from each cycle. If $h_i$ is the red weight of the restricted row $i$, the full weight of row $i$ is $h_i+182-h_{\tau^{-1}i}$. It follows that $h_i=h_{\tau^{-1}i}$. For any row pair $p$ fixed as a set by $\tau$, its restricted distance is $109+j_p$ by (2). This distance has the same parity as the sum of the two restricted row weights.

- For $\tau=(12)$, $h_1=h_2$ forces $j_{12}$ odd. The restricted distances on the triangle with vertices $3,4,5$ sum to an even integer, so the sum of $j_p$ on that triangle is odd. Thus $j$ consists of the edge $12$ and one edge among $3,4,5$, each of weight one.
- For $\tau=(12)(34)$, the fixed pairs $12,34$ both have even restricted distances. Hence $j$ consists precisely of those two edges.
- For $\tau=(1234)$, the sole row-pair orbit of size less than four is the pair of diagonals $13,24$. Invariance implies that $j$ is zero or consists precisely of these diagonals.

A color-interchanging automorphism has even order. Its row action has that same order by faithfulness. A row permutation of order six has a cube that is a color-interchanging transposition. Thus whenever $j$ is nonzero the whole group preserves a matching of two disjoint edges in $K_5$, whose stabilizer has order eight.

It remains to consider $j=0$. In this case each color-interchanging element has row order four. If three divided $|G|$, the row action would be intransitive since five does not divide $|G|$. A four-cycle then forces a four-point orbit and one fixed point, so $G\le S_4$. Its order would be 12 or 24. The unique index-two subgroup of $S_4$ is $A_4$, which has no four-cycle. If $G=S_4$, its nontrivial color character is the sign character and some transposition interchanges colors. These contradictions exclude three, again giving $|G|\mid8$.

In the [52-layer certificate](5x7x52_klein_certificate.txt), every row has red weight 182. The matching consists of row pairs $12$ and $34$ in one-based numbering. Each of its two edges has one unit of $W^R$ and one unit of $W^B$. Every slot is used exactly once. The full automorphism group of this particular coloring is the Klein four-group. To check this finite assertion, let $S$ be the set of its 52 binary matrices. For each of the eight row permutations preserving the matching, each of the $7!$ column permutations and each color choice, apply the resulting map to every matrix and retain it exactly when all images belong to $S$. The four resulting maps in one-based cycle notation are shown below. The action on layers is uniquely determined by the other coordinates.

| Row permutation | Column permutation | Color action |
|---|---|---|
| identity | identity | preserve |
| $(12)$ | $(12)(34)(56)$ | interchange |
| $(34)$ | $(13)(24)$ | interchange |
| $(12)(34)$ | $(14)(23)(56)$ | preserve |

When $j$ is a matching, (1) implies that all columns are balanced. All unused slots and all terms $w(k)>0$ must lie on the two row pairs of the matching, with a budget of two on each. The alternative $j=0$ would require a color-interchanging element of order four, excluded by the [involution obstruction](involution_obstruction.md). Thus every extremal stack with a color-interchanging symmetry has balanced columns and a distinguished matching.
