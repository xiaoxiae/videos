---
FIRST SECTION NAME
---

# Motivation
Since the time of the ancient Greeks, the best ideas were born in the bathroom -- just ask Archimedes. This would come in handy for programming, but unfortunately, laptops and moisture don't get along very well.

However, there is a rather obvious solution: bathroom tiles!

# Intro
We'll picture the bathroom wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have $4$ sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have the colors of the wall and some finite set of tile types. The question is: can we create a tiling that satisfies our requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

For this example, it is pretty clear that we can. However, if we were to change the top side like so, it would no longer be possible, because there are no tiles with two red side.

What we just described is the programming model that we'll be using (TODO: text writing constants). We'll reserve the top side for input, which will be some finite sequence of colors. Our program will be a finite set of tile types that we can use in the tiling, plus the colors of the remaining sides of the wall. The program will **accept** the input if there exists a valid tiling of some non-zero height, and **reject** it if there's none.

Looking at this example, the program will accept the input, if and only if it has even length. It should be pretty obvious why -- we have to start with the first tile and end with the second tile. Now notice that the tiles switched roles and we can again place the first and the second like so. Since we're always forced to add tiles by twos for the middle colors to match, the input length must be even, else the tilling cannot exist.

Another, slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones is divisible by three. The idea is to count, how many ones we've seen when tiling from the left. When counting, we'll loop back to 0 when the count reaches 3, because we're only intereseted in the remainder after division.

The tiles are divided into two groups: when the input contains a zero, we carry over the number of threes we've seen. When it contains a one, we increment.

With this out of the way, let's tile!

As you can see, the number of ones we're carrying in the tiles correspond to the actual number when counting from left, which is exactly what we want.

The input is accepted, because there are 6 ones, which is indeed divisible by 3.


# Time Complexity
For traditional programming models, a reasonable way to measure time complexity of a problem is to count the number of operations in relation to the size of the input.

For example, bubble sort will sort an input of size $n$ in $O(n^2)$ operations, and binary search will find an item in a sorted array in $O(log(n))$ operations.

For our programming model, this obviously wouldn't make sense, since the tiling either exists or it doesn't. What we'll do here instead is measure the only thing we can -- the minimum number of rows needed to accept the input.

But so far, we haven't seen any problems requiring more than one row, so let's look at one.

The task is to create a program that accepts the input, if and only if it contains parentheses that are balanced (meaning that for each opening one, there is a corresponding closing one to the right of it).

One solution might look like this. Although daunting at first, the best way to understand it is to look at a successful tiling.

As you can see, the tiles are defined in such a way that they connect each corresponding pair of parentheses using the wall itself. For example, these two are connected via this path.

We can again separate the tiles into a few groups.

The first two just connect adjacent opening and closing parentheses, since we don't need more than one layer for that.

We also have tiles for non-adjacent opening and losing parentheses, and tiles to connect them. 

Finally, we have a blank tile to fill in the gaps.

The reason for different colors for opening and closing parentheses is that if the color was the same, they would be interchangeable and the program would accept incorrect parentheses.

As for time complexity, there can be at most $n/2$ pairs of parentheses and we need at most one row for each, so this solution runs in time $O(n)$.

(TODO: animation)
Interestingly, $O(n)$ is not the fastest way this problem can be solved. There is an arguably more beautiful solution that only requires $O(\log n)$ rows, which I'm not going to show in this video but would instead love you, the viewer, to think about on your own.

(TODO: animation)
I will leave a link to solution to this problem and many more in the description, if you're interested in solving some on your own. Also, if you come up with a different solution or a new problem entirely, write it in the comments so other people can see and take inspiration from.


# Computational power (TODO)
If you've studied automata theory, you might have noticed some similarities between our programs (TODO: animace těch dvou programů) and automatons. This is, as we'll see, no coincidence.

Our model turns out to be equivalent to a linearly bounded Turing machine. By this we mean a Turing machine with a finite tape that is as long as the input.

Proving this requires a bit of work and is beyond the scope of this video, but essentially boils down to reducing every linearly bounded Turning machine to a tile program and vice versa. If you're interested, a proof can be found in the description bellow.


# To infinity and beyond! (TODO)
Let's go further and extend the bathroom wall to infinity in all directions.

The question about tiling still remains, but two new questions arise:

1. If a tileset is able to fill the plane, can it also fill it periodically?
2. Is there an algorithm that can determine, whether a tileset can fill the plane?

These questions, first asked by Hao Wang in the 1970, both have the sad answer "no," but it is pretty interesting why. It turns out that the first question implies the second, since if it were true then could just use bruteforce to look for the periodic pattern which would be the algorithm. However, if the second were true then this would contradict the halting problem (another famous result in the field of automata theory). Thus, since the second is false, the first one is false too.

Here is, for example, a tileset that can fill the plane aperiodically but not periodically, found in 2015 by Emmanuel Jeandel and Michael Rao.


# Outro
There are many other rabbit holes that I had to stop myself from going into to keep the video at a reasonable duration. Regardless, I hope you enjoyed a look into this weird programming model and who knows, maybe we'll all be programming in Tile++ some time in the future.
