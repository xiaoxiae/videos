---
FIRST SECTION NAME
---

# Intro
So you're taking a shower. In front of you, you see bathroom tiles that neatly fit together, creating a captivating pattern. The pattern is so interesting in fact that you think to yourself: can these be used for programming?

Well, as it turns out, they can!

# Definitions
We'll picture the wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have 4 sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have some finite set of tile types and the colors of the wall. The question is: can we create a tiling that satisfies the requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

For this example, it is pretty clear that we can. However, if we were to change the top side like so, it would no longer be possible, since the top row couldn't be filled with any tiles.

What we just described is the programming model that we'll be using. We'll reserve the top side for input, which will be some finite sequence of colors, and leave others arbitrary. Our program will be a finite set of tile types that we can use. The program will **accept** the input if there exists a valid tiling of some non-zero height, and **reject** it if there's none.

But enough theory, let's look at an example.


# Examples
The following program will accept the input, if and only has even length. It should be pretty obvious why -- we have to start with the first tile and then alternate. Since we have to end with the second tile, the input length must be even.

A slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones in the input is divisible by three. The main idea here is to remember, how many ones we've seen so far.


# TODO: indicate start and end 0
We start with 0, and must also end with 0, since the counter loops around at 3 (TODO: animace pod tilema). When the input contains a zero, we carry over the number, since it doesn't change the number of ones. When it does contain a one, we increment by one.


# Complexity
For regular programming models, a reasonable way to measure time complexity of a given problem is to count how the number of operations depend on the size of the input. For our programming model, this doesn't really make sense, since the filling either exists or it doesn't -- we're not doing any operations.

What we'll do here instead is measure how the number of layers depend on the size of the input. However, since we haven't really seen problems requiring more than one layer, let's look at one.

Create a program that accepts the input, if and only if it contains parentheses that are balanced (meaning that for each opening one, there is a closing one to the right).

Here, it should intuitively make sense that we need more than one layers to remember, how many parentheses we've seen already.


TODO:
- reference to automatons
- computational power
