---
FIRST SECTION NAME
---

TODO: standardize - bathroom model, tile model, ... terminology

# Motivation
Since the time of the ancient Greeks, the best ideas were born in the bathroom -- just ask Archimedes. This would come in handy for programming, but unfortunately, laptops and moisture don't get along very well.

The solution: bathroom tiles!

# Intro
We'll picture the bathroom wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have $4$ sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have the colors of the wall and some finite set of tile types. The question is: can we create a tiling that satisfies our requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

For this example, it is pretty clear that we can. However, if we were to change the top side like so, it would no longer be possible.

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

The first two just connect adjacent opening and closing parentheses, since we don't need more than one layer for that.

We also have tiles for non-adjacent opening and losing parentheses, and tiles to connect them. 

Finally, we have a single blank tile to fill in the gaps.

The reason for different colors for opening and closing tiles is that if the color was the same, they would be interchangeable, meaning that the program would accept incorrect parentheses.

As for time complexity, there can be at most $n/2$ pairs of parentheses and we need at most one row for each, so this solution runs in time $O(n)$.

(TODO: animation)
Interestingly, $O(n)$ is not the fastest way this problem can be solved. There is an arguably more beautiful solution that only requires $O(\log n)$ rows, which I'm not going to show in this video but would instead love you, the viewer, to think about on your own.

(TODO: animation)
I will leave a link to solution to this exercise and many more in the description, if you're interested in solving some on your own. Also, if you come up with a different solution or a new problem entirely, write it in the comments so other people can see and take inspiration from.


# Computational power (TODO)
If you've studied automata theory least a little, you might have noticed some similarities between our programs (TODO: animace těch dvou programů) and automatons. This is, as we'll see, no coincidence.

Our bathroom tile model turns out to be equivalent to a linearly bounded Turing machine. By this we mean a Turing machine with a finite tape as long as the input.

As a quick reminder, a Turing tape is a machine that has an infinite tape and a set of states. At any given time, it has a position on the tape and the state it is in. It then repeatedly does the following:
- reads the current position on the tape
- updates it depending on what the state and the current value is and
- moves to the left or right, again depending on what the state and the current value was

Turing machines are important, because they are as powerful as any modern-day programming language is, meaning that any problem that you solve in your language of choice, be it Python, Java, or C#, can also be solved using a Turing machine.

Since our Turing machine is linearly bounded, it is not as powerful as a regular Turing machine. However, we can still do a lot of neat things, like check, whether the input number is a prime, or a power of two, or whether it can be split into $n$ equal pieces, each having size $n$.

Proving this requires a bit of work and is beyond the scope of this video, but essentially boils down to reducing a linearly bounded non-deterministic Turning machine to a bathroom tile program and vice versa. If you're interested, a proof can be found in the description bellow.


# To infinity and beyond!
Let's extend bathroom wall to infinity in all directions.

The question about tiling still remains, same as in the previous model. But there are two, deeper questions:

1. If a tileset is able to fill the plane, can it also do so periodically?
2. Is there an algorithm that can determine, whether a tileset fills the plane?

These questions, first asked by Hao Wang in the 1970, 

TODO

Wang observed that the first implies the second.

TODO

These are called the Wang tiles, first proposed by a Chinese mathematician Hao Wang in the 1969.
