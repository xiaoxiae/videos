---
INTRODUCTION
---

# Kids
Imagine you're the head of a summer camp and your task is to group the attendees into pairs. To make the camp's next activity as enjoyable as possible, you told each attendee to write cards with names of people they'd like to be paired with. Given these cards, you'd now like to create a matching such that the amount of people that wanted to be with one another is maximal.

To find the matching, you certainly could test all possible options, but this would, for larger groups, take quite a while.

In this video, we'll be describing the blossom algorithm for maximum matching in a graph, developed by Jack Edmonds, a pioneer in many fields of computer science, that can perform this task very efficiently.

# Intro
Formally, a matching in a graph is a subset of edges, such that no two share a vertex. A matching is maximum if it contains the most edges possible compared to other matchings for the given graph.

We'll call vertices that are not in the matching exposed.

# Core
The core idea behind the algorithm are „augmenting paths.“ An augmenting path in a graph is an alternating sequence of edges in the matching and edges not in the matching, where the first and the last vertex is exposed.

As the name suggests, augmenting paths can improve (or augment) the size of the current matching by switching the unmatched edges on the path with the matched ones.

One thing to note is that a graph **doesn't** contain an augmenting path, if and only if the matching **is** maximum (see the description for proof).

This essentially gives us the algorithm -- repeatedly look for augmenting paths, until there are none left, at which point we know the matching is maximum.

---
TREE PERFECT MATCHING
---

# Tree
First, let's think about how to find augmenting paths in a tree (a graph without cycles). This will be pretty straight-forward -- we'll repeatedly run a modified BFS from exposed vertices.

Initially, every vertex is exposed, since the matching is empty.

We'll then pick one exposed vertex at random and run the BFS. If successful, it returns a path that we will alternate, improving the matching and repeating.

Finally, once the matching cannot be improved, the algorithm terminates.
---
GENERAL GRAPH MATCHING
---

# Problem
Although trees are a large family of graphs, we'd like our algorithm to work on any kind of graph, so let's consider a graph our algorithm will not work on.

Imagine we already found a partial matching and would like to further extend it. Running our algorithm here wouldn't work, since the augmenting path is longer than the shortest path.

The problem here is this part of the graph. It consists of an odd cycle with alternating edges (called the blossom), and an alternating path ending in an exposed vertex (called the stem).

The idea of finding augmenting paths is still pretty solid. To make it work here, we'll do the following:
- first, „contract“ the blossom into a single vertex, creating a new graph
- second, find an augmenting path in this new graph
- third, improve the maching using this augmenting path and
- fourth, „lift“ the path back to the original graph

Here, we're relying on the fact that the graph has an augmenting path if and only if the contracted graph has an augmenting path (see the description for proof).

# Blossom
Here is our algorithm in action. Although a little tricky to implement, the core idea is the contraction of the blossoms when they are encountered, recursion onto the newly formed graph, and lifting of the path back to the original graph.

# Overview
At the beginning of the video, we mentioned that this algorithm will be fast. So how fast is it, compared to testing all possible combinations?

Well, to begin with, testing all possible combinations naively means testing all subsets of edges, which there are about $2^{number of edges}$. On the other hand, an effitiently implemented blossom algorithm runs in $O(|E| |V|^2)$, which is much, much better.

It runs in this time, because the matching will improve at most $|V|$-times and in each iteration the entire graph is explored, which could take, in the worst case (if we compressed blossoms a lot) $|E| |V|$.

TODO: overview

TODO: outro - bigger graph
