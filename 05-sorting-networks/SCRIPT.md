---
INTRODUCTION
---

# Introduction
Sorting networks are made of wires that transmit values, and comparators that compare and possibly swap those values, putting the larger value at the bottom of the comparator.

Here is an example of a sorting network, and an example computation on a sample input.

You might have noticed that since the computation seems to run in parallel on the entire network, we could make it faster by shifting the comparators such that they get executed at the same time, when they don't share the same wire.

We can think of this as the depth of the sorting network -- the number of layers of wires that get executed at the same time.

---
BUBBLE SORT
---

# BubbleSort
We'll use bubble sort as an example of a sorting network that we can generate for any number of wires. It repeatedly gets the largest element to the last position by switching successive pairs of elements.

We need about $\mathcal{O}(n^2)$ comparators in total, the same as regular bubble sort. However, by smartly overlapping comparators, the depth of the sorting network becomes $\mathcal{O}(n)$.

---
BITONIC SORT
---

# Construction
This is nice, but we can do better. One way is to use something called a bitonic sort.

It gets its name from bitonic sequences, which are the code idea behind this algorithm. They are sequences of numbers, such that they either increase and then decrease, or vice versa.

TODO: diagramy

The algorithm is built out of smaller building blocks called half-cleaners, that take a single bitonic sequence and split it into two bitonic sequences, where the values in one are less than or equal to the values in the other.

TODO: animace toho, na co se to splitne

It looks extremely simple, but it's not at all obvious why it should split a bitonic sequence into two.

TODO: dokončení konstrukce

# Zero-one principle
For proof, we will use something called the zero-one principle. It states that if a sorting network correctly sorts all sequences of 0's and 1's (of valid size), then it correctly sorts all sequences.

The proof is examining all possible sequences of 0's and 1's (TODO sort of):

Now for the actual construction -- we'll start with an unsorted sequence. We'll treat it as $n$ bitonic sequences and will use half-cleaners to sort them. However, we'll make each second one flipped, so that they TODO.

Now we repeat the same thing for the remaining $n/2$ bitonic sequences, again flipping 

TODO: animate flipping

---
OPTIMAL SORTING NETWORKS
---

A collection of sorting networks that are even better than bitonic sort are optimal sorting networks, either in the number of comparators or possible depth.

The following table captures the current limits for smaller inputs. notice that starting at ..., TODO že je to prostě těžký.

---
TESTING NETWORK CORRECTNESS
---

An interesting question is how hard the problem of deciding whether a network correctly sorts all inputs is. It turns out that it is co-NP. This means that we can check in polynomial time that the network doesn't sort, given an input that it sorts incorrectly. Unfortunately, a polynomial-time algorithm for finding such input is not currently known.

TODO: Co-NP-complete: https://link.springer.com/chapter/10.1007/978-3-662-25209-3_18

Luckily, we can use the zero-one principle and only try all sequences of 0's and 1's, instead of trying out all permutations, which makes a huge difference (although it's still exponential).

TODO: table
