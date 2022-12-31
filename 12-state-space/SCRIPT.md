---
title: Thesesus and the Minotaur | Exploring State Space
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

---
Introduction
---

\marginpar{\texttt{Intro}}
Deep in the twisting maze of Minos, a lone Theseus seeks the mighty Minotaur.
After endless days of fruitless searching, Theseus finally locks eyes with the Minotaur in one of the maze's many long corridors.
\marginpar{Tady nějaká vhodná hudba.}
The enraged Minotaur lets out a gutteral howl a starts swiftly moving towards him.
This is rather unfortunate news, because Theseus forgot his sword at home and so his only option is to run away from the much faster but not very intelligent Minotaur -- can he get out before he is caught?

Before solving this question, let's start by looking at a simple version where there is no Minotaur.
You might recognize this as one of the fundamental problems in computer science, that is, finding the shortest path.

There are a number of algorithms that can help us solve this problem, the simplest one being Breadth-first search (or BFS for short).
The idea behind BFS is the following: we have a queue of states to explore, starting with the initial one.
In this problem, the 'states' are the positions Theseus can move to. <!-- MINOR: divný překrývání -->
Each round, we'll take a state from the queue, add its undiscovered neighbouring states to the queue and repeat, until the queue is either empty or we found what we're looking for.
Speeding this up a bit, we see that the algorithm indeed finds the shortest path.

---
Implementation
---

\marginpar{\texttt{BFS}}
From the visualizations, the algorithm seems very intuitive, but let's actually try to implement it in Python.

The input will be a list of strings containing the rows of the maze.
We'll need to extract the positions of Theseus and the escape, which are denoted as `T` and `E`, so let's add some code to do that.

Now if you've never implemented BFS then what to do next isn't all that clear.
This can happen quite often when coding something new, and a good way to overcome this is to write small functions that seem like they could be useful.

For example, we can write an `is_position_valid` function that returns True if the position can be moved to.

From the decription of the algorithm, we'll also need a `next_states` function that returns the neighbouring states of a given state.
The function will check each direction (left, right, up and down), and if the new state is valid, it will be added to the list of states, which is returned at the end.

Given these two small functions, we can tackle the BFS itself.
It will take two arguments: a starting state and a stop condition, which will be a function that takes in a state and returns True if it's an ending one, so the algorithm knows when to stop searching.
You might be thinking that this is a bit pointless, since we could just pass the position of the escape and check against it when running the algorithm and while this is true, this allows us to support more complex ways of ending the BFS (say if there were multiple escapes). <!-- is this pointless? then transform into allows us -->

As we've previously discussed, the algorithm uses a queue of states to explore, beginning with the starting one.
To record the states that we've already discovered and don't want to add to the queue again, we'll use Python's built-in set.

The rest of the function essentially writes itself from the way we previously described the algorithm: while the queue isn't empty, we'll take a state from the queue, check the stop condition (possibly reporting a solution)<!-- faster write --> and add its undiscovered neighbouring states to the queue, marking them discovered to not add them to the queue again. <!-- marking them discovered separate -->
Finally, If we didn't find an ending state after exploring all of them, we'll report that no solution exists.

Implemented like this, the algorithm is useless, because it just reports that the solution exists, not what it actually looks like. <!-- highlight solution found -->
We'd ideally like to see the path that Theseus took, and for that we'll need to slightly modify our code.
Instead of just recording that we discovered a state, we'll remember from which state it was discovered so we can later backtrack.

To do this, we'll use a dictionary instead of a set, with the keys being discovered states and values their predecessors.
Since the initial state doesn't have a predecessor, we'll make it None.
When adding a new state, we'll make sure to remember its predecessor.

TODO: nit

Now we can add the backtracking code.
There isn't anything too complicated here -- we start with the ending state and while it has a predecessor, we move to it and append it to the path.
Finally, we print the path in reverse, because we'd like it printed from start to end.

We can now call the BFS function with Theseus' starting position and a stop condition that returns True if the given state is the escape. <!-- the camera should be much more down -->
As we see, Theseus can indeed get out of this particular maze. <!-- move immediately to the maze and solution found, not first write solution found -->

---
Adding the Minotaur
---

\marginpar{\texttt{MinotaurMovement}}
Let's get back to the original problem.

For every move Theseus makes (left, right, up and down), the Minotaur makes two.
Fortunately, the Minotaur isn't particularly bright and so it always moves directly towards Theseus, wherever he is in the maze.
He does this by first checking if he can move closer horizontally, and if this is not the case then he will try to do so vertically, repeating twice.
Here are a few simulated moves for this particular configuration.

Try to pause here for a minute and think about how we could approach this seemingly more difficult problem.

The key insight is the following: in the previous task, the state was the position of Theseus.
Now, the state is a pair of positions of Theseus and the Minotaur.
In terms of their validity, they must be outside of the wall and, additionally, Theseus' position can't equal Minotaur's because he would be dead.

Besides these things, notice that the problem fundamentally didn't change -- we still have a state which we can use to generate neighbouring states and thus again use BFS.

\marginpar{\texttt{BFSMinotaur}}
Recall that the way we wrote the function BFS was very general -- it doesn't care about Theseus or the Minotaur; it just takes an initial state and a stop condition, whatever they might be, and repeatedly adds and explores neighbouring states via the `next_states` function, meaning that we can reuse it to solve our Minotaur problem!

For starters, let's add the Minotaur to the maze, say here.
We'll have to find it, so let's add some code to do that.
Although the BFS function doesn't change, the way we call it does, since the state is now a `(theseus, minotaur)` tuple and the stop condition only checks if Theseus escaped, not the Minotaur.

We'll also rename the `next_states` function, because it now only returns the next possible positions of Theseus.

To implement a proper `next_states` function for this problem, we'll first need a function that moves the Minotaur towards Theseus.
To do this, we'll first write a small function that moves the Minotaur in one dimension, returning +1, 0 or -1 based on on how it should move horizontally or vertically to get closer to Theseus. <!-- highight +1 0 1 -->
Just to see what the function does, here are a few examples of what it returns for specific input values. <!-- fade this in --> <!-- returns -> prints -->

The main function for Minotaur movement then uses this function to attempt to move closer to Theseus horizontally and, if not successful, vertically, repeating twice. <!-- highlight repeating twice (the entire block) -->

With these two functions, we can finally write the missing `next_states` function: given some state, Theseus attempts to move in all directions and Minotaur follows suit.
If he catches Theseus, the state is invalid, else it's fine.

Running the code now, we see that the path is quite a bit longer, since Theseus has to lead the Minotaur into a corner and only then escape. <!-- opět přímo vykreslit maze -->

---
Summary
---

As you can see, we implemented a general algorithm to solve problems where you need to get from one state to another in the least amount of steps possible (i.e. explore the state space). <!-- TODO is in the code -->
This is great, because problems that involve the state space are quite common and recognizing them will save you a lot of headache when trying to solve them in ways other than BFS. <!-- animace -->

---
Advent of Code 2022 (day 19)
---

\marginpar{\texttt{AOC}}
And, just to show you that this is not limited to problems on a 2D board, here is a really fun one taken from the Advent of Code 2022, day 19.

\marginpar{\texttt{Robots}}
There are 4 types of robots, each producing one of the following resources: ore, clay, obsidian and geode. <!-- split -->
Each robot produces one resource per minute (so if you have 4 ore robots, they produce 4 ore a minute). <!-- combine showing minutes and robot count -->
Besides this, you have a factory that can build a new robot in one minute, given a specific number of resources:
- the ore robot costs 4 ore
- the clay robot costs 2 ore
- the obsidian robot costs 3 ore and 14 clay and
- the geode robot costs 2 ore and 7 obsidian

The factory takes a whole minute building the robot, meaning that during a minute, the factory first subtracts the resources required to build the robot, the robots then produce their respective resources and finally the robot is finished. <!-- this has to be timed well -->

We start with one ore robot and no resources.
By building the robots in a specific order, we want to maximize the number of geodes produced after the first 24 minutes. <!-- show this in the top right corner -->

For these particular costs of the robots, here is the optimal solution.
As you can see, the maximum number of geodes is 9. <!-- highlight the number of geodes -->

Pause here and think of what the states are and how to get from one to another.

The state here is the current number of resources and robots, but also the remaining time, since states with zero or negative remaining time are invalid. <!-- show t -->
Getting from one state to another always means decreasing the remaining time by one, adding the resources that the robots acquired and attempting to build all possible robots. <!-- TODO: do this -->
Here is what the graph of the first few states looks like.

\marginpar{\texttt{RobotGraph}}
This solution works but wouldn't terminate in a reasonable amount of time because of the branching factor.
The branching factor is, for our purposes, the average number of neighbouring states.
For our problem, this is about 5 since, in each minute, we can either do nothing or build one of the 4 types of robots.

While there problem doesn't branch too much initially, the more resources you acquire, the more options you will have, meaning that getting to depth 24 of this tree will be extremely slow with a simple BFS. <!-- add the graph from 0 to 24 here -->
So is this entirely hopeless?

Well, no, there are a few things we can do.
The techniques we'll look into are twofold: pruning and prioritization.

Let's first look at pruning.

---
Pruning
---

Pruning is the technique of removing valid states from the search that you know aren't going to lead to the right solution.

For example, let's look at a branch where only ore robots are built.
It certainly is a valid branch but we know that it won't produce the correct result, because building more ore robots than a the highest requirement for ore is pointless (i.e. if the most amount of ore we can spend on constructing a robot is 3, it is sufficient to build only 3 ore robots).
We can therefore remove (or prune) states that build more robots than necessary and speed up the algorithm.

Furthermore, when we do find states that obtain some geodes, we can start pruning states that couldn't improve this number even if they build a geode robot every minute, achieving furher speedup.

While these strategies do help, as the graph shows, we'll need something better and for that, let's go back to the shortest path problem.

---
Prioritization
---

Until now, we used the good old BFS with a queue to process states.
However, it might be a good idea to "prioritize" states that look more promising over others. <!-- animate by color states that are closer to the escape -->
In this maze, states that are closer to the escape (in terms of their $(x, y)$) coordinates should be explored before those that are further.

For us to do this, there are two things that we have to change:
