---
title: <title>
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
---

\hrule
\vspace{1.5em}

If I gave you a graph and told you to calculate all of its vertex colorings using $n$ colors, what would you do?

You could just bruteforce the solution but that's too boring.
Instead, we'll use this crazy equation to calculate what is called a Tutte polynomial for this graph.
If we now plug in $n$ for $x$ and $0$ for $y$, we get the exact number of colorings.

Neat, right?
But that's not all:

- $x=1, y=1$ counts the number of spanning trees,
- $x=1, y=2$ counts the number of spanning subgraphs,
- $x=2, y=0$ counts the number of acyclic orientations

it is also used for simulating network failures, modelling behavior of ferromagnets, calculating the number of nowhere-zero flows... it's useful.

The general idea of why it is so powerful is that it contains information regarding the number of connected components for all of its edge subsets, which turns out to be sufficient for calculating all of the things I mentioned before.
