---
INTRODUCTION
---

# Motivation
**[m1]:**  In this short video, we'll be looking at an elegant proof of Cayley's formula about the number of spanning trees in a complete graph. It was discovered by Jim Pitman, and is a great example of a powerful proof technique called double counting.

# Definitions
**[d1]:** A complete graph on $n$ vertices (denoted $K_n$) is a graph, where each pair of vertices is connected by an edge.

**[d2]:** A spanning tree in a graph is a subgraph that is a tree and includes all vertices of the original graph. A good way to think of it is that it's the smallest subgraph that keeps the graph connected.

---
FORMULA STATEMENT
---

# Formula
**[c1]:** Cayley's formula is rather simple: it states that the number of spanning trees of a complete graph on $n$ vertices is $\kappa(n) = n^{n-2}$. While being simple in statement, it's definitely not trivial to prove.

**[c2]:** Also, it is worth noting that these three spanning trees are different. Although they are the same in structure (the fancy term here is isomorphic), they differ in where the edges actually are, which is what matters.

---
PROOF
---

**[p1]:** As I've mentioned earlier, the proof technique that we'll be using is double counting. This involves, as the name suggests, counting some quantity in two different ways.

**[p2]:** For this proof, we'll be counting the number of oriented trees on $n$ vertices that have a root and some numbering of edges. Let's call this quantity $\tau(n)$.

**[p3]:** Here are two examples of what the trees could look like.

**[p4]:** First, let's just count the number of trees without root and edge numbering. This, from definition, equals $\kappa(n)$. Next, the root can be any of the $n$ vertices, so we multiply by $n$. Finally, the edge numbers can be any permutation of numbers from $0$ to the number of edges, which is $n-1$. This brings the total to $\kappa(n) \cdot n \cdot (n-1)!$.

**[p5]:** The other way will be constructive -- we'll build the tree by adding oriented edges between the vertices, with numbers depending on when they were added.

**[p6]:** Looking at the example graph, we can make two observations about the edge we're about to add:

1. it has to start in the root of a component, because otherwise some edges wouldn't be pointing towards the root
2. it can not be between two vertices of a single component, as this would create a cycle, which a tree can not have

**[p9]:** Putting this together, let's count the number of ways we can add the $k$-th edge (counting from zero). In our example, $k = 3$.

**[p10]:** The edge can end in any vertex, of which there are $n$. Given this end, we know it has to start from the root of some component (observation 1) and it can not start in the component where it ends (observation 2). This means that from the $n - k$ components that we currently have, it can only start in $n - k - 1$ of them, since one is reserved for the end.

**[p11]:** To build the entire tree, all $n - 1$ edges must be added. When adding the $k$-th edge, there are $n \cdot (n - k - 1)$ ways to do so, resulting in the following formula.

**[p12]:** Here, we can take the $n$ out, becoming $n^{n - 1}$. As for the product itself, notice that this is just $(n-1) \cdot (n-2) \cdot \ldots \cdot 1$, which equals $(n - 1)!$

**[p13]:** Using the previous way to count, we can simplify, divide by $n$ and we're done.

---
OUTRO
---
