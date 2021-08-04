---
INTRODUCTION
---

In this video, we'll be describing the blossom algorithm for maximal matching in a graph, developed by Jack Edmonds.

As a quick reminder: a graph consists of vertices that are connected by edges.

A matching in a graph is a subset of edges, such that no two of them share a vertex. It is maximal if it contains the most edges possible (compared to other matchings for the given graph), and perfect, if each vertex is in some edge from the matching.

TODO: perfect -- odstranit z toho grafu ty problematické hrany

We'll call vertices that are not in the matching free vertices.

The core idea behind the algorithm is an „alternating path.“ An alternating path in a graph is an alternating sequence of edges in the matching and edges not in the matching. We'll call an alternating path „free,“ if the first and the last vertex is free.

What is interesting about free alternating paths is that if a graph contains it, then its matching is not maximal, because we can switch the edges and improve the matching by 1. Another thing that will be helpful (but we don't be proving, since it's not all that interesting) is that if a graph **doesn't** contain it, then it **is** maximal.

This means that we can repeatedly look for free alternatning paths, improve them and once there are no more, we know that we found a maximal matching.

---
TREE PERFECT MATCHING
---

Let's think about how to find maximal matching in a tree (a graph without cycles).

TODO: ukázat animaci nalevo strom, napravo né strom

We'd like to repeatedly look for free alternating paths, so that we could switch their edges and improve the matching, until it's maximal (just like we described eariler).

To do this a little more systematically, we'll build a forest of alternating paths from all free vertices and then look at all edges not in the pairing.

---
BIPARTITE GRAPH PERFECT MATCHING
---

- add cycles of even length to trees
- show that it doesn't break anything

---
GENERAL GRAPH MATCHING
---

- cycles of odd length suck -- show problem
- introduce blossom
- show that compressing it, finishing matching and uncompressing it doesn't break anything
- visualize algorithm runtime
