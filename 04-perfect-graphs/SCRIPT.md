# Introduction (Introduction)
Perfect graphs are certain type of graphs with various interesting properties, most notably that many algorithms that are NP complete on a general graph can be solved efficiently on a perfect one.

There exist various characterizations of perfect graphs. The one that we'll be focusing on in this video is the weak perfect graph theorem, proved in 1972 by László Lovász.

Before proceeding to the proof, there are quite a few definitions that we have to know in order to understand it. You might already know some of them, so feel free to skip forward in the video accordingly. (TODO list)

# Complement graph (Complement)
A graph $\conj{G}$ is a complement of the graph $G$, if and only if each two vertices adjacent in $G$ are not adjacent in $\conj{G}$. TODO in animation

# Clique and independent set (CliqueAndIndependentSet)
A clique is a subgraph of a graph, such that each two vertices are adjacent. Analogically, and independent set of a graph is a set of vertices such that no two are adjacent.

We'll also denote omega(G) to be the number of vertices of the largest clique in $G$, and alpha(G) to be the largest independent set in G.

These two concepts are closely tied together. Considering a complement of a graph, we see that each independent set becomes a clique, and each clique an independent set.

# Induced subgraph (InducedSubgraph TODO)
A graph $H$ is an induced subgraph of the graph $G$ (denoted $H \subseteq G$), if and only if we can get $H$ by removing zero or more vertices (along with their edges TODO in animation) from $G$. Note that we're only removing whole vertices (and their edges), not edges by themselves.

TODO: strict, change the text

# Chromatic number (ChromaticNumber)
The chromatic number $\chi(G)$ of a graph $G$ is the smallest number of colors we can use to color the graph's vertices, such that no two adjacent vertices have the same color.

# Perfect graph (PerfectGraphs TODO)
Finally, a graph $G$ is perfect, if and only if $\forall H \subseteq G: \chi(H) = \omega(H)$.

# Lemma 1 (Lemma1 TODO)
Let's prove our first lemma, which is actually a characterization of a perfect graph.

A vast independent set in $G$ is an independent set, such that each maximum clique in $G$ contains a vertex from the set.

TODO Jigoerajgjea!

The graph $G$ is perfect, if and only if it contains a vast independent set.



# Lemma 2 (Lemma2 TODO)
Our second lemma is another characterization of perfect graphs. Let $G$ be a graph. Then it is perfect, if and only if any graph constructed from $G$ by inflating a vertex is also perfect.

By inflating, we mean that we replace the vertex with $K_n$ and connect it to all of its neighbours.

TODO: proof

# Weak perfect graph theorem
The graph $G$ is perfect, if and only if $\conj{G}$ is perfect.

First, notice that although this is an equivalence, we only need to prove one implication, since the statement is symetrical. TODO: text animation

We'll prove the implication using a contradiction. Let's take the smallest $G$ (in the number of vertices) that is perfect but $\conj{G}$ isn't.

Because $\conj{G}$ isn't perfect, it follows from lemma 1 it has an induced subgraph $H$ without a vast independent set. Furthermore, $H = \conj{G}$, because if $H \subset \conj{G}$, then $\conj{H}$ would be perfect (since $\conj{H} \subset G$, which is a contradiction with the minimality of $(G, \conj{G})$.

TODO: obrázek toho lemmatu

$\conj{G}$ not having a vast independent set means that each independent set misses at least one maximum clique.

TODO: animace toho, že máme ten graf s největší klikou, a ty vrcholy jsou všude, jen né v ní.

Translated into the language of the graph $G$, each clique misses at least one maximum independent set. This follows from the observations that we made about cliques and independent sets earlier in the video.

TODO: animace vysloveně v textu (jako slova, become...)

Let $Q_1, Q_2, \ldots, Q_t$ be the set of cliques in $G$. From the previous observation, for each $Q_i$, we have a maximum independent set $I_i$, such that they miss one another.

We'll now do something which seems weird, but is actually the core idea of the proof. 

x is f(x) |{i | x \in I_i}|

We'll inflate x to size f(x) (if f(x) == 0, delete it)

G* is perfect from lemma (2) 

count number of vertices of G*... sum f(x) = t \times \alpha(g)
- t is number of Q_1

chi(G*) >= |v(G*)| / alpha(G*) = V( \alpha g .. .TODO = t

TODO pro Q*, dojde jiný odhad

# Strong perfect graph theorem
