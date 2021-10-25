---
INTRODUCTION
---

Graphs and polynomials are two things that, at a first glance, seem completely unrelated -- what would it even mean for a graph to be equal to some polynomial?

Yet, by the end of this video, you'll hopefully be convinced that it actually makes quite a lot of sense, and that for example, the graph on the left corresponds to the polynomial on the right, with its function values containing information about the graph's properties and structure.

TODO: animace grafu vedle polynomu


---
DEFINITIONS
---

Let's start simple: this is a graph. It consists of vertices connected by edges. We'll call $V$ the set of vertices and $E$ the set of edges.

The graph can either be connected, consisting of a single component, or not connected, consisting of multiple components. We'll also define $c(G)$ as the number of components. As you can see, $c(G)$ of this graph is $3$.

--- nový graf

For a connected graph, we define its spanning tree as the smallest subgraph that keeps the graph connected. We'll call the number of edges in a graph's spanning tree its **rank** (denoted $r(G)$). For a connected graph, this is equal to $|V| - 1$ (feel free to pause here and think about why).

We can generalize the concept of a spanning tree for graphs that are not connected by considering the spanning trees of each individual component. Here, the rank of the graph will be $r(G) = |V| - c(G)$. This is because splitting the graph into more components decreases the number of edges in the spanning trees by one.

Similarly, the nullity of a given set of edges, defined as $n(G) = |E| - r(G)$ is the number of edges that are not in the spanning trees. We can think of it as the opposite of rank. This should again make sense, since it's just the number of all edges minus the ones in the spanning trees.

TODO: animace označující ty množiny na nějakém grafu o více komponentách (konkrétně si uvědomit, že to jsou doplňky)

Notice that we defined rank and nulity in a way that we can think about a rank or nulity of a set of edges, not just the entire graph.

With this out of the way, we can define the Tutte polynomial as being the following:

TODO: definice.

This looks completely arbitrary. And... well... to some extent, it is. There are other ways to derive a polynomial from a graph, but we'll look at why this particular one makes the most amount of sense for what we'd like to do. So... what would we like to do?

---
DEFINITIONS
---

TODO: hodnoty
- (1, 1) -- počet koster (s důkazem)
- (2, 1) -- počet lesů
- (2, 0) -- počet acyklických zorientování

TODO: chromatický polynom
TODO: zmínka o flow polynomu
TODO: rekurzivní vzorec
