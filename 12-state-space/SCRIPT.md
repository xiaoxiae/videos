---
title: Thesesus and the Minotaur (Searching State Space)
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

---
INTRODUCTION
---

\marginpar{\texttt{SceneName}}
Theseus, the Greek hero, has embarked on a journey to find the terrible Minotaur. <!-- write theseus -->
Finding himself deep in the twisting maze of Minos, the Minotaur has been alerted to his presence and starts moving towards him. <!-- animate twice camera out and then camera pan to the right -->
This is rather unfortunate news for Theseus, because in this version of the story, he seems to have forgotten his sword and so his only option is to run away, with Minotaur giving chase -- can he get out before he is caught?

Before solving this slightly tricky question, let's start by looking at a simple version where there is no Minotaur.
You might recognize this as one of the fundamental problems in computer science, that is, finding the shortest path in a maze.
There are a number of algorithms that can to help us solve this problem, but the one we're interested in is BFS.

The idea behind BFS is quite simple: we'll have a queue of positions to explore, starting with the initial one.
Each round, we'll take a position from the queue, add the unexplored positions to it and repeat. <!-- animation of the algorithm on the maze, with the actual queue -->

Let's implement it in Python.

TODO: top-down implementation (starting with the BFS function)
- with the stop_condition thingy

Since we see that we can get out by ourselves in this particular maze, let's see if we can do so with the Minotaur on our tail.

The rules of this new game are the following: for every move Theseus makes (left, right, up and down), the Minotaur can make two (again left, right, up and down). <!-- animate theseus and the minotaur moving -->
Fortunately, the Minotaur isn't particularly bright and so it always moves directly towards Theseus, wherever he is in the maze.
He first checks if he can move closer horizontally, and if this is not the case then he will try to do so vertically, repeating twice.

Here are a few simulated moves for this particular maze.

The key insight for solving this problem is the following: when implemeting BFS, the state that we kept track of was just the position of Theseus.
Now, the state has changed and is the position of Theseus and the position of the Minotaur.
Interestingly, the way we wrote BFS is very general and doesn't care about Theseus or Minotaur, it just takes the oldest state, adds its undiscovered neighbouring states and repeats, meaning that we can use it to solve our Minotaur problem as well!

TODO: implementation

Just to show you that this method can apply to a wide variety of problems, we'll help this frog jump across a bridge filled with holes.
The frog wants to get to the other side in as few jumps as possible without falling, but since it only knows prime numbers, it can jump 2, 3, 5 or 7 tiles at a time.
