# Introduction (Introduction)
Perfect graphs are certain type of graphs with various interesting properties, most notably that many algorithms that are NP complete on a general graph can be solved efficiently on a perfect one.

There exist various characterizations of perfect graphs. The one that we'll be focusing on in this video is the weak perfect graph theorem, proved in 1972 by László Lovász.

Before proceeding to the proof, there are some definitions and lemmas we have to know.

# Complement graph (Complement)
A graph $H$ is a complement of the graph $G$, if and only if each two vertices adjacent in $G$ are not adjacent in $H$.

# Clique and independent set (CliqueAndIndependentSet)
A clique is a subgraph of a graph, such that each two vertices are adjacent. Analogically, and independent set of a graph is a set of vertices such that no two are adjacent.

We'll also denote omega(G) to be the number of vertices of the largest clique in G, and alpha(G) to be the largest independent set in G.

These two concepts are closely tied together. Considering a complement of a graph, we see that each independent set becomes a clique, and each clique an independent set.

# Induced subgraph (InducedSubgraph TODO)
A graph $H$ is an induced subgraph of the graph $G$ (denoted $H \subseteq G$), if and only if we can get $H$ by removing zero or more vertices from $G$. Note that we're only removing whole vertices (and their edges), not edges by themselves.

# Chromatic number (ChromaticNumber)
The chromatic number $\chi(G)$ of a graph $G$ is the smallest number of colors we can use to color the graph's vertices, such that no two adjacent vertices have the same color.

# Perfect Graphs (PerfectGraphs TODO)
Finally, a graph $G$ is perfect, if and only if $\forall H \subseteq G: \chi(H) = \omega(H)$.

# Observations
chi g >= omega g
dědičnost

# Lemma 1

# Nafouknutí grafu

# Lemma 2

# Znění

# Důkaz
- nejmenší t. 

[o1] This is a sentence in the script to record.

[o2] This is another sentence in the script to record.

# Section two (SectionTwoClassName)

[w1] This is a third sentence to record.

# Strong theorem
