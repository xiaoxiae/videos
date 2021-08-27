---
INTRODUCTION
---

In this short video, we'll be looking at an elegant proof of Cayley's formula about the number of spanning trees in a complete graph. It was discovered by Jim Pitman, and is a great example of a powerful proof technique called double counting.

# Definitions
A complete graph on $n$ vertices is a graph, where each pair of vertices is connected by an edge.

A spanning tree of a graph is a subgraph that is a tree and includes all vertices of the original graph. A good way to think of it is that it's the smallest subgraph that keeps the graph connected.

TODO: animace toho, že rozpojení je špatný

---
PROBLEM STATEMENT
---

Cayley formula is rather simple: it states, that the number of spanning trees in a complete graph κ(n) = n^(n-2), where $n$ is the number of vertices. While simple in statement, it's definitely not trivial to prove.

TODO: nechat ten statement celou dobu nahoře

Also, it's worth noting that this spanning tree is different than this one and also than this one -- although they are the same in structure, they differ on where the edges actually are, which is what matters.

TODO: animace těch grafů vedle sebe

---
PROOF
---

As I've mentioned eariler, the proof technique that we'll be using is double counting. This involves, as the name suggests, counting something in two different ways. For this proof, we'll be counting oriented trees on $n$ vertices that have a root (with all edges pointing towards it) and some numbering of edges.

TODO: příklady těch stromů

When counting using $κ$, this is equal to $κ(n) \cdot n \cdot (n-1)!$, because there are $κ(n)$ trees on $n$ vertices, $n$ ways to pick the root, and $(n-1)!$ ways to number the edges (since there number of edges of a tree is $n-1$).
