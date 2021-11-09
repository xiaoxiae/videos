---
FIRST SECTION NAME
---

# Intro
Since the time of ancient Greeks, the best ideas were born in the bathroom -- just ask Archimedes. However, since laptops and moisture don't get along very well, we'll have to come up with another way of writing code.

The solution: bathroom tiles!

# Definitions
We'll picture the bathroom wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have 4 sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have some finite set of tile types and the colors of the wall. The question is: can we create a tiling that satisfies the requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

For this example, it is pretty clear that we can. However, if we were to change the top side like so, it would no longer be possible, since the top row couldn't be filled with any tiles.

What we just described is the programming model that we'll be using. We'll reserve the top side for input, which will be some finite sequence of colors, and leave others arbitrary. Our program will be a finite set of tile types that we can use in the tiling. The program will **accept** the input if there exists a valid tiling of some non-zero height, and **reject** it if there's none.

But enough definitions, let's look at an example.


# Examples
The following program will accept the input, if and only if it has even length. It should be pretty obvious why -- we have to start with the first tile and end with the second tile. Then we again have to add the tiles like so. Since we're always adding tiles by two to end up with matching sides, the input length must be even.

Another, slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones in the input is divisible by three. The idea is to count how many ones we've seen, when filling from the left. When counting, we'll loop back to 0 when the count reaches 3.

The tiles are divided into two groups: when the input contains a zero, we carry over the number of threes. When it contains a one, we increment (and possibly loop back).

Starting from the left, let's try and find a tiling.

As you can see, it exists. This makes sense, since there are 6 ones in the input, which is indeed divisible by three.


# Time complexity (TODO)
For regular programming models, a reasonable way to measure time complexity is to count how the number of operations depend on the size of the input.

For our programming model, this obviously doesn't make sense, since the tiling either exists or it doesn't -- we're not really doing any operations.

What we'll do here instead is measure the minimum number of layers needed to accept the input. However, since we haven't seen any problems requiring more than one layer, let's look at one.

The task is to create a program that accepts the input, if and only if it contains parentheses that are balanced (meaning that for each opening one, there is a closing one to the right of it).

Here, it should intuitively make sense that we need more than one layer to remember, how many parentheses we've seen already. A straightforward solution might look like this:


# Computational power (TODO)

- Turing
- reference to automatons
