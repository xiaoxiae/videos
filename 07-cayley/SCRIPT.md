---
INTRODUCTION
---

# Motivation TODO
In this short video, we'll be looking at an elegant proof of Cayley's formula about the number of spanning trees in a complete graph. It was discovered by Jim Pitman, and is a great example of a powerful proof technique called double counting.

# Definitions
A complete graph on $n$ vertices (denoted $K_n$) is a graph, where each pair of vertices is connected by an edge.

A spanning tree in a graph is a subgraph that is a tree and includes all vertices of the original graph. A good way to think of it is that it's the smallest subgraph that keeps the graph connected.

---
PROBLEM STATEMENT
---

# Formula
Cayley's formula is rather simple: it states, that the number of spanning trees of a complete graph on $n$ vertices is $\kappa(n) = n^{n-2}$. While simple in statement, it's definitely not trivial to prove.

Also, it's worth noting that these three spanning trees are not equal. Although they are the same in structure (the fancy term here is isomorphic), they differ in where the edges actually are, which all that matters.

---
PROOF
---

As I've mentioned earlier, the proof technique that we'll be using is double counting. This involves, as the name suggests, counting some quantity in two different ways.

For this proof, we'll be counting the number of oriented trees on $n$ vertices that have a root and some numbering of edges. Let's call this quantity $\tau(n)$.

Here are two examples of what the trees could look like. As you can see, the edges are oriented such that they point towards the root.

The first way to count will be straightforward: to begin with, let's count the number of trees without root and edge numbering -- this, from definition, equals $\kappa(n)$. Next, the root can be any of the $n$ vertices. Finally, the edge numbers can be any permutation of numbers from $0$ to $n-1$ (which is the number of edges), bringing the total to $\kappa(n) \cdot n \cdot (n-1)!$.

The other way will be constructive. Imagine we're building the tree by adding oriented edges between the vertices. Taking $n = 7$ as an example, let's add a few vertices.

Looking at the graph, we can see it is made up of smaller components, each having a single root.

We can now make two observations about the edge we're about to add:

1. it has to start in the root of a component, because otherwise some edges wouldn't point towards the root
2. it can't be between two vertices of a single component, as the component wouldn't be a tree anymore

Putting this together, let's count the number of ways we can add the $k$-th edge.

It can end in any vertex, of which there are $n$. When it comes to where it can start, we know it has to start from the root of some component (observation 1). and it can't start in the component where it ends (observation 2), so from the $n - k$ components, it can only start in $n - k - 1$ of them.

To build the entire tree, $n - 1$ edges must be added. At the $k$-th step, there are $n \cdot (n - k - 1)$ ways to add it, resulting in the following formula.

Taking the $n$ out, it becomes $n^{n - 1}$. As for the product, notice that it's just $(n-1)!$.

Using the previous way to count, we can simplify, divide by $n$ and we're done.

