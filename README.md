# The maximum height of a box-free 5 × 7 grid

**The exact value is $N(5,7)=52$.** This repository contains an explicit red-and-blue coloring of the $5\times7\times52$ grid with no monochromatic box. It attains the upper bound of Alm and Miller and disproves their conjecture that the maximum is 50. [Alm and Miller, §6](https://arxiv.org/html/2611.19635v1#S6)

[Read the short paper (PDF)](paper/box-free.pdf) · [LaTeX source](paper/box-free.tex) · [52-layer certificate](5x7x52_klein_certificate.txt) · [Verification program](verify_klein_52.py)

## Exact box counts beyond the threshold

The [companion paper (PDF)](paper/multiplicities.pdf) gives proofs and constructions for the minimum number of monochromatic boxes. [LaTeX source](paper/multiplicities.tex)

* In a binary grid with three or four rows, every minimum box count reduces to a six-color rectangle minimum. An equitable matching construction determines the latter at all heights for a general palette of $c$ colors and any width from $c$ through $2c$. Thus $N(3,b)=N(4,b)$ for every width. For widths 7 through 12 their common values are 126, 84, 72, 67, 66 and 66. [Proof, construction and prior results](short_slices.md)
* On the $5\times7$ base, write $8h=420q+e$ with $0\le e<420$. For every positive height except possibly 53, the minimum is $420\binom q2+eq$, plus exactly two boxes when $h\equiv105\pmod{210}$. At the first exceptional residue, $h=105$, the minimum is exactly 422. A uniform 210-layer block extends the finite construction indefinitely. For an arbitrary fixed base and palette the eventual correction to a quadratic is a periodic squared lattice distance. [Finite certificate](verify_height_multiplicity.py)
* At the first forced height on the original base, $4\le B(53)\le5$. Four boxes would force a prescribed triangle and edge of doubled row pairs and an automorphism group of order at most two. [Proof](first_forced_height.md) · [Five-box witness](verify_first_forced.py)
* At widths nine and ten, colored row-pair projections exclude the nominal packing height of 45. For both five and six rows the certified ranges are $42\le N(a,9)\le44$ and $40\le N(a,10)\le44$. At height 45 and width ten, at least seven and fourteen boxes are forced for five and six rows respectively. [Projection inequalities](projection_bounds.md) · [Six-row constructions and the Petersen graph](six_row_packings.md)

Run the following checks from the repository root with Python 3.9 or later.

```sh
python3 check_short_slices.py
python3 verify_height_multiplicity.py
python3 verify_six_row_stacks.py
python3 verify_affine_stacks.py
python3 verify_first_forced.py
```

## The construction

Two rows, two columns and one color specify a colored rectangle position. There are $2\binom52\binom72=420$ such positions. A stack is box-free precisely when no position occurs in two layers. Each layer contains at least eight monochromatic rectangles, giving an upper bound of $\lfloor420/8\rfloor=52$ layers.

Two commuting permutations of the rows and columns, each coupled with a color exchange, generate the construction from 15 seeds. Four seed orbits have size two and eleven have size four. Of the resulting 52 layers, 48 contain eight rectangles and four contain nine. They use all $48\cdot8+4\cdot9=420$ positions exactly once. The paper lists every seed and gives a disjoint partition of the 108 position orbits. The full automorphism group of this coloring is the Klein four-group.

Run the following with Python 3.9 or later. The checker expands the seeds, verifies that its output matches the supplied certificate, checks every layer's rectangles, and rejects any repeated colored position.

```sh
python3 verify_klein_52.py
```

The discovery search can also be reproduced from scratch with a C++17 compiler. It uses only the standard library, a fixed shuffle seed and an exact-cover search. It enumerates 737,124 distinct candidate supports and finds the displayed solution after 19,307 search nodes.

```sh
c++ -O3 -std=c++17 search_klein_52.cpp -o /tmp/search_klein_52
/tmp/search_klein_52
```

## Further results

| Result | Proof or data | Verification |
| --- | --- | --- |
| A second construction gives 51 layers in nine orbits of a cyclic group of order six. | [51-layer certificate](5x7x51_cyclic_certificate.txt) | [Cyclic construction and checker](verify_cyclic_51.py) |
| Row weights and automorphisms of extremal stacks satisfy additional parity and fixed-position restrictions. | [Row action and defect counts](stack_symmetry.md) · [Involutions](involution_obstruction.md) | The main paper gives a direct proof for the displayed 52-layer coloring. |
| Exact rectangle minima on $5\times n$ and $6\times n$ for every $n$, and eventual quasipolynomiality at each fixed height. | [Strip formulas and proofs](strip_layers.md) | [Finite block checker](check_strip_layers.py) |
| Exact square-layer rectangle minima for orders 9 through 21. In particular $\rho(21,21)=4250$, implying at least 1050 monochromatic boxes in every two-coloring of the $21^3$ cube. | [Square-array bounds and constructions](square_layers.md) | [Square certificate checker](check_square_layers.py) |

```sh
python3 verify_cyclic_51.py
python3 check_strip_layers.py
python3 check_square_layers.py
```

## Earlier experiments and the original 50-layer coloring

The included [50-layer coloring](5x7x50_exact_zero_certificate.txt) comes from [Alm and Miller's repository](https://github.com/algorithmachine/box-free-colorings/blob/main/5x7x50_exact_zero_certificate.txt). It has 400 occupied positions and no box. Exhaustive local searches found no way to increase its height by deleting at most six layers and replacing them with one more than the number removed. The six-deletion check covers all $\binom{50}{6}=15{,}890{,}700$ choices. The independent 51-layer cyclic certificate also admits no such exchange through six deletions, covering $\binom{51}{6}=18{,}009{,}460$ choices at radius six. These statements concern the particular certificates supplied here.

For individual $5\times7$ layers, exactly 900 column multisets attain the minimum of eight rectangles. Permuting rows and globally exchanging colors groups them into six classes of sizes 60, 120, 120, 120, 240 and 240. Column positions still matter when copies are used in a stack.

```sh
python3 check_box_layers.py 5x7x50_exact_zero_certificate.txt
python3 check_two_deletions.py
python3 classify_minimal_layers.py
c++ -O3 -std=c++17 check_exchange_radius.cpp -o /tmp/check_exchange
/tmp/check_exchange 5x7x50_exact_zero_certificate.txt 6
/tmp/check_exchange 5x7x51_cyclic_certificate.txt 6
```

The general grid-box problem was studied by [Cooper, Fenner and Purewal, *Monochromatic Boxes in Colored Grids*](https://doi.org/10.1137/080740702).
