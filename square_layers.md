# Minimum monochromatic rectangles in square binary arrays

Let $\rho(n,n)$ be the minimum number of monochromatic rectangles in a red-blue $n\times n$ array. Each rectangle consists of the four entries on two distinct rows and two distinct columns. We determine the following thirteen values.

| $n$ | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\rho(n,n)$ | 80 | 130 | 220 | 324 | 486 | 672 | 945 | 1248 | 1664 | 2124 | 2736 | 3400 | 4250 |

In graph terminology this is the two-color multiplicity of $C_4$ in $K_{n,n}$. Moon and Moser gave finite lower bounds in 1962. Erdős and Moon subsequently established the asymptotic density $1/8$ and recorded that the exactness of those finite bounds for $n\ge10$ was open in 1964. Rukmani and Vijayalakshmi gave explicit upper bounds for every order in 2015. [Moon and Moser](https://doi.org/10.1080/0025570X.1962.11975343) · [Erdős and Moon, p. 38](https://doi.org/10.4153/CMB-1964-003-8) · [Rukmani and Vijayalakshmi](https://doi.org/10.1016/j.akcej.2015.11.018)

Alm and Miller give exact diagonal entries through order 8, empirical upper bounds at orders 17–21, and $\rho(21,21)\ge4201$. The November 2026 OEIS record also lists the sequence through order 8. Our proof uses classical finite-field matrices and sequences alongside explicit small certificates. The comparison with these sources does not establish bibliographic priority for every value. [Alm and Miller, §§3 and 7](https://arxiv.org/html/2611.19635v1) · [OEIS A399620](https://oeis.org/A399620)

## 1. Lower bounds

Let $k_c(i,j)$ count the columns in which rows $i,j$ both have color $c$. Write $R$ for the rectangle count and $S$ for the sum of all $k_c(i,j)$. Then

$$R=\sum_{i<j,c}\binom{k_c(i,j)}2,\qquad S\ge n\left(\binom{\lfloor n/2\rfloor}2+\binom{\lceil n/2\rceil}2\right).$$

Indeed, a column with $a$ red entries contributes $\binom a2+\binom{n-a}2$ to $S$, minimized at a balanced split. For an integer $s\ge0$, the identity
$\binom k2-sk+\binom{s+1}2=(k-s)(k-s-1)/2$ gives

$$R\ge sS-n(n-1)\binom{s+1}2. \tag{1}$$

Equality in this affine estimate holds exactly when every colored row-pair count is $s$ or $s+1$.

**Even orders.** For $n=2m$, take $s=\lfloor m(m-1)/(n-1)\rfloor$. Equation (1) yields
$$\rho(n,n)\ge ns\,m(m-1)-n(n-1)\binom{s+1}2. \tag{2}$$

**Orders $4t-1$.** With $s=t-1$ in (1) we obtain
$$\rho(4t-1,4t-1)\ge\binom{4t-1}2(t-1)^2. \tag{3}$$

**Orders $4t+1$.** For every integer $t\ge1$,
$$\rho(4t+1,4t+1)\ge n(n-1)\binom t2+2t^2,\qquad n=4t+1. \tag{4}$$

*Proof.* There are $n(n-1)$ colored row pairs and $S\ge n(2t)^2=n(n-1)t$. Expanding each binomial coefficient around $t$ gives
$$R=n(n-1)\binom t2+(t-\tfrac12)\big(S-n(n-1)t\big)+\tfrac12\sum_{i<j,c}(k_c(i,j)-t)^2.$$

Let $r_i$ be the number of red entries in row $i$. Since $k_R(i,j)-k_B(i,j)=r_i+r_j-n$, integrality gives
$$ (k_R-t)^2+(k_B-t)^2\ge |k_R-t|+|k_B-t|\ge |r_i+r_j-n|.$$

Partition the rows according to whether $r_i\le 2t$ or $r_i\ge 2t+1$. Every pair within one part contributes at least one to the last sum. The smallest possible number of such pairs is $\binom{2t}{2}+\binom{2t+1}{2}=4t^2$. This proves (4).

## 2. Families attaining the bounds

We use signs $+1$ and $-1$ for red and blue. In a row pair of sign vectors $u,v$, their intersection counts are $(n+u\cdot v\pm(\sum u+\sum v))/4$. For an odd prime power $q$, let $\chi$ be the quadratic character of $\mathbb F_q$, extended by $\chi(0)=0$. Its basic correlation identity is
$$\sum_{x\in\mathbb F_q}\chi(x-a)\chi(x-b)=-1 \quad (a\ne b).$$
For $x\ne b$, the summand equals $\chi((x-a)/(x-b))$. The fractional linear map takes these $x$ bijectively onto the field with $1$ removed.

**Theorem 1.** Equation (4) is sharp whenever $q=4t+1$ is a prime power.

*Proof.* The Paley matrix $Q_{ij}=\chi(i-j)$ is symmetric, has zero row and column sums, and has distinct row inner products $-1$. Insert signs $d_i$ on its diagonal, using $2t$ of one sign and $2t+1$ of the other. Each row and column now has sum $d_i$ at index $i$, so the lower bound on $S$ is exact. For $i\ne j$ the new row dot product is $-1+(d_i+d_j)Q_{ij}$. If $d_i=-d_j$, both colored counts equal $t$. When $d_i=d_j$, one count equals $t$ and the other differs from $t$ by one. Thus the total squared deviation is precisely the $4t^2$ pairs with equal diagonal signs. Equation (4) follows with equality. [Paley, *On Orthogonal Matrices* (1933)](https://doi.org/10.1002/sapm1933121311)

**Theorem 2.** Equation (3) is sharp whenever there exists a Hadamard matrix of order $4t$. In particular it is sharp whenever $q=4t-1$ is a prime power.

*Proof.* Normalize the first row and column of the Hadamard matrix to $+1$, then delete them both. Every remaining row and column has sum $-1$, and distinct row dot products are $-1$. Their two colored counts are therefore $t-1$ and $t$, attaining (3). In the prime-power case there is a direct construction. The character matrix $Q_{ij}=\chi(i-j)$ is skew-symmetric. Filling the diagonal with $-1$ retains all distinct row dot products $-1$ and gives the required row and column sums. [Paley (1933)](https://doi.org/10.1002/sapm1933121311)

**Theorem 3.** Equation (2) is sharp whenever $n=q-1$ with $q$ an odd prime power.

*Proof.* On $\mathbb F_q^\times$ put $f(x)=\chi(x+1)$ except that $f(-1)=1$. Each row $u_a=(f(ax))_{x\ne0}$ has sum zero, and the same holds for columns. This is the binary Sidel'nikov sequence and its multiplicative shifts. To check its correlation directly, let $b\ne0,1$. Summing the unmodified product $\chi(x+1)\chi(bx+1)$ over the field gives $-\chi(b)$. Remove the term $1$ at $x=0$, then restore the two contributions at $x=-1,-1/b$ where the zero character values were changed. The result is
$$u_1\cdot u_b=-\chi(b)-1+\chi(1-b)(1+\chi(-b)).$$
For $q\equiv1\pmod4$ this belongs to $\{0,-4\}$. For $q\equiv3\pmod4$ it belongs to $\{-2,2\}$. The dot product for $u_a,u_{a'}$ uses $b=a'/a$. Since each row is balanced, its pair's two colored counts both equal $(n+u_a\cdot u_{a'})/4$. These are $s$ or $s+1$ for the slope in (2) (the case $q=3$ follows directly). All conditions for equality now hold. [Sidel'nikov, *Some k-Valued Pseudo-random Sequences and Nearly Equidistant Codes* (1969)](https://www.mathnet.ru/eng/ppi1781)

## 3. Finite certificates

The three theorems cover every order in the table except 14, 20 and 21. For order 15 use the Sylvester matrix of order 16, $H_{ij}=(-1)^{i\cdot j}$ with indices in $\mathbb F_2^4$. For the three remaining orders the following arrays realize the lower bounds. Each shift below moves the indicated blocks one position to the right, wrapping around within each block.

- **Order 14.** Rotate the two consecutive blocks of seven in each of the strings `11010001110100` and `11101001000101` simultaneously to obtain two orbits of seven rows. For 70 row pairs the colored counts are $(3,3)$, and for the other 21 they are $(4,4)$.
- **Order 20.** Take the twenty cyclic shifts of `11111010100100110000`. There are 50 row pairs with counts $(4,4)$ and 140 with counts $(5,5)$.
- **Order 21.** Split the columns into four consecutive blocks of five and one fixed column. Develop the following four seed rows by five simultaneous cyclic shifts and append the fixed row on the last line.

```text
11001 00101 00101 10001 1
00101 00011 00111 01010 1
10011 01010 10101 11100 0
11010 11100 00111 01010 0
00000 11111 00000 11111 1
```

For order 21 the unordered pair of counts is $(5,5)$ on 110 row pairs, $(4,5)$ on 50 and $(5,6)$ on 50. Thus the rectangle count is $110\cdot20+50\cdot16+50\cdot25=4250$. The seed rows were found by minimizing the rectangle count over arrays with the prescribed order-five symmetry.

All thirteen colorings are implemented in [check_square_layers.py](check_square_layers.py). Running `python3 check_square_layers.py` checks their dimensions, examines every pair of rows and columns directly, and compares each count with its lower bound.

**Corollary.** Every two-coloring of the $21\times21\times21$ cube contains at least $1050$ monochromatic boxes.

*Proof.* Its 21 layers contain at least $21\cdot4250$ colored rectangles. If one colored position occurs $h$ times, it yields $\binom h2\ge h-1$ monochromatic boxes. Summing over $2\binom{21}2^2=88200$ colored positions gives $21\cdot4250-88200=1050$. This improves the bound of 21 in [Alm and Miller, §7.2](https://arxiv.org/html/2611.19635v1#S7.SS2).
