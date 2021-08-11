---
INTRODUCTION
---

# Intro
TODO: motivation, this sucks. Imagine you have a group of people,each having preferences regarding who they'd like to be matched with. Your task is to create as many pairs as possible while respecting the preferences (i. e. no two people will be matched).

You certainly could test all possible options, but this would, for larger groups of people, take quite a while. We need something better.

In this video, we'll be describing the blossom algorithm for maximal matching in a graph, developed by Jack Edmonds in 1961.

---

Formally, a matching in a graph is a subset of edges, such that no two share a vertex. A matching is maximal if it contains the most edges possible (compared to other matchings for the given graph).

We'll call vertices that are not in the matching exposed vertices.

# Core
The core idea behind the algorithm are „augmenting paths.“ An augmenting path in a graph with some matching is an alternating sequence of edges in the matching and edges not in the matching, where the first and the last vertex is exposed.

On the graph, one such augmenting path is highlighted in red.

As the name suggests, augmenting paths can improve (or augment) the size of the current matching by switching the edges on the path.

Is essentially the algorithm -- repeatedly look for augmenting paths and use them to improve the matching.

One thing to note is that if a graph **doesn't** contain an augmenting path, then the matching **is** maximal. This ensures that we're done when we run out of augmenting paths.

---
TREE PERFECT MATCHING
---

# Tree
First, let's think about how to find augmenting paths in a tree (a graph without cycles). This will be pretty straight-forward -- run a BFS from some exposed vertex until we find another one.

Initially, all are exposed, since the pairing is empty.

TODO: animace

---
GENERAL GRAPH MATCHING
---

Let's consider a general graph to see why our previous approach doesn't quite work. If we were to run a BFS from this vertex, 

- introduce blossom
- show that compressing it, finishing matching and uncompressing it doesn't break anything

- visualize algorithm runtime (left is graph, right is forest)
