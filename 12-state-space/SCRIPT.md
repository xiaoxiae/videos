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

\marginpar{\texttt{Intro}}
Deep in the twisting maze of Minos, a lone Theseus seeks the mighty Minotaur.
After endless days of fruitless searching, Theseus finally locks eyes with the Minotaur in one of the maze's many long corridors.
The enraged Minotaur lets out a gutteral howl a starts swiftly moving towards him.
This is rather unfortunate news, because Theseus forgot his sword at home and so his only option is to run away from the much faster but not very intelligent Minotaur -- can he get out before he is caught?

Before solving this question, let's start by looking at a simple version where there is no Minotaur.
You might recognize this as one of the fundamental problems in computer science, that is, finding the shortest path in a maze.

There are a number of algorithms that can help us solve this problem, the simplest one being Breadth-first search (or BFS for short).
The idea behind BFS is very simple: we have a queue of states to explore, starting with the initial one.
In our case, the 'states' are the just the possible positions Theseus can move to.
Each round, we'll take a state from the queue, add its undiscovered neighbouring states to the queue and repeat, until the queue is either empty or we found what we're looking for.
Speeding this up a bit, we see that the algorithm indeed finds the shortest path, which is nothing surprising.

\marginpar{\texttt{BFS}}
Now from the visualizations, it seems very intuitive, but let's actually try to implement it in Python.

The input will be a list of strings containing the rows of the maze.
We'll need the position of Theseus and the position of the escape, which are denoted as `T` and `E`, so let's add some code to find them.

Now if you've never implemented BFS then what to do next isn't all that clear.
This can happen quite often when coding something new, and a good way to overcome this is to write some smaller but useful functions what will help with the core of the algorithm.

For example, we'll definitely need to check if a position can even be moved to.
We'll therefore create the `is_valid` function that does exactly that, returning True if the position is not a wall, else returning False.

Speaking of states, we'll also need a function that given some state will return the neighbouring states (call it `next_states`).
The function will check each direction (left, right, up and down), and if the new state is valid (using the `is_valid` function), it will be added to the list of states, which is returned at the end.

Finally, given these two functions, let's tackle the BFS itself.
It will need two arguments: a starting state and a stop condition, which will be a function that takes in a state and returns True if it's an ending one, so the algorithm know when to stop searching.
You might be thinking that this is a bit pointless, since we could just pass the position of the escape and check against it when running the algorithm and while this is true, this generality allows us to support things like multiple escape tiles, which would be impossible when only providing one ending state.

As we've previously discussed, the algorithm uses a queue of states to explore, beginning with the starting one.
To record the states that we've already discovered and don't want to add to the queue again, we'll use Python's built-in set.

The rest of the function essentially writes itself from the way we previously described the algorithm: while the queue isn't empty, we'll take a state from the queue, check the stop condition (possibly reporting a solution) and finally add its undiscovered neighbouring states to the queue and mark them discovered.
If we didn't find an ending state, we'll report that no solution exists.

Implemented like this, the algorithm is a bit useless, because it just says that the solution exists, not what it actually looks like.
We'd ideally like to see the path that Theseus took to get out of the labyrinth, and for that we'll need to slightly modify the code.
The main idea is that instead of just recording that we discovered a state, we'll remember from which state it was discovered, so we can later backtrack from the ending state to the starting one.

To do this, we'll use a dictionary instead of a set, with the keys being discovered states and values their predecessors.
Since the initial state doesn't have a predecessor, we'll just make it None.
Also, when adding a new state, we'll make sure to remember its predecessor.

Now we can add the backtracking code.
There isn't anything too complicated here -- we start with the ending state and while it has a predecessor, we append the predecessor to the path and move to it.
Finally, we print the path in reverse, because we backtracked but would actually like the path printed from start to end.

We can now call the BFS function with Theseus' starting position and a stop condition, which will return True if the state is the position of escape.

Running the code, we see that Theseus can indeed get out of this particular maze.

\marginpar{\texttt{MinotaurMovement}}
Let's see if we can still do so with the Minotaur on his tail.
For every move Theseus makes, right, up and down), the Minotaur makes two.
Fortunately, the Minotaur isn't particularly bright and so it always moves directly towards Theseus, wherever he is in the maze.
He does this by first checking if he can move closer horizontally, and if this is not the case then he will try to do so vertically, repeating twice.
Here are a few simulated moves for this particular maze.

Try to pause here for a minute and think about how we could approach this slightly more difficult problem.
The key insight is the following: in the previous task, the state was just the position of Theseus.
Now, the state is a pair of positions: the position of Theseus and the position of the Minotaur.

On the surface, it seems like this makes the problem fundamentally more difficult, but it actually doesn't.

\marginpar{\texttt{BFSMinotaur}}
The way we wrote the function BFS earlier is very general -- it doesn't care about neither Theseus nor the Minotaur; it just takes an initial state and a stop condition, whatever they might be, and repeatedly adds and explores neighbouring states, meaning that we can re-use it to solve our Minotaur problem!

For starters, let's add the Minotaur to the maze, say here.
We'll have to find it, so let's add some code to do that.
Next, we'll have to rename the `next_states` function, because now it only returns the next possible positions of Theseus, completely ignoring the Minotaur.
Let's make it `next_theseus_positions`.

Now let's make the Minotaur move.
For this, we'll first write a small function that returns -1, 0 or 1 depending on whether a value is smaller, equal or larger to another value.
This is essential for the Minotaur movement, since it performs this exact calculation to move closer both horizontally and vertically.
The main function is quite TODO

TODO: add next_moves

TODO: implementation

TODO: animatoin for if theseus can get out from the original larger maze

Just to show you that this method can apply to quite a wide variety of problems, we'll help this frog jump across a bridge filled with holes.
It wants to get to the other side in as few jumps as possible without falling, but since it's a frogmatician, it only knows prime numbers and can therefore only jump 2, 3, 5 or 7 tiles at a time (either forward or backward).

TODO: implementation
