---
title: <title>
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
---

\hrule
\vspace{1.5em}

Imagine there are $n$ houses on a grid, each of which contains some number of people.
Since they're all friends, they would like to find a nice place to meet up and that requires the least amount of total steps.
How can we find this place efficiently?
Pause here for a second and think about how we could do this.

To solve the problem, there are three key observations that we have to make.

The first one is that the $x$ and $y$ coordinates of the meeting place are independent -- moving horizontally doesn't change the vertical distance the people have to make.
This splits our problem into two, 1D versions of the problem.
