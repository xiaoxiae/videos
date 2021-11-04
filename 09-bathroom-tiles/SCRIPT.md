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

But enough theory, let's see some examples of programs.

For example, this program will accept the input, if and only if it is of even length. It's pretty obvious why -- we have to start with TODO, and then we can either end with TODO, or repeat...

A slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones in the input is even. Notice that we replaced some of the colors with characters, and will sometimes do so, because it makes the program more readable.

Let's say we want to write a program (i. e. create a tile set) that accepts the input if and only if it contains all red or blue colors, but not both combined.

TODO:
- reference to automatons
- complexity by height
- computational power
- variations (triangles, hexagons)
- 

