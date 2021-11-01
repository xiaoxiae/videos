---
FIRST SECTION NAME
---

# Intro
So you're taking a shower. In front of you, you see bathroom tiles that neatly fit together, creating a captivating pattern. The pattern is so interesting in fact that you think to yourself: can these be used for programming?

Well, as it turns out, they can!


# Definitions
We'll picture the wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have 4 sides with some colors.

For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

Now say we have some finite set of tile types and the colors of the wall. We can use as many tiles of each type as we want to create a tiling, but we can't rotate them. The question is: can we create a tiling that satisfies the requirements?

TODO: animace toho setu a vedle toho stěny

For some cases, it is pretty obvious that we either can or can't. Yet for others, it is not as clear.

TODO: animace toho, pro které je to jasné a pro které ne, a pro které je to nejasné (například sudý počet jedné barvy)

What we just described is the programming model that we'll be using. We'll reserve the top side for input, which will be some finite sequence of colors. Our program will then be a finite set of tile types that we can use. Our program will **accept** the input if there exists a valid tiling of some non-zero height, and **reject** it if there's none.

But enough theory, let's see an example.

Let's say we want to write a program (i. e. create a tile set) that accepts the input only if it contains all red or blue colors, but not both combined.

TODO:
- reference to automatons
- complexity by height
- computational power
- variations (triangles, hexagons)
- 

