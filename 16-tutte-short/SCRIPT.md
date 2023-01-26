---
title: <title>
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
---

\hrule
\vspace{1.5em}

If I gave you a graph and told you to calculate different ways of coloring its vertices such that adjacent vertices have different colors, what would you do?

You could just bruteforce the solution but that's too boring.
Instead, we'll calculate what is called a chromatic polynomial for this graph.
If we plug in $n$ for any $x$, we get the exact number of colorings -- cool, right?

This, however, is just a specialized form of the much more interesting Tutte polynomial.
This two-variate polynomial is fascinating because

- $x=1, y=1$ counts the number of spanning trees,
- $x=2, y=0$ counts the number of acyclic orientations

and much more -- it is used for measuring network reliability, for calculating linear codes and even has ties to quantum field theory.

If you found this interesting, I'd recommend you check out this neat handbook, written by many experts in the field, which contains a great overview of this polynomial's many fascinating uses.
