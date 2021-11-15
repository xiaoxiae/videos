---
FIRST SECTION NAME
---

# Motivation
Since the time of the ancient Greeks, the best ideas were born in the bathroom -- just ask Archimedes. This would be pretty handy for programming; however, laptops and moisture don't get along very well, so we'll have to program in another way.

The solution: bathroom tiles!

# Intro
We'll picture the bathroom wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have $4$ sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have the colors of the wall and some finite set of tile types. The question is: can we create a tiling that satisfies our requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

For this example, it is pretty clear that we can (TODO: animation of finishing the tiling). However, if we were to change the top side, it would no longer be possible, since the top row couldn't be filled with tiles of any type.

What we just described is the programming model that we'll be using (TODO: text writing constants). We'll reserve the top side for input, which will be some finite sequence of colors. Our program will be a finite set of tile types that we can use in the tiling, plus the colors of the remaining sides of the wall. The program will **accept** the input if there exists a valid tiling of some non-zero height, and **reject** it if there's none.

Looking at this example, the program will accept the input, if and only if it has even length. It should be pretty obvious why -- we have to start with the first tile and end with the second tile. Now notice that the tiles switched roles and we can again place the first and the second like so. Since we're always forced to add tiles by twos for the middle colors to match, the input length must be even.

Another, slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones is divisible by three. The idea is to count (using the left and right side of each tile) how many ones we've seen when tiling from the left. When counting, we'll loop back to 0 when the count reaches 3, because we're only intereseted in the remainder after division.

The tiles are divided into two groups (TODO: more apparent highlight (flash isn't apparent enough) -- maybe wiggle?): when the input contains a zero, we carry over the number of threes we've seen. When it contains a one, we increment.

With this out of the way, let's tile!

As you can see, the number of ones we're carrying in the tiles correspond to the actual number when counting from left (TODO: also isn't apparent enough, maybe wiggle?) (TODO: exponential speed increase (smooth it?), linear looks bad), which is exactly what we want.

The input is accepted, because there are 6 ones, which is indeed divisible by 3.


# Time Complexity
For traditional programming models, a reasonable way to measure time complexity of a problem is to count the number of operations in relation to the size of the input.

For example, bubble sort will sort an input of size $n$ in $O(n^2)$ operations, and binary search will find an item in a sorted array in $O(log(n))$ operations.

For our programming model, this obviously doesn't make sense, since the tiling either exists or it doesn't -- we're not really doing any operations. What we'll do here instead is measure the minimum number of rows needed to accept the input.

But... we haven't seen any problems requiring more than one row yet, so let's look at one.

The task is to create a program that accepts the input, if and only if it contains parentheses that are balanced (meaning that for each opening one, there is a corresponding closing one to the right of it).

One solution might look like this. Although daunting at first, the best way to understand it is to look at a successful tiling.

As you can see, the tiles are defined in such a way that they connect each corresponding pair of parentheses using tiles of the wall. For example, these two are connected via this path.

We can again separate the tiles into a few groups.

The first two just connect adjacent opening and closing parentheses, since we don't need more than one layer for that. We also have tiles for a opening and losing parentheses -- .

TODO

The reason for different colors for opening and closing tiles is that if the color was the same, they would be interchangeable and the program would accept incorrect parentheses.

(TODO: animation)
As for time complexity, there can be at most $n/2$ pairs of parentheses and we need at most one row for each, so this solution runs in $O(n)$ (technically, it runs in height $O(n)$, but let's stick to time).

(TODO: animation)
Interestingly, $O(n)$ is not the fastest way this problem can be solved. There is an arguably more beautiful solution that only requires $O(\log n)$ rows, which I'm not going to show in this video but would instead love you, the viewer, to think about on your own.

(TODO: animation)
I will leave a link to solution to this exercise and many more in the description, if you're interested in solving some on your own. Also, if you come up with a different solution or a new problem entirely, write it in the comments so other people can see and take inspiration from.


# Relations to Automatons (TODO)
If you've studied automata theory least a little, you might have noticed some similarities between some of our programs (TODO: animace těch dvou programů) and automatons. This is, as we'll see, no coincidence.

TODO: že bere vstup
For our purposes, a deterministic automaton is an oriented graph with a starting vertex and an ending vertex (TODO: denote by arrow and double circle -- literally copy the cool website form ag). We'll start in the starting vertex, read the input one character at a time, and move using the corresponding edge from the vertex we're in (TODO: state moving animation). We'll say the automaton **accepts** the input, if it ends in an ending vertex after reading the entire input, and **reject** it if it either doesn't, or gets stuck somewhere (meaning if there isn't a corresponding edge from the current vertex).

Notice that we're doing basically the same thing in both of the one-row programs. The colors in the middle of the tiles correspond to the states of the automaton and the tile types the edges. The left wall color is the starting vertex and the right one is the end.

TODO: edges (actually make the vertex colors the same as the colors on the program)

TODO: stack automatons reference for multiple rows

TODO: transition: we'll do something even better

# Computational power (TODO)
Believe it or not, our bathroom tile model is actually Turing complete, meaning that anything that can be programmed using your language of choice, be it Python, Java or C, can be made into a tiling program. (TODO: animace toho, jak tam jezdí loga různých jazyků).

Proving this requires a bit of work and is beyond the scope of this video, but essentially boils down to reducing a Turning machine to a bathroom tile program, and vice versa.
