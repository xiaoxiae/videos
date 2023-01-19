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
Introduction (BFS)
---

\marginpar{\texttt{Intro}}
Deep in the twisting maze of Minos, a lone Theseus seeks the mighty Minotaur.
After endless days of fruitless searchin, Theseus locks eyes with the Minotaur in one of the maze's many corridors.
\marginpar{Tady nějaká vhodná dramatická hudba.}
The enraged Minotaur lets out a gutteral howl a starts moving towards him.
This is rather unfortunate news, because Theseus forgot his sword at home and so his only option is to run away from the much faster but not very intelligent Minotaur -- can he get out before he is caught?

Before solving this question, let's start by looking at a simple version where there is no Minotaur.
You might recognize this as one of the fundamental problems in computer science, that is, finding the shortest path.

There are a number of algorithms that can help us solve this problem, the simplest one being Breadth-first Search (or BFS for short).
The idea behind BFS is the following: we have a queue of states to explore, starting with the initial one.
In this problem, the set of states (formally the state space) are the positions Theseus can move to.
Each round, we'll take a state from the queue, add its undiscovered neighbouring states to the queue and repeat, until the queue is either empty or we found what we're looking for.
Speeding this up a bit, we see that the algorithm indeed finds the shortest path.

---
Implementation
---

\marginpar{\texttt{BFS}}
From the visualizations, the algorithm seems intuitive, but let's actually try to implement it in Python.

The input will be a list of strings containing the rows of the maze.
We'll need to extract the positions of Theseus and the escape, which are denoted as `T` and `E`, so let's add some code to do that.

Now if you've never implemented BFS then what to do next isn't all that clear.
This can happen quite often when coding something new, and a good way to overcome this is to write small functions that seem like they could be useful.

For example, we can write an `is_position_valid` function that returns True if the position can be moved to (i.e. is within the maze and isn't a wall).

From the decription of the algorithm, we'll also need a `next_states` function that returns the neighbouring states of a given state.
The function will check each direction (left, right, up and down), and if the new state is valid, it will be added to the list, which is returned at the end.

Given these two small functions, we can tackle the BFS itself.
It will take two arguments: a starting state and a stop condition, which will be a function that takes in a state and returns True if it's an ending one, so the algorithm knows when to stop searching.
You might be thinking that this is a bit pointless, since we could just pass the position of the escape and check against it when running the algorithm and while this is true, this way allows us to support more complex ways of ending the BFS like multiple escape tiles.

As we've previously discussed, the algorithm uses a queue of states to explore, beginning with the starting one.
To record the states that we've already discovered and don't want to add to the queue again, we'll use Python's built-in set.

The rest of the function essentially writes itself from the way we previously described the algorithm: while the queue isn't empty, we'll take a state from the queue, check the stop condition (possibly reporting a solution) and add its undiscovered neighbouring states to the queue, marking them discovered to not add them to the queue again.
Finally, if we didn't find an ending state after exploring all of them, we'll report that no solution exists.

Implemented like this, the algorithm is useless, because it just reports that the solution exists, not what it actually looks like.
We'd ideally like to see the path that Theseus took, and for that we'll need to slightly modify our code.
Instead of just recording that we discovered a state, we'll remember from which state it was discovered so we can later backtrack.

To do this, we'll use a dictionary instead of a set for storing discovered states, with the keys being states themselves and values their predecessors.
Since the initial state doesn't have a predecessor, we'll make it None.
When discovering a new state, we'll make sure to remember its predecessor.

Now we can add the backtracking code.
There isn't anything too complicated here -- we start with the ending state and while it has a predecessor, we'll move to it and append it to the path.
Finally, we print the path in reverse, because we'd like it printed from start to end, not the other way around.

One small note here: for clarity of code, I wanted to exclude importing libraries, so I used a list as a queue here. <!-- highlight stuff -->
That is a terrible idea, because popping from the beginning takes linear time -- in practice, you should use Python `collections` module and its `deque` class, which has a popleft operation that is constant. <!-- remove highlights here -->

Now we can finally call the BFS function with Theseus' starting position and a stop condition that returns True if the given state is the escape.

And, as we see, Theseus can indeed escape this particular maze.

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

The key idea is the following: in the previous task, the state was the position of Theseus.
Now, the state becomes a pair of positions of Theseus and the Minotaur.
In terms of their validity, they must be outside of the wall and, additionally, Theseus' position can't equal Minotaur's because he would be dead.

Notice, however, that the problem fundamentally didn't change -- we still have a state which we can use to generate neighbouring states and thus again use BFS.

\marginpar{\texttt{BFSMinotaur}}
Luckily, the way we wrote the function BFS was very general -- it doesn't care about Theseus or the Minotaur; it just takes an initial state and a stop condition, whatever they might be, and repeatedly adds and explores neighbouring states via the `next_states` function, meaning that we can reuse it to solve our Minotaur problem!

For starters, let's add the Minotaur to the maze.
We'll have to find it, so let's add some code to do that.
Although the BFS function doesn't change, the way we call it does, since the state is now a `(theseus, minotaur)` tuple and the stop condition only checks if Theseus escaped, not the Minotaur.

We'll also rename the `next_states` function, because now it only returns the next possible positions of Theseus. To properly implement `next_states`, we'll frist need a function that moves the Minotaur towards Theseus.
To do this, we'll write a small function that moves the Minotaur in just one dimension, returning +1, 0 or -1.
To see what the function does, here are a few examples of what it returns for specific input values.

The main function for Minotaur movement then uses this function to attempt to move closer to Theseus horizontally and, if not successful, vertically, repeating twice.

With these two functions, we can finally write `next_states`: given some state, Theseus attempts to move in all directions and Minotaur follows suit.
If he catches Theseus, the state is invalid, else it's fine.

Running the code now, we see that the path is quite a bit longer.
Before visualizing it, try to pause here and solve the problem yourself -- what should Theseus do?

It turns out that Theseus has to lead the Minotaur into a corner to gain additional distance and only then escape, but escape he does.

This is very exciting -- we implemented a general algorithm to solve problems that have states where the goal is to get from one to another in the least amount of steps possible, like the shortest path problem and Theseus and the Minotaur problem.

---
Advent of Code 2022 (day 19)
---

\marginpar{\texttt{AOC}}
Now you might say that this algorithm is only useful for problems that involve a 2D board, but this is not the case. To convince you otherwise, here is a 3D board... nono, just kidding; here is a really fun problem taken from the Advent of Code 2022, day 19.

\marginpar{\texttt{Robots}}
There are 4 types of robots, each producing one of the following resources: ore, clay, obsidian and geode.
Each robot produces one resource per minute (so if you have 4 ore robots, they produce 4 ore a minute).
Besides this, you have a factory that can build a new robot in one minute:

- the ore robot costs 4 ore
- the clay robot costs 2 ore
- the obsidian robot costs 3 ore and 14 clay and
- the geode robot costs 2 ore and 7 obsidian

The factory takes a whole minute building the robot, meaning that during a minute, the factory first subtracts the resources required to build the robot, the robots then produce their respective resources and finally the robot is finished.

We start with an ore robot and no resources.
By building the robots in a specific order, we want to maximize the number of geodes produced after the first 24 minutes.

For these costs of the robots, here is the optimal solution. As you can see, the maximum number of geodes is 9.

Pause here and think of what the states are and how to get from one to another.

The states are the current number of resources and robots, but also the time, since we have to know when to stop exploring.
Getting from one state to another always means increasing the time by one, adding the acquired resources and attempting to build all possible robots.

This solution works but wouldn't terminate in a reasonable amount of time because of the branching factor, which is the average number of neighbouring states.

\marginpar{\texttt{RobotGraph}}
When going from the starting state (which is an ore robot and no resources), the problem doesn't branch too much initially, but the more resources are acquired, the more options there are, so getting to depth 24 of this tree will take a very long time, since it has around 21 million states.

So is the problem entirely hopeless? Well, no, there are a few things we can do, namely pruning and prioritization.

Let's first look at pruning.

---
Pruning
---

Pruning is the technique of removing valid states from the search that you know aren't going to lead to the right solution.

For example, let's think about a branch where only ore robots are built.
It certainly is a valid branch but we know that it won't produce the correct result, because building more ore robots than what's the highest requirement for ore is pointless.
We can therefore remove this branch and others like it to speed up the algorithm.

As another example, when we finally find states that obtain some geodes, we can start ignoring other states that couldn't obtain more even if they build a geode robot every minute, achieving further speedup.

While these strategies do help, as the graphs show, we can do even better and for that, let's go back to the shortest path problem.

---
Prioritization (A*)
---

\marginpar{\texttt{AStar}}
Remember that to solve it, we used BFS, which uses a queue to process states in the order they were discovered.
However, it might be a good idea to first explore (i.e. "prioritize") states that look more promising than others.
In this maze, for example, states that are closer to the escape (in terms of their $(x, y)$ coordinates) should probably be explored before those that are further, because there is a higher chance that they will lead to the escape.

This is what the A* algorithm does -- it uses a priority queue to prioritize states based on a heuristic function, which is an estimate of how far the state is from the end (in our case, the $(x, y)$ distance).
I won't go into detail here but if you're interested in an in-depth look at A*, here is a fantastic video from my friends at Polylog that you should definitely watch.

Anyway, here is what happens when we use A* for our shortest path problem -- pretty awesome, right?

\marginpar{\texttt{RobotGraph}}
And here is what happens when we use it on our robots problem (in combination with pruning) -- only 400 000 states, amazing.
The heuristic here is preferring states that have more rare resources (so first geode, then obsidian, then clay and finally ore).

---
Non-uniform edge costs (Dijkstra)
---

\marginpar{\texttt{BeegMaze}}
There is one last thing I want to cover before the video ends -- what if distances between the states weren't equal?
In the problems we've seen, it took exactly step to get from one state to another, but this isn't always the case.
Say you wanted to find the shortest path in a maze like this where you're allowed to break the wall, but it takes you 10 steps while regular moves take just 1.

Intuitively, we'd still like to use BFS, but now there is a problem -- the order in which the states are added to the queue no longer corresponds to the distance from the start because getting through the wall takes much longer.
To fix it, we'll replace the regular queue with a priority queue (similar to A*) to always visit the state that is closest to the start.

\marginpar{\texttt{Dijkstra}}
Here is the implementation, side by side with the BFS implementation -- as you can see, the algorithms are very similar with only a few differences.

Dijkstra uses a heap instead of the deque, which is a data structure that can quickly return its smallest element.
It uses it to always explore the element that is closest from the start.

The `next_states` function has to be aware that different neighbouring states can have different distances and so it has to return both the neighbour and the distance to it.
The distance from the start to the neighbour is the distance from start to the current state, plus the distance from the current state to the neighbour.

A given state can be discovered by multiple states with different distances before it is finally explored, so we have to add it to the heap every time we find a way to get to it quicker.
To do this, we track the distances to each state using a dictionary.

There is a more efficient implementation that doesn't require adding it to the heap multiple times but is beyond the scope of this video.

\marginpar{\texttt{BeegMaze}}
Solving our crowded maze problem, here is the shortest path, breaking 4 walls in total and taking exactly 69 steps. Nice.

\marginpar{\texttt{BeegMazeAStarTho}}
And, as you might be thinking, since the core principle of BFS and Dijkstra are the same, we can again use A* to prioritize states that are closer to the escape, solving the problem in fewer steps.

---
Outro
---

\marginpar{\texttt{Outro}}
This is the end of the video.
I hope it gave you the necessary tools for solving state space problems of all shapes and sizes.
If you have an interesting one that you'd like to share or you feel like I missed something, let me know in the comments.

\marginpar{\texttt{LastScreen}}
Thanks for watching!
