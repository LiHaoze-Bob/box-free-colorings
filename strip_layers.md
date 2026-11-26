# Rectangle multiplicity on strips of five and six rows

Write $\rho(m,n)$ for the least number of monochromatic rectangles in a binary $m\times n$ array. Alm and Miller ask when the convexity bound for this parameter is sharp. The following formula answers this for every width of the five- and six-row strips. [Alm and Miller, Problem 4](https://arxiv.org/html/2611.19635v1#S8)

**Theorem 1.** Let $m\in\{5,6\}$, $T=m(m-1)$ and $n=5q+r$, where $0\le r<5$. Then

$$\rho(m,n)=T\binom q2+\frac{T}{5}rq+\mathbf 1_{\{n\equiv 5\pmod {10}\}}\begin{cases}2&m=5,\\4&m=6.\end{cases}$$

For instance, on a strip of width 15 the two minima are 62 and 94. Both infinite exceptional residue classes have a strictly positive gap above the usual integer convexity bound.

## Lower bound and parity

For each row pair $i,j$ let $k_b$ be its number of columns agreeing in bit $b$. The total rectangle count is $R=\sum\binom{k_b}{2}$ over the $T$ colored row pairs. Put $S=\sum k_b$. A column with $a$ ones contributes $\binom a2+\binom{m-a}2$ to $S$, at least $d=T/5$ for these two heights. A balanced column attains this minimum. For integral $k$ we have $\binom k2\ge qk-\binom{q+1}2$, hence

$$ R\ge qdn-T\binom{q+1}2=T\binom q2+drq. $$

Now suppose $n=5q$ is odd. Write $s_i$ for the weight of row $i$. Since $k_1-k_0=s_i+s_j-n$, two rows whose weights have the same parity give an odd difference. At least four row pairs have this property when $m=5$, and at least six when $m=6$. In either case each such pair contributes at least one to the sum of squared deviations below.

$$ R=T\binom q2+(q-\tfrac12)(S-Tq)+\tfrac12\sum(k_b-q)^2. $$

This proves the extra two for $m=5$ and at least three for $m=6$. If a six-row column is unbalanced, $S>Tq$ and $q\ge1$, so the integer excess is at least four. Otherwise every column has three ones. Any two such columns have equal numbers of common ones and common zeros. Thus their red and blue rectangle counts are equal and $R$ is even. The base $30\binom q2$ is even as well, which gives the extra four.

## A common block for both heights

Use the ten columns of the following six-row block, numbered 0 through 9 from left to right. For height five delete the last row. The bit in row $i$ is the coefficient of $2^i$ in the column mask.

```
column   0   1   2   3   4   5   6   7   8   9
mask    35  26  22  49  38  21  13  44  11  56
```

One construction of the block starts with the edges of $K_5$ in lexicographic order. Put ones on the two endpoints for each edge of the cycle $(0,1,2,3,4)$, and on the three nonendpoints for each diagonal. Complete each column to three ones with the sixth entry. Every colored pair of rows occurs together in exactly two columns. For example, the intersection number of an adjacent pair of points is one cycle edge plus one disjoint diagonal. For a diagonal the corresponding count is two disjoint diagonals. Each row has weight five, so the same counts hold for zeros. A pair involving the sixth point occurs together in ones on the two incident cycle edges.

For $s=n\bmod 10$, take the columns in the table as a remainder block. The counts follow by summing the contributions of the at most 36 pairs of columns in each line.

| $s$ | Column indices | $R$ for five rows | $R$ for six rows |
|---:|:---|---:|---:|
| 0 | empty | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 2 | 0,1 | 0 | 0 |
| 3 | 0,1,5 | 0 | 0 |
| 4 | 0,1,5,7 | 0 | 0 |
| 5 | 0,1,2,3,6 | 2 | 4 |
| 6 | 0,1,2,3,6,7 | 4 | 6 |
| 7 | 0,1,2,3,4,6,7 | 8 | 12 |
| 8 | 0,1,2,3,4,5,6,7 | 12 | 18 |
| 9 | 0,1,2,3,4,5,6,7,8 | 16 | 24 |

Append $\lfloor n/10\rfloor$ whole blocks. Each block shifts every agreement count $k_b$ by two. Since all columns used are balanced, a shift from width $n$ to $n+10$ increases $R$ by $2dn+T$, exactly the increment in the claimed formula. The table proves all ten starting cases and completes the proof.

## Fixed height and large width

**Theorem 2.** For every fixed $m\ge3$, the gap between $\rho(m,n)$ and its integer convexity lower bound is bounded in $n$ and eventually periodic. In particular $\rho(m,n)$ is eventually a quadratic quasipolynomial.

*Proof.* Now put $T=m(m-1)$ and $d=\binom{\lfloor m/2\rfloor}2+\binom{\lceil m/2\rceil}2$. Let $B$ consist of every balanced binary column of height $m$ once, and set $P=|B|$. Row permutations and global color exchange preserve $B$ and act transitively on the types of colored row pairs. Thus every type occurs the same number $\lambda=dP/T$ of times. With $h=\lfloor dn/T\rfloor$, the integer convexity lower bound is

$$F(n)=h d n-T\binom{h+1}2.$$

Appending $B$ to any balanced array shifts all $k_b$ by $\lambda$, and increases the rectangle count by $\lambda dn+T\binom{\lambda}{2}$. This is also $F(n+P)-F(n)$, since the slope index $h$ increases by $\lambda$. For each residue modulo $P$ start from a fixed balanced array of that width and append blocks. This bounds the gap $\rho(m,n)-F(n)$ by a constant $C_m$ at all widths. An unbalanced column gives $S\ge dn+1$ and therefore $R\ge F(n)+h$. For $h>C_m$ every optimum uses only balanced columns. Appending $B$ to such an optimum shows that along each residue the nonnegative integer gap is eventually nonincreasing, hence eventually constant. Thus $P$ is an eventual period, possibly larger than the least one.

The finite block and the two strip formulas can be checked with `python3 check_strip_layers.py`. The all-width statements follow from the proofs above.
