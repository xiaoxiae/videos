=== WEAK PERFECT GRAPH THEOREM ===

--- INTRODUCTION ---

# Introduction (Introduction)
Perfect graphs are certain type of graphs with various interesting properties, notably that many algorithms that are NP complete on a general graph can be solved efficiently on a perfect one.

There exist various characterizations of perfect graphs. The one that we'll be focusing on in this video is the Weak perfect graph theorem, proved in 1972 by László Lovász.

Before proceeding to the proof, there are quite a few definitions that we have to know in order to understand it. You might already know some of them, so feel free to skip forward in the video accordingly.

--- DEFINITIONS ---

# Complement graph (Complement)
A complement of a graph $G$ is a graph $\bar{G}$, such that each two vertices are adjacent in $\{G}$, if and only if they are not adjacent in $G$.

# Clique and independent set (CliqueAndIndependentSet)
A clique is a subgraph of a graph, such that each two vertices are adjacent. Analogically, and independent set of a graph is a set of vertices such that no two are adjacent.

We'll also denote $\omega(G)$ to be the number of vertices of the largest clique in $G$, and $\alpha(G)$ to be the largest independent set in $G$.

These two concepts are closely tied together. Considering a complement of a graph, we see that each independent set becomes a clique, and each clique an independent set.

# Induced subgraph (InducedSubgraph)
A graph $H$ is an induced subgraph of the graph $G$ (denoted $H \subseteq G$), if and only if we can get $H$ by removing zero or more vertices (along with their edges) from $G$.

Aditionally, it is a proper subgraph, if we remove one or more vertices.

# Chromatic number (ChromaticNumber)
The chromatic number $\chi(G)$ of a graph $G$ is the smallest number of colors we can use to color the graph's vertices, such that no two adjacent vertices have the same color.

# Perfect graph (PerfectGraph)
Finally, a graph $G$ is perfect, if and only if $\forall H \subseteq G: \chi(H) = \omega(H)$.

--- LEMMA 1 ---

# Lemma 1 (Lemma1 TODO)
Our first lemma is actually a characterization of a perfect graph. It states that the graph $G$ is perfect, if and only if it contains a vast independent set. By vast, we mean an independent set in $G$, such that each maximum clique in $G$ contains a vertex from the set.

TODO: proof

--- LEMMA 2 ---

# Lemma 2 (Lemma2 TODO)
Our second lemma states that if $G$ is perfect, then any graph constructed from $G$ by expanding a vertex is also perfect. By expanding, we mean that we replace the vertex with $K_n$ and connect it to all of its neighbours accordingly.

For proof, we'll use induction. Base case is expanding a single vertex to $K_2$, which is perfect.
For the induction step, TODO the rest of the proof

--- WEAK PERFECT GRAPH THEOREM ---

# Weak perfect graph theorem (Theorem)
Now we'll finally prove the main theorem which state that a graph $G$ is perfect, if and only if $\bar{G}$ is perfect.

First, notice that although this is an equivalence, we only need to prove one implication, since the statement is symetrical (complementing a complement graph yields the original graph). TODO: in text

We'll prove the implication using a contradiction. Let's take the smallest $G$ (in the number of vertices) that is perfect but $\bar{G}$ isn't.

Because $\bar{G}$ isn't perfect, it follows from lemma 1 that it has an induced subgraph $H$ without a vast independent set. Furthermore, $H = \bar{G}$, because if $H \subset \bar{G}$, then $\bar{H}$ would be perfect (since $\bar{H} \subset G$ and $G$ is perfect). This would, however, be a contradiction with the minimality of $(G, \bar{G})$.

TODO: obrázek toho lemmatu?

$\bar{G}$ not having a vast independent set means that each independent set misses at least one maximum clique.

Translated into the language of the graph $G$, each clique misses at least one maximum independent set. This follows from the observations that we made about cliques and independent sets in complementing graphs earlier in the video.

TODO: animace vysloveně v textu (jako slova, become...)

Let $Q_1, Q_2, \ldots, Q_t$ be the set of all cliques in $G$. From the previous observation, for each clique, we have a maximum independent set, such that they miss one another.

Now, we'll now do something that seems very strange, but is actually the core idea behind the proof. For each vertex $v$, let $f(v)$ denote the number of the maximum independent sets that it's in.

TODO: the animation with the independent sets and f(x) above the given vertex

We'll now create a new graph $G^*$ from $G$ by expanding each vertex $v$ to size $f(v)$.

TODO: the animation of the vertex expanding into a K_3

We know that $G^*$ is perfect, because $G$ was perfect and any graph expanded from $G$ is, using lemma 2, also perfect. The rest of the proof is basically playing with equations in order to reach a contradiction by showing that $\chi(G^*) != \omega(G^*)$, TODO that it's still quite interesting

Let's count the number of vertices of $|V(G^*)|$. Notice that due to the expansion, the maximum independent sets from $G$ now don't overlap anymore, and so the number of vertices is $t . \alpha(G^*)$.

Using this, we'll approximate the chromatic number of $G^*$. Because vertices of each color each form an independent set (from definition -- they can't be adjacent to one another), the best we can do is ....

This is now equal to ..., because TODO: tohle není triviální pozorování

TODO: plug in values
$$\chi(G^*) \ge \frac{|V(G^*)|}{\alpha(G^*)}$$

TODO: animation of how each independent set takes one portion of the vertex.

--- STRONG PERFECT GRAPH THEOREM

# Strong perfect graph theorem
