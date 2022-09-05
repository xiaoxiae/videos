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
Deep in the twisting maze of Minos, a lone Theseus seeks the mighty minotaur. <!-- just image of the labyrinth -->
After endless days of fruitless searching, the minotaur is alerted to his presense and starts moving towards him. <!-- animate twice camera out and then camera pan to the right; minotaur has question mark above him -->
This is rather unfortunate news for Theseus, because he seems to have forgotten his sword at home and so his only option is to run away -- can he get out before he is caught? <!-- animation of an exclamation point above theseus -->

Before solving this slightly tricky question, let's start by looking at a simple version where there is no Minotaur.
You might recognize this as one of the fundamental problems in computer science, that is, finding the shortest path.
There are a number of algorithms that can help us solve this problem, the simplest one being Breadth-first search (or BFS for short).

The idea behind BFS is very simple: we have a queue of positions (or states) to explore, starting with the initial one.
Each round, we'll take a position from the queue, add its unexplored neighbours and repeat. <!-- animation of the algorithm on the maze, with the actual queue on the side; animating what is explored -->

Let's try implementing it in Python.
TODO: conversion to code

TODO: top-down implementation (starting with the BFS function)
- with the stop_condition thingy

Since we see that Theseus can get out in this particular maze, let's see if we can do so with the Minotaur on his tail.

The rules of this new task are the following: for every move Theseus makes (left, right, up and down), the Minotaur can make two (again left, right, up and down). <!-- animate theseus and the minotaur moving -->
Fortunately, the Minotaur isn't particularly bright and so it always moves directly towards Theseus, wherever he is in the maze.
He does this by first checking if he can move closer horizontally, and if this is not the case then he will try to do so vertically, repeating twice.
Here are a few simulated moves for this particular maze.

Try to pause here for a minute and think about how we could conceptually solve this more difficult problem.

The key insight is the following: in the previous task, the state that we kept track of was just the position of Theseus.
Now, the state has changed and is the position of Theseus and the position of the Minotaur.
However, the way we wrote BFS earlier is very general -- as you can see, it doesn't care about Theseus nor the Minotaur, it just takes an initial state (whatever it might be) and repeatedly adds and explores its neighbouring states, meaning that we can easily re-use it to solve our Minotaur problem!

TODO: implementation

Just to show you that this method can apply to a wide variety of problems, we'll help this frog jump across a bridge filled with holes.
The frog wants to get to the other side in as few jumps as possible without falling, but since it's a frogmatician, it only knows prime numbers and can therefore jump 2, 3, 5 or 7 tiles at a time.

TODO: implementation
