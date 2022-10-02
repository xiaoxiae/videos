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
This is rather unfortunate news for Theseus, because he seems to have forgotten his sword at home and so his only option is to run away from the much faster but not very intelligent minotaur -- can he get out before he is caught? <!-- animation of an exclamation point above theseus -->

Before solving this slightly tricky question, let's start by looking at a simple version where there is no Minotaur.
You might recognize this as one of the fundamental problems in computer science, that is, finding the shortest path in a maze.

There are a number of algorithms that can help us solve this problem, the simplest one being Breadth-first search (or BFS for short). <!--  --> The idea behind BFS is very simple: we have a queue of states to explore, starting with the initial one.
In our case, the 'states' are the possible positions Theseus can move to.
Each round, we'll take a state from the queue, add its undiscovered neighbouring states to the queue and repeat, until the queue is either empty or we've found what we're looking for. <!-- animation of the algorithm on the maze, with the actual queue on the side; animating what is explored -->

Let's try implementing it in Python.

The input will be a list of strings containing the rows of the maze.
We'll definitely need the position of Theseus and the position of the escape tile, so let's just add some code to find them.

Now if you've ever implemented BFS then the next steps are quite obvious, but for those that haven't, they aren't all that clear.
Well, wherever we're coding and get to a position where we aren't sure what to do, a good thing to try is to write smaller functions that seem like they can be useful.

For example, we'll definitely need to check if a tile can be moved to (since Theseus isn't a ghost).
We'll therefore create the `is_valid` function that will return True if the given state can be moved to, else False.

Speaking of states, we'll definitely need a function that given some state will return the valid neighbouring states (call it `next_states`).
The function will each direction (left, right, up and down).
If the new state is valid (using the `is_valid` function we implemented earlier), it will be added to the list of states, returning it at the end.

Finally, given these two functions, we'll be able to tackle the BFS itself.
It will need two arguments: the starting state, which will be the initial position of Theseus, and a stop condition, which will be a function that takes in a state and returns True if it's an ending one, so the algorithm know when to stop searching.
You might be thinking that this is a bit pointless, since we could just pass the position of the end and check against it when running the algorithm, but this generality allows us to support things like multiple escape tiles, which would be impossible when only providing one ending state.

As we've previously discussed, the algorithm uses a queue of states to explore, beginning with the starting one.
To record the states that we've already discovered and don't want to add to the queue again, we'll use Python's built-in set data structure.

The rest of the function essentially writes itself from the way we previously described the algorithm: while the queue isn't empty, we'll take a state from the queue, check the stop condition (possibly reporting a solution) and finally add its undiscovered neighbouring states to the queue and mark them discovered.
If we didn't find an ending state, we'll report that no solution exists.

We can now call the BFS with Theseus' starting position and a stop condition, which will return True if the state is the ending one.

Written like this, the algorithm is a bit underwhelming, because it just says that the solution exists, not what it actually looks like.
We'd ideally like to see the path that Theseus took to get out of the labyrinth, and for that we'll need to slightly modify the code.
The main idea is that instead of recording that we discovered a state, we'll additionally remember from which state it was discovered, so we can later backtrack from the ending state to the starting one.

To do this, we'll use a dictionary instead of a set, with the keys being discovered states and values their predecessors.
The initial state doesn't have a predecessor so we'll make it None.
When adding a new state, we'll make sure to remember its predecessor.

Now we can add the backtracking code.
There isn't anything too exciting

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
