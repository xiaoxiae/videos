---
INTRODUCTION
---

# Kids
Imagine you're the head of a summer camp and your task is to group the attendees into pairs. To make the camp's next activity as enjoyable as possible for everyone, you told each attendee to write cards with names of people they'd like to be paired with. Given these cards, you'd now like to create a matching such that the amount of the people that wanted to be with one another is maximal.

To find the matching, you certainly could test all possible options, but this would, for larger groups, take quite a while.

In this video, we'll be describing the blossom algorithm for maximal matching in a graph, developed by Jack Edmonds, a pioneer in many fields of computer science, that can perform this task very efficiently.

# Intro
Formally, a matching in a graph is a subset of edges, such that no two share a vertex. A matching is maximal if it contains the most edges possible compared to other matchings for the given graph.

We'll call vertices that are not in the matching exposed.

# Core
The core idea behind the algorithm are „augmenting paths.“ An augmenting path in a graph with some matching is an alternating sequence of edges in the matching and edges not in the matching, where the first and the last vertex is exposed.

As the name suggests, augmenting paths can improve (or augment) the size of the current matching by switching the unmatched edges on the path with the matched ones.

One thing to note (see the video description for proof) is that a graph **doesn't** contain an augmenting path, if and only if the matching **is** maximal.

This essentially gives us the algorithm -- repeatedly look for augmenting paths, until there are none left, at which point we know the matching is maximal.

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
Although trees are a large family of graphs, most graphs that we would like to run the algorithm on likely won't be a tree, so let's consider a graph our algorithm will not work on.

Imagine we already found a partial matching and would like to further extend it. Running our algorithm here wouldn't work, since the augmenting path is longer than the shortest path.

The problem here is this part of the graph, called the blossom (hence the name of the algorithm). It consists of an odd cycle with alternating edges, and an alternating path ending in an exposed vertex.

Our tree algorithm is still pretty neat and we would like to use it here too. What we'll do is the following:
- first, „compress“ the blossom into a single vertex
- second, find an augmenting path in this new graph and improve the maching
- third, „lift“ the path back to the original graph.

Here, we're relying on the fact that we can always lift the path back, which we won't be proving here (see the video description if you're interested).

# Blossom
- visualize algorithm runtime (left is graph, right is forest)
