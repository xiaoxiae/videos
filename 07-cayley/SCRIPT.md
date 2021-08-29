---
INTRODUCTION
---

# Motivation TODO
In this short video, we'll be looking at an elegant proof of Cayley's formula about the number of spanning trees in a complete graph. It was discovered by Jim Pitman, and is a great example of a powerful proof technique called double counting.

# Definitions
A complete graph on $n$ vertices is a graph, where each pair of vertices is connected by an edge.

A spanning tree in a graph is a subgraph that is a tree and includes all vertices of the original graph. A good way to think of it is that it's the smallest subgraph that keeps the graph connected.

---
PROBLEM STATEMENT
---

# Formula
Cayley's formula is rather simple: it states, that the number of spanning trees of a complete graph on $n$ vertices is $\kappa(n) = n^{n-2}$. While simple in statement, it's definitely not trivial to prove.

Also, it's worth noting that these three spanning trees differ. Although they are the same in structure (the fancy term here is isomorphic), they differ in where the edges actually are, which is what matters.

---
PROOF
---

As I've mentioned earlier, the proof technique that we'll be using is double counting. This involves, as the name suggests, counting some quantity in two different ways.

For this proof, we'll be counting the number of oriented trees on $n$ vertices that have a root and some numbering of edges. Let's call this quantity $\Tau$.

Here are two examples of what the trees could look like. The root is highlighted in yellow, with all edges pointing towards it.

The first way to count will be using Cayley's formula, which itself equals the number of trees on $n$ vertices. Additionally, there are $n$ ways to select the root and $(n-1)!$ ways to select the edge numbering, bringing the total to $\kappa(n) \cdot n \cdot (n-1)!$.

The other way will be constructive -- imagine we're building the tree by adding edges between vertices. Let's say we've already added $k$ of them, so the graph might look like this.

It is made up of components that all have individual roots.

Looking at the graph, we can make two observations about the edge we're about to add:

1. it can't be between two vertices of a single component, as it would create a cycle
2. it has to lead from the root of a component, because otherwise the edges wouldn't point towards the root

Putting this together: there are $n - k - 1$ components (every edge combines two components into one) and therefore $n - k - 1$ ways to pick where the edge will start. 
