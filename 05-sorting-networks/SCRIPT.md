---
INTRODUCTION
---

TODO: what are sorting networks
TODO: an example

---
SIMPLE ALGORITHMS
---

# BubbleSort
We'll use bubble sort as an example of a sorting network. It looks just as you'd think it should -- it gets the largest element to the last position by switching successive pairs of elements, like so.

Normally, we need about $\mathcal{O}(n^2)$ comparisons. However, by overlapping comparisons on non-overlaping elements, the depth of the sorting network is $\mathcal{O}(n)$!

---
BITONIC SORT
---

# Construction
This is nice, but we can do much better. One way is to use something called a bitonic sort.

---
PROOF
---

# Zero-one principle

# Proof

---
OPTIMAL SORTING NETWORKS
---

---
TESTING NETWORK CORRECTNESS
---

TODO: Co-NP-complete: https://link.springer.com/chapter/10.1007/978-3-662-25209-3_18
