---
title: What does this C program do?
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

\marginpar{\texttt{Intro}}
What does this C program do?

If we run it, the `main` function calls the `f` function with values 61 and 25, printing their sum of 86... but how?

Looking closely at the `f` function, we see that it is recursive.
While `y` isn't zero, it performs binary operations on the numbers and calls itself, finally returning `x` once `y` reaches zero.

To see why it adds the numbers, let's see what the binary operations do.
For the first parameter, it calculates bitwise xor, getting ones where exactly one of the numbers has a one bit.
For the second, it calculates bitwise and, getting ones where both of the numbers have a one bit, and shifts the number to the left.

If you think about these two operations, it is actually exactly how long addition works if we were to do it all at once -- the first number is the part of the numbers we can cleanly add and the second is the carry.

The recursion runs until the carry is zero and the sum is completed.

# TODO: run the recusion on the adding until we're done
