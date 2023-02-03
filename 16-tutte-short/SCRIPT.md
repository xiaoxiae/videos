---
title: Undirected graphs can't equal a polynomial... right?
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
---

\hrule
\vspace{1.5em}

If I gave you this graph and told you to calculate all of its vertex colorings using $n$ colors, what would you do?

You could try to bruteforce the solution, but that would only work for smaller $n$s.
Instead, we can calculate what is called a chromatic polynomial for this graph.
If we plug in $n$ for any $x$, we get the exact number of colorings -- cool, right?

This, however, is just a form of the much more interesting Tutte polynomial.
This two-variate polynomial is fascinating because

- $x=1, y=1$ counts the number of spanning trees,
- $x=2, y=0$ counts the number of acyclic orientations

and much more -- it is used for measuring network reliability, for calculating linear codes and even has ties to quantum field theory. <!-- fade in more list -->

If you found this interesting and want to know more (like how to actually calculate it), I'd recommend you check out this neat handbook, written by many experts in the field, which contains a great overview of this polynomial's many fascinating uses.

In any case, thanks for watching!
