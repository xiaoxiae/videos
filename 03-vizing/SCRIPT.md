# Vizing's theorem
[v1] In this video, we'll be proving Vizing's theorem, which puts an upper and lower bound on the number of colors needed to edge-color a graph.

[v2] An edge coloring is valid, if no vertex contains edges of the same color. For example, this is a vaild edge coloring, while this is not.

## Theorem (Intro)
[t1] The theorem states that the number of colors chi prime needed to edge-color a graph is between the maximum [[degree]] of the graph \Delta(G) and the maximum degree of the graph plus one.

## - (Degree)
[d1] As a reminder, the degree of a vertex is the number of edges containing it, and the maximum degree of the graph is the maximum degree of its vertices.

## Example (Example)
*[e1] Let's look at an example graph. We can use 3 colors to color its edges, which also happens to be its maximum degree. However, adding additional two edges like so doesn't change the maximum degree, but increases the number of colors needed by one.

## Lower bound (LowerBound)
[l1] Proving the lower bound is simple. Looking at a vertex with degree \Delta(G), we obviously need as many colors as the number of its edges.

## - (FreeColor)
[f1] Before proving the upper bound, let's make a quick observation that will be useful during the proof.

[f2] When we have \Delta(G) + 1 colors, each vertex of the graph has at least one free color. By free, we mean that the vertex doesn't have an edge of this color.

*[f3] This makes sense, because we have one more color than the maximum degree of the graph.

[f4] Additionally, if an adjacent vertex also has this free color, they can switch the free color and the color of the edge between them, without breaking the coloring.

## Upper bound (UpperBound)
[u1] We'll prove the upper bound constructively. Let's assume that we have some partial coloring of $G$ using chi prime + 1 colors, and want to color some edge (x, y).

[u2] From the previous observation, we know that $x$ has some free color. If $y$ has the same free color, then we can color the edge (x, y) using it.

[u3] If $x$ doesn't have this free color, there must be an edge with this color from $x$ to some other vertex, which also has some free color.

[u4] This chain can go on a bit, but eventually, one of two things will happen.

[u5] Case one is that the free color of the last vertex in the chain is the free color of $x$. In this case, we'll go back the chain and change colors. This frees up the color for $x$ that we needed to color (x, y) and we're done.

[u6] Case two is that the free color of the last vertex is a color of an edge from $x$ that we've seen before. This is unfortunate, since we're now stuck in a loop and can't use the previous trick.

[u7] In this case, we'll take the longest path from $v$ of alternating free colors of $x$ and $u$, and switch the colors on this path. We're doing this to get rid of the loop. However, since this path can end up pretty much anywhere, we'll again have to consider two possibilities.

[u8] The first is that the path ends in the vertex right before $v$, let's call it $w$. Notice that by switching, we reduced the problem to case 1, only with blue and red reversed.

[u9] The second is that the path doesn't end in $w$. This is even better, since $x$ and $w$ now have the same color and we again reduced the problem to case 1.

[u10] It's also good to realize that the switch operation doesn't break the coloring, since we would then have a neat, but invalid proof.

[u11] For vertices other than the first and the last, nothing happens, since they still have edges of the same colors. For $x$, the free color was red to begin with, so it just turns blue. For the ending vertex, we'll make the observation that either red or blue must have been free, because otherwise the path that we took wasn't the longest.

[u12] Combining the lower and upper bound, we see that no matter what, we can always color any graph using either \Delta(G) or \Delta(G) + 1 colors.
