# Vizing's theorem
In this video, we'll be proving Vizing's theorem, which puts an upper and lower bound on the number of colors needed to edge-color a graph. An edge coloring is valid, if no vertex contains edges of the same color.

## Theorem (Intro)
More precisely, the theorem states that the number of colors chi prime needed to edge-color a graph is between the degree of the graph \Delta(G) and the degree of the graph plus one.

## - (Degree)
As a reminder, the degree of a vertex is the number of its edges, and the degree of the entire graph is the maximum degree of its vertices.

## Example (Example)
Let's look at an example graph. We can use 3 colors to color its edges, which also happens to be its degree. However, adding additional two edges like so doesn't change the degree, but increases the number of colors needed by one.

## Lower bound (LowerBound)
Proving the lower bound is simple. Looking at a vertex with degree \Delta(G), we obviously need as many colors as the number of its edges.

Before proving the upper bound, let's make a quick observation that will be useful during the proof.

## - (FreeColor)
When we have \Delta(G) + 1 colors, each vertex of the graph has at least one free color. By free, we mean that it doesn't have an edge of this color. If some adjacent vertex also has this color, they can switch the color of the edge between them with their free color, without breaking the coloring.

This makes sense, because we have one more color than the degree of the graph.

## Upper bound (UpperBound)
We'll prove the upper bound using a contradiction. Let's assume that we can't in fact color some graph $G$ using chi prime + 1 colors. This means that whichever way we color the graph, we'll always have some uncolored edge (x, y).

From the previous observation, we know that $x$ has some free color. $y$ can't have this free color, because we could then color the edge (x, y) using it, so it has to have one that $x$ doesn't. Because $x$ doesn't have it, there must be an edge with this color from $x$ to some other vertex, which also has some free color.

This chain can go on a bit, but eventually, one of two things will happen.

Case one is that the free color of the last vertex in the chain is the free color of $x$. In this case, we'll go back the chain and change colors, like so. This frees up the color for $x$ that we needed to color (x, y) and we've reached a contradiction.

Case two is that the free color of the last vertex is the color of an edge from $x$ that we've seen before. This is unfortunate, since we're now stuck in a loop and can't use the previous trick.

In this case, we'll take the longest path from $w$ of alternating free colors of $x$ and $v$, and switch its colors. We're doing this to remove the loop by freeing up a different color for $x$.

Let's think about why this doesn't break the coloring.

For vertices in between, nothing happens. For $x$, the free color was red to begin with, so it just turns blue. For the ending vertex, we'll make the observation that either red or blue must have been free, because otherwise the path that we took wasn't the longest.

We've now reduced the problem to case one, which we know reaches a contradiction, proving the upper bound.

Combining the lower and upper bound, we see that no matter what, we can always color any graph using either \Delta(G) or \Delta(G) + 1 colors.
