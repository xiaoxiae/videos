# Vizing's theorem
In this video, we'll be proving Vizing's theorem, which puts an upper and lower bound on edge coloring of a graph. A valid edge coloring of a graph is a coloring of edges such that no vertex has edges of the same color.

## Theorem (Intro)
[t1] Vizig's Theorem states, that the number of colors needed to edge-color a graph is either the degree of the graph, or degree of the graph plus one.

## Degree (Degree TODO)
As a reminder, the degree of a vertex is the number of outgoing edges, and the degree of the entire graph is the maximum degree of one of its vertices.

## Example (Example)
Let's look at an example graph. We can use 3 colors to colors it, which happens to be its degree. However, adding additional two edges like so doesn't change the degree, but increases the number of colors needed by one.

## Lower bound (LowerBound)

Proving the lower bound is quite trivial. Looking at a vertex with the maximum degree in the graph, we obviously need as many colors as the number of its edges.

[l2] Before proving the upper bound, let's make a quick observation that will be useful during the proof.

[l2] When we have \chi + 1 colors, each vertex of the graph has at least one free color. By this, we mean that we can change the color of any of the vertex's edge to the free color and not break the coloring (for this particular vertex). This makes sense, because we have one more color than the degree of the graph.

## Upper bound (UpperBound)

[l2] We'll prove the upper bound using a contradiction. Let's assume that we can't in fact color some graph $G$ using \chi + 1 colors. This means that while coloring, we ran out of colors and can't color some vertex ${x, y}$.

From the previous observation, we know that $x$ has some free color. $y$ can't have this free color, because we could then color the edge with this color, so it has to have one different from $x$. This means that there is an edge with this color from $x$ to some other vertex, which also has some free color.

This chain can go on a bit, but eventually, one of two things will happen.

Case one is that the free color of the last vertex in the chain is the color of $x$. In this case, we'll go back the chain and change colors, like so. This frees up the color for $x$ that we need and we colored e.

Case two is that the free color of the last vertex is color of an edge from $x$ that we've seen before. This is a little unpleasant, since we're now stuck in a loop and can't use the previous trick.

In this case, let's look at the longest path from this vertex of alternating free colors of $x$ and $v$, starting at $w$.

Let's think about why switching the colors on this path doesn't break anything.

For vertices in between, nothing happens, since the blue edge turns red and a red turns blue. For $x$, the free color was red to begin with, and just turns blue.

For the ending vertex, we'll make the observation that either red or blue has to also be free, because otherwise the path that we took wouldn't be the longest.

TODO: end animation

This means that we've reached a contradiction, since no matter what, we can color the vertex (x, y) using no more than \Delta(G) \le \chi'(G), proving the theorem.

TODO: proof rectangle
