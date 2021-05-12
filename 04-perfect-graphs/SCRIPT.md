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

# PerfectGraph
<!--- p1 --> Finally, a graph $G$ is perfect (informally denoted $G_{\star}$), if and only if $\forall H \subseteq G: \chi(H) = \omega(H)$.

---
OBSERVATIONS AND EXAMPLES
---

# Observations

<!--- o1 --> With definitions out of the way, let's make a few observations about how perfect graphs behave that will help us understand the proof better.

<!--- o2 --> Firstly, $\forall H \subseteq G: \omega(H) \le \chi(H)$, because each maximum clique has to contain $\omega(H)$ different colors. What perfect graphs are saying is that this inequality is actually an equality.

<!--- o3 --> Secondly, if a graph is perfect, then each of its induced subgraphs is perfect too. This follows immediately from the definition of a perfect graph (since something is true for each of its induced subgraphs).

<!--- o4 --> As for examples, some common families of graphs that are perfect include complete graphs ($\chi = n = \omega$) and bipartite graphs ($\chi$ is either 1 when it has no edges, or 2 if it does, either of which works).

<!--- o5 --> Some families that are not perfect include cycles of odd length $\ge 5$ ($\omega = 2$ and $\chi = 3$) and even wheel graphs of length $\ge 6$ ($\omega = 3$ and $\chi = 4$).

TODO: animace a výpis

---
LEMMA 1
---

# Lemma1
<!--- lone1 --> Our first lemma is actually a characterization of a perfect graph. It states that the graph $G$ is perfect, if and only if each induced subgraph contains an independent set, such that each maximum clique in $G$ contains a vertex from the set (called a vast independent set).

<!--- lone2 --> The left-to-right implication is pretty straight-forward. Since $\chi(G) = \omega(G)$, each largest clique contains all possible colors. That means we can choose any particular color and let the independent set be all vertices of that color. By definition, such independent set is vast.

<!--- lone3 --> The right-to-left implication can be proved using induction on the number of vertices. The base case is trivially true. For the induction step, assume that we've proven the statement for all smaller graphs.

<!--- lone4 --> Let $G$ be a graph such that each induced subgraph of $G$ contains a vast independent set. Let $I$ be a vast independent set in $G$ itself. Let $H$ be the induced subgraph obtained from $G$ by removing $I$. Observe that $\omega(H) = \omega(G) - 1$, since all maximum cliques in $G$ contain one vertex from $I$. $H$ satisfies the right hand side of our equivalence, so by induction, $H$ is perfect. Therefore there exists a vertex coloring of $H$ using $\omega(G) - 1$ colors. Adding the vertices of $I$ back, we can color all of them using one extra color and obtain coloring of $G$ using $\omega(G)$ colors. 

---
LEMMA 2
---

# Lemma2
<!--- ltwo1 --> Our second lemma states that if $G$ is perfect, then any graph constructed from $G$ by expanding a vertex is also perfect. By expanding, we mean that we replace the vertex with a complete graph of any size $K_n$ and connect it to all of its neighbours accordingly.

TODO: ještě jeden příklad

<!--- ltwo2 --> For proof, observe that expanding a vertex to $K_n$ is equivalent to expanding it to $K_2$ (n-1)-times. It's therefore sufficient to prove that expanding a vertex to $K_2$ doesn't destroy perfectness of a graph. Let's again use induction on the number of vertices in $G$. Base case is expanding a single vertex to $K_2$, which is perfect. Now we have some graph $G$ and a vertex $v$ that we expand to $v$, $v'$, forming $G'$. We'll examine two cases.

<!--- ltwo3 --> Case one is that expanding increases $\omega$. Obviously, $\omega$ can only increase by 1. This is fine, since we now can use an additional color that we'll use on $v'$, so $G'$ is still perfect.

<!--- ltwo4 --> Case two is that expanding doesn't increase $\omega$. In this case, let's take a $\chi$ coloring of $G$. Looking at the set of vertices with the same color as $v$, we know that this must be a vast independent set (since each clique contains all of the colors). However, $v$ is not a part of a maximum clique, because otherwise $\omega$ would have increased.

<!--- ltwo5 --> Removing all vertices of this color besides $v$ will decrease $\omega$ by one and, by induction, give a $\chi(G) - 1$ coloring of the smaller graph. Adding the vertices back using the removed color, including the not-yet-added $v'$ proves the second case.

---
WEAK PERFECT GRAPH THEOREM
---

# Theorem
<!--- tone1 --> Now we'll finally prove the main theorem. It states that a graph $G$ is perfect, if and only if $\bar{G}$ is perfect.

<!--- tone2 --> First, notice that although this is an equivalence, we only need to prove one implication, since the statement is symmetrical.

<!--- tone3 --> We'll prove the implication using a contradiction. Let's take the smallest graph $G_\star$ that is perfect but $\bar{G}$ isn't.

<!--- tone3.5 --> Because $\bar{G}$ isn't perfect, it follows from lemma 1 that it has an induced subgraph $H$ without a vast independent set. Furthermore, $H = \bar{G}$, because if $H \subset \bar{G}$, then $\bar{H}$ would be perfect (since $\bar{H} \subset G$ and $G$ is perfect). This would, however, be a contradiction with the minimality of $(G, \bar{G})$.

<!--- tone4 --> We now know that $\bar{G}$ doesn't have a vast independent set, meaning that each independent set misses at least one maximum clique. Translated into the language of the graph $G$, each clique misses at least one maximum independent set.

<!--- tone5 --> Let's list all of the cliques in $G_\star$, calling them $Q_1$ to $Q_t$. From the previous observation, for each clique $Q_i$, we have a maximum independent set $I_i$, such that they are disjunct.

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
