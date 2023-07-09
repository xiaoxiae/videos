---
title: The real difference between BFS and DFS
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \usepackage{todonotes}
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=70mm, top=15mm, bottom=15mm, marginparwidth=60mm}
- \newcommand{\fix}[1]{\todo[color=green!40]{#1}}
- \newcommand{\note}[1]{\todo[color=blue!40]{#1}}
---

\hrule
\vspace{1.5em}

Have you ever wondered what the true difference between BFS and DFS is?

Well I have and I wanted to visualize them on the same maze to see what they're really doing.

Running BFS, it goes layer by layer, always exploring tiles that are nearest from the start.

DFS, on the other hand, wonders away, always exploring tiles nearest to where it currently is.

Plotting which of the algorithms get to a certain tile first visualizes this quite nicely and makes for a pretty cool poster.

Make sure to keep this in mind when deciding which one to use and, if you'd like to learn more, check out my video about searching the state space.

In any case, thank you for watching!
