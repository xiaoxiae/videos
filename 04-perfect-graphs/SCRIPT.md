---
INTRODUCTION
---

# Introduction
<!--- i1 --> Perfect graphs are a family of graphs with various interesting properties, notably that many algorithms that are NP complete on a general graph can be solved efficiently on a perfect one.

<!--- i2 --> There exist various characterizations of perfect graphs. The one that we'll be focusing on in this video is the Weak perfect graph theorem, proved in 1972 by László Lovász.

<!--- i3 --> Before proceeding to the proof, there are quite a few definitions that we have to know in order to understand it. You might already know some of them, so feel free to skip forward in the video accordingly.

---
DEFINITIONS
---

# Complement
<!--- c1 --> A complement of a graph $G$ is a graph $\bar{G}$, such that each two vertices are adjacent in $\bar{G}$, if and only if they are not adjacent in $G$.

# CliqueAndIndependentSet
<!--- cis1 --> A clique is a subgraph of a graph, such that each two vertices are adjacent. Analogically, an independent set in a graph is a set of vertices such that no two are adjacent.

<!--- cis2 --> We'll also denote $\omega(G)$ to be the size of the largest clique in $G$, and $\alpha(G)$ to be the size of the largest independent set in $G$.

<!--- cis3 --> These two concepts are closely tied together. Considering a complement of a graph, we see that each independent set becomes a clique, and vice versa.

# InducedSubgraph
<!--- is1 --> A graph $H$ is an induced subgraph of the graph $G$ (denoted $H \subseteq G$), if and only if we can get $H$ by removing zero or more vertices (along with their edges) from $G$.

<!--- is2 --> Additionally, it is a proper induced subgraph, if we remove one or more vertices.

# ChromaticNumber
<!--- cn1 --> The chromatic number $\chi(G)$ of a graph $G$ is the minimum number of colors we can use to color the graph's vertices, such that no two adjacent vertices have the same color.

TODO: minimum

# PerfectGraph
<!--- p1 --> Finally, a graph $G$ is perfect (informally denoted $G_{\star}$), if and only if $\forall H \subseteq G: \chi(H) = \omega(H)$.

---
OBSERVATIONS
---

TODO

---
LEMMA 1
---

# Lemma1
<!--- lone1 --> Our first lemma is actually a characterization of a perfect graph. It states that the graph $G$ is perfect, if and only if each induced subgraph contains an independent set, such that each maximum clique in $G$ contains a vertex from the set (called a vast independent set).

<!--- lone2 --> The right implication is pretty straight-forward. Since $\chi(G) = \omega(G)$, then each largest clique has all possible colors, menaning that we can then let the independent set be vertices of any given color.

<!--- lone3 --> The left implication can be proved using induction. The base case is trivially true. For the induction step, assume that we've proven the statement for all smaller graphs.

<!--- lone4 --> We know that $G$ has a vast independent set $I$. Let $H$ be the induced subgraph from $G$ by removing this set. By induction, we know that $H$ is perfect, so $\chi(H) = \omega(H)$. Adding the vertices of $I$ back increases $\omega$ by one (all maxium cliques contained one vertex from $I$) and also increases $\chi$ by one (we have to use a new color to color $I$).

---
LEMMA 2
---

# Lemma2
<!--- ltwo1 --> Our second lemma states that if $G$ is perfect, then any graph constructed from $G$ by expanding a vertex is also perfect. By expanding, we mean that we replace the vertex with a complete graph of any size $K_n$ and connect it to all of its neighbours accordingly.

TODO: ještě jeden příklad

<!--- ltwo2 --> For proof, we'll again use induction. Base case is expanding a single vertex to $K_2$, which is perfect. Now we have some graph $G$ and a vertex $v$ that we expand to $v$, $v'$, forming $G'$. We'll examine two cases.

<!--- ltwo3 --> Case one is that expanding increases $\omega$. This is fine, since we now have an additional color that we'll use on $v'$, so $G'$ is still perfect.

<!--- ltwo4 --> Case two is that expanding doesn't increase $\omega$. In this case, let's take a $\chi$ coloring of $G$. Looking at the set of vertices with the same color as $v$, we know that this must be a vast independent set (since each clique contains all of the colors). However, $v$ is not a part of a maximum clique, because otherwise $\omega$ would have increased.

<!--- ltwo5 --> Removing all vertices of this color besides $v$ will decrease $\omega$ by one and, by induction, give a $\chi(G) - 1$ coloring of the smaller graph. Adding the vertices back using the removed color, including the not-yet-added $v'$ proves the second case.

TODO: říct že teď roztahuju, jak chci (indukcí)
TODO: výraznější transformace

---
WEAK PERFECT GRAPH THEOREM
---

# Theorem
<!--- tone1 --> Now we'll finally prove the main theorem. It states that a graph $G$ is perfect, if and only if $\bar{G}$ is perfect.

<!--- tone2 --> First, notice that although this is an equivalence, we only need to prove one implication, since the statement is symmetrical.

<!--- tone3 --> We'll prove the implication using a contradiction. Let's take some graph $G_\star$ that is perfect but $\bar{G}$ isn't.

<!--- tone4 --> Because $\bar{G}$ isn't perfect, it follows from lemma 1 that it doesn't have a vast independent set, meaning that each independent set misses at least one maximum clique. Translated into the language of the graph $G$, each clique misses at least one maximum independent set.

TODO: doesn't follow! dokázat to pomocí nejmenšího

<!--- tone5 --> Let's list all of the cliques in $G_\star$, calling them $Q_1$ to $Q_t$. From the previous observation, for each clique, we have a maximum independent set ($I_1, \ldots, I_t$), such that they miss one another.

<!--- tone6 --> We'll now do something that seems very strange, but is actually the core idea behind the proof. For each vertex $v$ in $G_\star$, let $f(v)$ denote the number of the maximum independent sets that it's in.

<!--- tone7 --> By expanding each vertex $v$ to size $f(v)$, we create a new graph $G'_\star$.

<!--- tone8 --> Now we know that $G'_\star$ is perfect, because $G_\star$ was perfect and any graph expanded from $G_\star$ is, using lemma 2, also perfect.

<!--- tone9 --> The rest of the proof is basically playing with equations in order to show that $\chi(G'_\star) \neq \omega(G'_\star)$, which would make $G'_\star$ not perfect, leading to a contradiction.

<!--- tone10 --> Let's count the number of vertices of $G'_\star$. Since the maximum independent sets from $G_\star$ don't overlap in $G'_\star$ (from the way we expanded each vertex), it's equal to $t . \alpha(G_\star)$.

<!--- tone11 --> Using this, we'll approximate the chromatic number of $G'_\star$. It must be greater than $|V(G'_\star)| / \alpha(G'_\star)$, because that is the ideal situation (each color is not only an independent set, but also the largest one).

<!--- tone12 --> $\alpha(G'_\star)$ is, however, just $\alpha(G_\star)$, because expanding a vertex can't increase the size of the maximum independent set.

<!--- tone13 --> Plugging the value for vertices and simplifying gives us $t$.

<!--- tone14 --> We'll now make an approximation for $\omega(G'_\star)$.

<!--- tone15 --> Let $Q'$ be the largest clique in $G'_\star$. This clique must have been created from inflating some clique $Q$ in $G_\star$. Recall that each clique in $G$ misses at least one maximum independent set. This means, that $\omega(G'_\star) \le t - 1$, because there can be at most one vertex for each independent set, except the one that we know it misses.

<!--- tone16 --> Combining those two inequalities, we get that $\omega(G'_\star) < \chi(G'_\star)$, meaning that $G'_\star$ is not perfect, reaching a contradiction and proving the theorem.

---
STRONG PERFECT GRAPH THEOREM
---

# Theorem2
<!--- ttwo1 --> A stronger version of the theorem that we just proved is the Strong perfect graph theorem. It states that a graph is perfect, if and only if the length of its every hole and antihole (excluding length 3) is even. By hole, we mean an induced cycle and by antihole, we mean a complement to an induced cycle.

<!--- ttwo2 --> The two examples are, using this theorem, not perfect, since they each contain either a hole or an antihole of size 5.

<!--- ttwo3 --> We won't be proving this theorem, since it took a 150-page paper released in 2002 to do so, but we'll observe that it immediately proves the Weak perfect graph theorem (from definition of a complement -- holes become antiholes and vice versa).
