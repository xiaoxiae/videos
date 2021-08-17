---
INTRODUCTION
---

# Kids
Imagine you're the head of a summer camp and your task is to group the attendees into pairs. To make the camp's next activity as enjoyable as possible for everyone, you told each attendee to write cards with names of people they'd like to be paired with. Given these cards, you'd now like to create a matching such that the amount of the people that wanted to be with one another is maximal.

Given the cards, we can create a graph with edges between attendees that would like to be with one another (i. e. cards go both ways).

To find the matching, you certainly could test all possible options, but this would, for larger groups, take quite a while. We need something better.

In this video, we'll be describing the blossom algorithm for maximal matching in a graph, developed by Jack Edmonds in 1961.

---

# Intro
Formally, a matching in a graph is a subset of edges, such that no two share a vertex. A matching is maximal if it contains the most edges possible (compared to other matchings for the given graph).

We'll call vertices that are not in the matching exposed vertices.

# Core
The core idea behind the algorithm are „augmenting paths.“ An augmenting path in a graph with some matching is an alternating sequence of edges in the matching and edges not in the matching, where the first and the last vertex is exposed.

On the graph, one such augmenting path is highlighted in red.

As the name suggests, augmenting paths can improve (or augment) the size of the current matching by switching the edges on the path.

One thing to note is that if a graph **doesn't** contain an augmenting path, then the matching **is** maximal. This ensures that we're done when we run out of augmenting paths.

Given that a graph doesn't contain an augmenting path if and only if it is maximal, we've essentially formulated our algorithm -- repeatedly look for augmenting paths, until there are none left, at which point the matching is maximal.

---
TREE PERFECT MATCHING
---

# Tree
First, let's think about how to find augmenting paths in a tree (a graph without cycles). This will be pretty straight-forward -- we'll run a modified BFS from exposed vertices.

Initially, every vertex is exposed, since the pairing is empty.

We'll then pick one exposed vertex at random and run the BFS. If successful, it returns a path that we will alternate, improving the matching and repeating.

Finally, once the matching cannot be improved, the algorithm terminates.

---
GENERAL GRAPH MATCHING
---

# Problem
Let's consider a graph our algorithm won't quite work. Let's say we already found a partial matching and would like to further extend it. Running our algorithm here wouldn't work, since the augmenting path is longer than the shortest path and goes as follows.

TODO: blossom

What we could, however, do, is „compress“ this blossom TODO

- introduce blossom
- show that compressing it, finishing matching and uncompressing it doesn't break anything

- visualize algorithm runtime (left is graph, right is forest)
