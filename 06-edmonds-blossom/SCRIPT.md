---
INTRODUCTION
---

# Kids
**[k1]:** Imagine you're the head of a summer camp and your task is to group the attendees into pairs. To make it as fair as possible, you told each attendee to write cards with names of people they'd like to be paired with.

**[k2]:** Given these cards, you'd now like to create a matching such that the amount of people that wanted to be with one another is maximum.

**[k3]:** To find the matching, you certainly could test all possible options, but this would, for larger groups, take quite a while.

**[k4]:** In this video, we'll be describing the much faster blossom algorithm for maximum matching in a graph, developed by Jack Edmonds -- a pioneer in many fields of computer science.

---
DEFINITIONS
---

# Intro
**[i1]:** Formally, a graph consists of vertices connected by edges. A matching in a graph is a subset of edges, such that no two share a vertex. A matching is maximum if it contains the most edges possible compared to other matchings for the given graph. We'll call vertices that are not in the matching exposed.

---
CORE IDEA
---

# Core
**[c1]:** The core idea behind the algorithm are „augmenting paths.“ An augmenting path in a graph is an alternating sequence of edges in the matching and edges not in the matching, where the first and the last vertex is exposed.

**[c2]:** As the name suggests, augmenting paths can improve (or augment) the size of the current matching by switching which edges are matched and which are unmatched. As you can see, the matching is still valid, but its size increased by 1 compared to the previous one.

**[c3]:** One thing to note is that a graph contains an augmenting path, if and only if the matching is not maximum (TODO: see description for proof boxík). This means that we can repeatedly improve the matching using augmenting paths, until there are none left, at which point we know the matching is maximum.

---
MAXIMUM TREE MATCHING
---

# Tree
**[t1]:** First, let's think about how to find augmenting paths in a graph without cycles (a tree). This should be pretty straight-forward -- we'll run a breadth-first-search (BFS for short) from exposed vertices, alternating between adding edges not in the matching and edges in the matching.

**[t2]:** The rest of the algorithm just repeatedly improves the matching using augmenting paths and terminates when there aren't any remaining.

**[t3]:** To understand it, it will be best to see it in action.

**[t4]:** Initially, every vertex is exposed, since the matching is empty.

**[t5]:** The algorithm then pick one exposed vertex at random and run the BFS. Here it successfully finds an alternating path, so it uses it to improve the matching and repeats.

\centerline{\em průběh algoritmu (možná bude vypadat trochu jinak)}

**[t6]:** Here is one interesting path that it finds and improves that neatly showcases the layers of the BFS.

\centerline{\em průběh algoritmu}

**[t7]:** Finally, once no augmenting path is found, the algorithm terminates.

---
MAXIMUM GENERAL GRAPH MATCHING
---

# Problem
**[p1]:** Although trees are a large family of graphs, we'd like our algorithm to work on all of them, so let's consider a graph our algorithm will not work on.

**[p2]:** Imagine we already found some a matching that isn't yet maximum and would like to improve it. Running our algorithm here without any changes wouldn't work, since the augmenting path is not the shortest path from the exposed vertex and our algorithm doesn't find it.

**[p3]:** The problem here is this part of the graph. It consists of an odd cycle with alternating edges (called the blossom), and an alternating path ending in an exposed vertex (called the stem). 

**[p4]:** To fix the problem, we'll avoid it -- when we come from the stem into the blossom, we'll do the following:
- first, we'll „contract“ the blossom into a single vertex
- second, we'll find an augmenting path in this new graph
- third, we'll improve the matching using this augmenting path and
- fourth, we'll „lift“ the path back to the original graph

**[p5]:** Here, we are relying on the fact that the graph has an augmenting path if and only if the contracted graph has an augmenting path (TODO: see description for proof boxík).

# Blossom
**[b1]:** Adding this contraction to our algorithm will be pretty straight-forward. Each time we add a new layer of edges, we'll check for blossoms. If found, we will contract the blossom, find the augmenting path in the new graph and then lift back.

\centerline{\em průběh algoritmu}

**[b2]:** Here we can see the contraction in action.

\centerline{\em průběh algoritmu}

# Overview
**[o1]:** Let's compare how fast our algorithm is, compared to a naive solution. For clarity, let $e$ be the number of edges and $v$ the number of vertices.

**[o2]:** When testing all possible combinations, we have to check each subset of edges -- there are $2^e$ subsets (we can either choose an edge or not), so the naive algorithm is exponential.

**[o3]:** On the other hand, an efficiently implemented blossom algorithm will run in $O(e v^2)$, which is polynomial.

TODO: možná ještě nějaká animace k tomuhle?

**[o4]:** To understand why it runs in this time, let's briefly think about what it does. It improves the matching at most $v$-times, during which the entire graph is explored (taking time $e$), but we could recurse up to $v$-times by contracting blossoms. Multiplying this together giving us the aforementioned time complexity.
