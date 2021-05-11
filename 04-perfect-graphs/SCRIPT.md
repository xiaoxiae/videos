=== WEAK PERFECT GRAPH THEOREM ===

--- INTRODUCTION ---

# Introduction (Introduction)
Perfect graphs are a family of graphs with various interesting properties, notably that many algorithms that are NP complete on a general graph can be solved efficiently on a perfect one.

There exist various characterizations of perfect graphs. The one that we'll be focusing on in this video is the Weak perfect graph theorem, proved in 1972 by László Lovász.

Before proceeding to the proof, there are quite a few definitions that we have to know in order to understand it. You might already know some of them, so feel free to skip forward in the video accordingly.

--- DEFINITIONS ---

# Complement graph (Complement)
A complement of a graph $G$ is a graph $\bar{G}$, such that each two vertices are adjacent in $\bar{G}$, if and only if they are not adjacent in $G$.

# Clique and independent set (CliqueAndIndependentSet)
A clique is a subgraph of a graph, such that each two vertices are adjacent. Analogically, and independent set in a graph is a set of vertices such that no two are adjacent.

We'll also denote $\omega(G)$ to be the size of the largest clique in $G$, and $\alpha(G)$ to be the size of the largest independent set in $G$.

These two concepts are closely tied together. Considering a complement of a graph, we see that each independent set becomes a clique, and vice versa.

# Induced subgraph (InducedSubgraph)
A graph $H$ is an induced subgraph of the graph $G$ (denoted $H \subseteq G$), if and only if we can get $H$ by removing zero or more vertices (along with their edges) from $G$.

Additionally, it is a proper subgraph, if we remove one or more vertices.

# Chromatic number (ChromaticNumber)
The chromatic number $\chi(G)$ of a graph $G$ is the smallest number of colors we can use to color the graph's vertices, such that no two adjacent vertices have the same color.

# Perfect graph (PerfectGraph)
Finally, a graph $G$ is perfect (informally denoted $G_{\star}$), if and only if $\forall H \subseteq G: \chi(H) = \omega(H)$.

--- LEMMA 1 ---

# Lemma 1 (Lemma1)
Our first lemma is actually a characterization of a perfect graph. It states that the graph $G$ is perfect, if and only if it contains an independent set, such that each maximum clique in $G$ contains a vertex from the set (called a vast independent set).

The right implication is pretty straight-forward. Since $\chi(G) = \omega(G)$, then each largest clique has all possible colors. We can then let the independent set be vertices of any given color, and are done.

The left implication can be proved using induction. The base case is $\omega(G) = 1$ and is trivially true. For the induction step, assume that we've proven the statement for all smaller graphs.

We know that $G$ has a vast independent set $I$. Let $H$ be the induced subgraph from $G$ by removing this set. By induction, we know that $H$ is perfect, so $\chi(H) = \omega(H)$. Adding the vertices of $I$ back increases $\omega$ by one (all maxium cliques contained one vertex from $I$) and also increases $\chi$ by one (we have to use a new color to color $I$).

--- LEMMA 2 ---

# Lemma 2 (Lemma2)
Our second lemma states that if $G$ is perfect, then any graph constructed from $G$ by expanding a vertex is also perfect. By expanding, we mean that we replace the vertex with $K_n$ and connect it to all of its neighbours accordingly.

For proof, we'll again use induction. Base case is expanding a single vertex to $K_2$, which is perfect. Now we have some graph $G$ and a vertex $v$ that we expand to $v$, $v'$, forming $G'$. We'll examine two cases.

Case one is that expanding increases $\omega$. This is fine, since we now have an additional color that we'll use on $v'$, so $G'$ is still perfect.

Case two is that expanding doesn't increase $\omega$. In this case, let's take the coloring of $G$. Looking at the set of vertices with the same color as $v$, we know that this must be a vast independent set (since each clique contains all of the colors). However, $v$ is not a part of a maximum clique, because otherwise $\omega$ would have increased.

Removing all vertices of this color besides $v$ will decrease $\omega$ by one and, by induction, give the coloring of the smaller graph. Adding the vertices back, including the not-yet-added $v'$ proves the second case.

--- WEAK PERFECT GRAPH THEOREM ---

# Weak perfect graph theorem (Theorem)
Now we'll finally prove the main theorem. It states that a graph $G$ is perfect, if and only if $\bar{G}$ is perfect.

First, notice that although this is an equivalence, we only need to prove one implication, since the statement is symmetrical.

We'll prove the implication using a contradiction. Let's take some graph $G$ that is perfect but $\bar{G}$ isn't.

Because $\bar{G}$ isn't perfect, it follows from lemma 1 that it doesn't have a vast independent set, meaning that each independent set misses at least one maximum clique. Translated into the language of the graph $G$, each clique misses at least one maximum independent set.

Let's now list all of the cliques in $G$, calling them $Q_1$ to $Q_t$. From the previous observation, for each clique, we have a maximum independent set ($I_1, \ldots, I_t$), such that they miss one another.

Now, we'll now do something that seems very strange, but is actually the core idea behind the proof. For each vertex $v$ in $G$, let $f(v)$ denote the number of the maximum independent sets that it's in.

We'll now create a new graph $G'$ from $G$ by expanding each vertex $v$ to size $f(v)$.

Now we know that $G'$ is perfect, because $G$ was perfect and any graph expanded from $G$ is, using lemma 2, also perfect.

The rest of the proof is basically playing with equations in order to show that $\chi(G') != \omega(G')$, which would make $G'$ not perfect, leading to a contradiction.

Let's count the number of vertices of $G'$. Since the maximum independent sets from $G$ don't overlap in $G'$ (from the way we expanded each vertex), it's equal to $t . \alpha(G)$.

Using this, we'll approximate the chromatic number of $G'$. It must be greater than $|V(G')| / \alpha(G')$, because that is the ideal situation (each color is not only an independent set, but also the largest one).

$\alpha(G')$ is, however, just $\alpha(G)$, because expanding a vertex can't increase the size of the maximum independent set.

Plugging the value for vertices gives and simplifying just $t$.

We'll now make an approximation for $\omega(G')$.

Let $Q'$ be the largest clique in $G'$. This clique must have been created from inflating some clique $Q$ in $G$. Recall that each clique in $G$ misses at least one maximum independent set. This means, that $\omega(G') <= t - 1$, because there can be at most one vertex for each independent set, except the one that we know it misses.

Combining those two inequalities, we get that $\omega(G') < \chi(G')$, meaning that $G'$ is not perfect, reaching a contradiction and proving the theorem.

--- STRONG PERFECT GRAPH THEOREM ---

# Strong perfect graph theorem (Theorem2)
A stronger version of the theorem that we just proved is the Strong perfect graph theorem. It states that a graph is perfect, if and only if the length of its every hole and antihole (excluding length 3) is even. By hole, we mean an induced cycle and by antihole, we mean a complement to an induced cycle.

The two examples are, using this theorem, not perfect, since they each contain either a hole or an antihole of size 5.

We won't be proving this theorem, since it took a 150-page paper released in 2002 to do so, but we'll observe that it immediately proves the Weak perfect graph theorem (from definition of a complement - holes become antiholes and vice versa).
