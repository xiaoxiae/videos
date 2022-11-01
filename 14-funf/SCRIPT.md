---
title: What does this weird C program do?
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

Here is a weird C program that calculates the sum of two numbers -- can you figure out how it works?

Looking closely at the `f` function that does the calculation, we see that it is recursive.
While `y` isn't zero, it performs binary operations on the numbers and calls itself, finally returning `x` once `y` reaches zero.

To see why it adds the numbers, let's see what the binary operations do.
For the first parameter, it calculates bitwise xor, getting ones where exactly one of the numbers has a one bit.
For the second, it calculates bitwise and, getting ones where both of the numbers have a one bit, and shifts the number to the left.

If you think about these two operations, it is actually exactly how long addition works if we were to do it all at once -- the first number is the bits we can cleanly sum without carrying and the second is the bits we have to carry to the left.

The recursion runs until the carry is zero and the sum is complete.

Thanks for watching!
