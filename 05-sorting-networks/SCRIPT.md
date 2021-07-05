---
INTRODUCTION
---

# Introduction
Sorting networks are made of wires that transmit values, and comparators that swap the values so that the larger value is at the bottom and the smaller is at the top.

Here is an example of a sorting network and a computation on a sample input.

You might have noticed that the computation runs in parallel on the entire network. It is therefore reasonable to think about groups of comparators that get executed at the same time as layers of this network. Each wire in a given layer must have at most one comparator attached to it, because attempting to swap a single wire (TODO: animation of different layout that breaks this) using with two comparators at the same time would yield undefined results.

In the visualization, they aren't really executed at the exact same time, because they would overlap and the visualization wouldn't be clear. (TODO: mesh them even closer together) Instead, the layers are indicated by the spacing between comparators.

Having defined layers, we could also reasonably define the depth (or the running time) of the network as the number of layers, since it directly corresponds to how fast the network is at sorting an input.

# Oriented comparators
The comparators that we described earlier always put the larger value at the bottom. However, we could alternatively define them as having an orientation and placing the larger value depending on their orientation.

Notice, however, that these models are (excluding some edge cases) equivalent, so we'll use them interchangeably. By equivalent, we mean that we can convert any non-oriented network to an oriented one and vice-versa.

---
BUBBLE SORT
---

# BubbleSort
We'll use bubble sort as an example of a sorting network that we can generate for any number of wires. It works just like regular bubble sort does, by repeatedly moving the largest element to the last position by swapping successive pairs of elements.

We need about $\mathcal{O}(n^2)$ comparators in total, the same as regular bubble sort. However, by overlapping them as such, the depth of the sorting network becomes $\mathcal{O}(n)$.

TODO: denote the running time and the number of comparators somehow

---
BITONIC SORT
---

# Construction
This is nice, but we can do better. One way is to use something called a bitonic sort.
It gets its name from bitonic sequences, which are the code idea behind this algorithm.

A sequence is strictly bitonic, if it's first increasing and then decreasing, or first decreasing and then increasing. A bitonic sequence is a rotation of a strict bitonic sequence.

The algorithm is based on smaller building blocks called half-cleaners that take a single bitonic sequence and split it into two bitonic sequences, where the values in one are less than or equal to the values in the other. We won't yet show how to build this block, but trust me that we can do so in a single layer for any size.

We'll now make two observations that will naturally give us the algorithm.

First, notice that we can sort any bitonic sequence of size $n$ by splitting it into two bitonic sequences using a half-cleaner, and recursively repeating this process. The number of layers will be $\log_2(n)$, since each half-cleaner has $1$ layer and we're recursivelly spliting the problem into two smaller ones.

Second, we can merge two sorted sequences of numbers in the sorting network into a bitonic sequence by swapping the wires of either one of the sequences. TODO: phrasing

Combining the two observations, we can build the bitonic sort relatively easily: at the beginning, we have $n/2$ bitonic sequences of size $2$. We'll use half-cleaners to sort them, and then merge them together. After this, we'll have $n/4$ bitonic sequences of size $4$. We'll repeat this until we have a single bitonic sequence, that we again sort and are done.


---
PROOF
---

# Half-cleaner
For proving that the network constructed using the previous observations, we can trivially see that the network sorts all inputs correctly, given that the half-cleaner works as intended.

TODO: show half-cleaner

, we only need to describe how the half-cleaner is built and that it really works on all bitonic sequences. The first part's easy: this is a half-cleaner.

The second part -- not so much, but we'll use a trick called the zero-one principle. It states that if a sorting network correctly sorts all sequences of 0's and 1's (of a valid size), then it correctly sorts all sequences. The proof of this principle is simple -- TODO

As for the half-cleaner, the proof is examining all possible kinds of sequences of 0's and 1's and seeing how the half-cleaner behaves.

---
OPTIMAL SORTING NETWORKS
---

A collection of sorting networks that are even better than bitonic sort (and any other generic sorting network, in fact) are optimal sorting networks. The „optimal“ here can mean one of two things: either the number of comparators or the depth.

The following table captures the current limits for smaller inputs. notice that starting at ..., TODO že je to prostě těžký.
