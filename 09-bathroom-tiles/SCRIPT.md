---
FIRST SECTION NAME
---

# Intro
Since the time of ancient Greeks, the best ideas were born in the bathroom -- just ask Archimedes. However, since laptops and moisture don't get along very well, we'll have to come up with another way of writing code.

The solution: bathroom tiles.

# Definitions
We'll picture the wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have 4 sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have some finite set of tile types and the colors of the wall. The question is: can we create a tiling that satisfies the requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

For this example, it is pretty clear that we can. However, if we were to change the top side like so, it would no longer be possible, since the top row couldn't be filled with any tiles.

What we just described is the programming model that we'll be using. We'll reserve the top side for input, which will be some finite sequence of colors, and leave others arbitrary. Our program will be a finite set of tile types that we can use in the tiling. The program will **accept** the input if there exists a valid tiling of some non-zero height, and **reject** it if there's none.

But enough definitions, let's look at an example.


# Examples
TODO: task (write it explicitly)
The following program will accept the input, if and only if it has even length. It should be pretty obvious why -- we have to start with the first tile (TODO: highlight left side) and then alternate. Since we can only end with the second tile (TODO: highlight side), the input length must be even (TODO: zkrátím a ukážu,že to nejde).

Another, slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones in the input is divisible by three.

The main idea here is to keep track of how many ones we've seen so far when filling from the left. We start with 0, and must end with a number divisible by 3. TODO: ffs this is a weird paragraph (TODO: under tiles animation 0 1 2 0 1 2 ...). When the input contains a zero, we carry over the number. When it contains a one, we increment (TODO: změním jedničku).


# Time complexity (TODO)
For regular programming models, a reasonable way to measure time complexity is to count how the number of operations depend on the size of the input.

For our programming model, this obviously doesn't make sense, since the tiling either exists or it doesn't -- we're not really doing any operations.

What we'll do here instead is measure the minimum number of layers needed to accept the input. However, since we haven't seen any problems requiring more than one layer, let's look at one.

The task is to create a program that accepts the input, if and only if it contains parentheses that are balanced (meaning that for each opening one, there is a closing one to the right of it).

Here, it should intuitively make sense that we need more than one layer to remember, how many parentheses we've seen already. A straightforward solution might look like this:


# Computational power (TODO)

TODO:
- reference to automatons
