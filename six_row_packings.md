# Box-free stacks with six rows

We construct a $6\times9\times42$ coloring and a $6\times10\times40$ coloring. In both constructions each layer minimizes the number of monochromatic rectangles. The accompanying [verifier](verify_six_row_stacks.py) expands three binary seeds and tests every pair of layers on every colored row pair.

## The two constructions

The following ten triples on six points form a $2$-$(6,3,2)$ design. A column is identified with its six-bit integer, with row zero in the low bit. Index the ten columns by the two-element subsets of $\{0,1,2,3,4\}$ in lexicographic order.

| Pair | 01 | 02 | 03 | 04 | 12 | 13 | 14 | 23 | 24 | 34 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Column | 7 | 26 | 44 | 49 | 41 | 50 | 28 | 21 | 38 | 11 |

Each pair of rows belongs to exactly two triples, and likewise to two triple complements. Two design columns share two ones exactly when their index pairs are disjoint, as one can check from the table. They then also share two zeros. Thus the column pairs contributing rectangles are the fifteen edges of the Petersen graph $P=KG(5,2)$. Each of its edges supplies one red and one blue rectangle. Deleting any design column deletes its three incident edges and leaves 24 rectangles.

A seed below lists the design-column indices in the order they occupy the output columns. The indices run from 0 through 9 in the order of the table. A permutation of the five labels acts on the design-column indices by mapping each unordered pair. A permutation of the output positions moves each whole column to its image.

* For width nine use the seeds $(0,7,2,6,9,3,8,1,4)$ and $(0,1,3,5,6,8,9,7,2)$. Independently rotate the first seven output positions and cycle the labels $(0\ 1\ 2)$. Each seed has an orbit of length 21. The two orbits together use $42\cdot24=1008$ distinct colored rectangle slots.
* For width ten use the seed $(0,1,3,4,2,7,8,5,6,9)$. For $b\in\mathbb F_5$ and $t\in\mathbb Z/8$, act on the five labels by $x\mapsto 2^t x+b$, and rotate the first eight output positions by $t$. The last two positions are fixed. These forty images form a single orbit using $40\cdot30=1200$ distinct colored slots.

For a direct check, run `python3 verify_six_row_stacks.py`. Its generators act on the actual six rows and binary colors, and its seeds are explicit binary arrays.

## A restriction at height 44 in the single-design model

Assume all layers of a hypothetical $6\times10\times44$ stack are column permutations of the one labeled design above. Each layer is a bijection $f:V(P)\to V(K_{10})$. For an edge $e$ of $P$, its two colored row-pair labels each occur only at $e$ in the design. Thus box-freeness means that the 44 images $f(e)$ are distinct. Write $m(e)$ for the one edge of $K_{10}$ missing from this list.

**Proposition.** The ten target columns split into five pairs $M_0,\ldots,M_4$. Each edge $e$ of $P$ joins two disjoint pairs of source labels. If $i$ is the fifth source label, then $m(e)=M_i$. For a fixed target column in $M_i$, a source vertex is mapped there five times when its pair contains $i$ and four times otherwise.

**Proof.** Fix a target column $a$. Each layer contributes three edge incidences at $a$, since $P$ is cubic. Of the $15\cdot9$ possible incidences, $15\cdot9-44\cdot3=3$ are missing. Let $T$ be their three source edges and let $d$ be the degree vector of $T$ on $V(P)$.

Let $n_v$ count layers mapping $v$ to $a$ and put $x_v=n_v-4$. For each of the three edges at $v$, its images at $a$ total nine less its possible missing incidence. Summing gives $(3I+A)x=3\mathbf1-d$, where $A$ is the adjacency matrix of $P$ and $\sum_vx_v=4$. Adjacent vertices of $P$ have no common neighbor and nonadjacent distinct vertices have one. Hence $A^2=2I-A+J$. Multiplying by $2I-A$ gives $4x=\mathbf1-2d+Ad$.

At vertex $v$, $(Ad)_v\ge d_v$ because every incident edge has a neighboring endpoint. Since $d_v\le3$ and $x_v$ is integral, $x_v\ge0$. Where $d_v=0$, one has $x_v\ge1$. Three edges touch at most six vertices, so at least four have degree zero. The sum condition forces exactly four of them, with $x_v=1$ there and $x_v=0$ elsewhere. The original matrix equation shows that those four vertices are independent. Four pairwise intersecting two-subsets of five labels share a label $i$, since a pairwise-intersecting family without a common label is contained in a triangle. The remaining six vertices induce precisely the matching of three edges omitting $i$, and this matching must be $T$.

For any fixed $i$, the endpoints of $m(e)$ for any one edge omitting $i$ are exactly the target columns of type $i$. Thus there are two such columns and all three edges omitting $i$ miss the same pair. This proves the proposition.

**Symmetry consequence.** Within this model no stack of height 44 admits a symmetry of order two acting on source labels and target columns. Write the action as $(h,\tau)\in S_5\times S_{10}$ on the bijections. A nontrivial involution $h$ is a single or a double transposition. In either case some Petersen edge $e$ has both endpoints individually fixed by $h$, using the two disjoint source pairs $ab,cd$ for $h=(ab)$ or $(ab)(cd)$. An involution on ten columns fixes at least five target edges setwise. At most one of those edges is missing for $e$. The unique layer realizing any of the other fixed images of $e$ must be invariant under $(h,\tau)$. Hence $\tau$ acts on the ten columns with the same cycle type as $h$ acts on the ten source vertices, which has at least three transpositions. Each exchanged target pair is a fixed target edge. No invariant layer can map the individually fixed endpoints of $e$ to such an exchanged pair. This would leave at least three images missing for $e$. If $h$ is the identity and $\tau$ is nonidentity, an invariant bijection is already impossible. This argument applies to a family of permutations of one design and does not exclude a general height-44 stack.

The group can also contain no element of order three. A three-cycle on the five labels fixes two labels, hence fixes both columns of each of the associated target pairs individually. It fixes only one source vertex, the pair of the two fixed labels. Since 44 is not divisible by three, an action of order three on the layers has a fixed layer. Its bijection would identify actions with different numbers of fixed points. Finally, a pure target permutation fixing the design labels preserves each $M_i$ and therefore has order at most two. The group on the source and target labels thus embeds in $S_5$ and its order is divisible by neither two nor three. It is trivial or cyclic of order five.
