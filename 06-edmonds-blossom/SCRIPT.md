---
INTRODUCTION
---

# Kids
**[k1]:** Imagine you're the head of a summer camp and your task is to group the attendees into pairs. To make it as fair as possible, you told each attendee to write cards with names of people they'd like to be paired with.

**[k2]:** Given these cards, you'd now like to find a matching (which, in this case, means the same thing as pairing) such that the amount of people that wanted to be with one another is maximum.

**[k3]:** You certainly could test all possible combinations, but this would, for larger groups, take quite a while. In this video, we'll be describing the much faster blossom algorithm for maximum matching in a graph, developed by Jack Edmonds -- a pioneer in many fields of computer science.

---
DEFINITIONS
---

# Intro
**[i1]:** Formally, a graph consists of vertices connected by edges. A matching in a graph is a subset of edges, such that no two share a vertex.

**[i2]:** A matching is maximum if it contains the most edges possible compared to other matchings for the given graph. Also, we'll call vertices that are not in the matching exposed.

---
CORE IDEA
---

# Core
**[c1]:** The core idea behind the algorithm are „augmenting paths.“ An augmenting path in a graph is an alternating sequence of matched and unmatched edges, where the first and the last vertex is exposed.

**[c2]:** As the name suggests, augmenting paths can improve (or augment) the size of the current matching by switching the matched and unmatched edges. As you can see, the matching is still valid, but its size increased by 1.

**[c3]:** One thing to note is that a graph contains an augmenting path, if and only if the matching is not maximum. This means that we can repeatedly improve the matching using augmenting paths, until there are none left, at which point we know the matching is maximum.

---
MAXIMUM TREE MATCHING
---

# Tree
**[t1]:** Let's think about how to find augmenting paths in a tree. This is pretty straight-forward -- we'll run a breadth-first-search (or BFS for short) from exposed vertices, alternating between adding matched and unmatched edges.

**[t2]:** The rest of the algorithm repeatedly improves the matching using augmenting paths and terminates when there aren't any remaining. To better understand how this all works, it will be best to see an example.

**[t3]:** Initially, every vertex is exposed, since the matching is empty.

**[t4]:** The algorithm then picks one exposed vertex at random and run the BFS. Here it successfully finds an augmenting path, so it uses it to improve the matching and repeats.

**[t5]:** Let's fast-forward a bit until some larger augmenting path is found.

**[t6]:** Here is a longer path that the algorithm finds that neatly showcases the alternating edges.

**[t7]:** Finally, once no augmenting path is found, the algorithm terminates.

---
MAXIMUM GENERAL GRAPH MATCHING
---

# Problem
**[p1]:** Although trees are a large family of graphs, we'd like our algorithm to work on all of them, so let's look at a graph our algorithm will not work on.

**[p2]:** Imagine we already found some matching that isn't yet maximum and would like to improve it. Running the algorithm here wouldn't work, since the augmenting path is longer than the shortest path and is therefore not found.

**[p3]:** The problem here is this part of the graph. It consists of an odd cycle with alternating edges called the blossom, hence the name of the algorithm, and an alternating path ending in an exposed vertex called the stem.

**[p4]:** To fix the problem, we'll avoid it -- when we come from the stem into the blossom, we'll do the following:

**[p5]:**

1. we'll „contract“ the blossom into a single vertex
2. we'll find an augmenting path in this new graph
3. we'll improve the matching using this augmenting path and
4. we'll „lift“ the path back to the original graph

**[p6]:** Here, we are relying on the fact that the graph has an augmenting path if and only if the contracted graph has an augmenting path.

# Blossom
**[b1]:** Adding this operation to our algorithm will be pretty straight-forward. Each time we add unmatched edges, we'll check for blossoms. If found, we will contract the blossom, find the augmenting path in the new graph and then lift back.

**[b2]:** The rest of the algorithm hasn't changed at all. As you can see, it does exactly what it did before, so we'll again fast-forward a bit until something interesting happens.

**[b3]:** Here we can see the contraction in action. Once it finds the blossom, it contracts it, runs the algorithm again on the smaller graph, finds the augmenting path, improves the matching and then lifts back.

**[b4]:** After this, it terminates, since there are no more augmenting paths.

# Overview
**[o1]:** Let's compare how fast our algorithm is to a naive solution. For clarity, let $e$ be the number of edges and $v$ the number of vertices.

**[o2]:** When testing all possible combinations, we have to check each subset of edges. The number of subsets is $2^e$ (each edge either is in a subset or not), so the naive algorithm is exponential.

**[o3]:** As for the blossom algorithm: it improves the matching at most $v$-times, during which the entire graph is explored (taking time $e$), but we could contract up to $v$-times. Multiplying this together gives us the time complexity $e v^2$, which is polynomial and exponentially better than the naive solution.

**[o4]:** But, if there are only 6 attendees of your summer camp, you can probably do it by hand.
