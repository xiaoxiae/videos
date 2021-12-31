---
MOTIVATION
---

**[m1]:** Since the time of the ancient Greeks, the best ideas were born in the bathroom -- just ask Archimedes. This would come in handy for programming, but unfortunately, laptops and moisture don't get along very well.

**[m2]:** But there is a surprising solution: bathroom tiles!

---
INTRODUCTION
---

**[i1]:** We'll picture the bathroom wall as a rectangle of width $w$ and height $h$ that we want to entirely fill with square tiles of size $1$. Each tile will have $4$ sides with some colors.

**[i2]:** For the tiling to make sense, we want the adjacent tiles' colors to match. We'll also make it so that each side of the wall has some color that again must match the tiles it's adjacent to.

**[i3]:** Now say we have the colors of the wall and a finite set of tile types. The question is: can we create a tiling that satisfies our requirements? Note that we can use as many tiles of each type as we want, but we cannot rotate them.

**[i4]:** For this example, it is pretty clear that we can. However, if we were to change the top side like so, it would no longer be possible, because there are no tiles with red on the top side.

**[i5]:** This is essentially the programming model that we'll be using. The input will be some finite sequence of colors on the top side of the wall (which could also be symbols to make some of the programs more readable). Our program will be a finite set of tile types and the remaining colors of the wall. Note that neither the tileset nor the wall colors can depend on the input. The program will **accept** the input if there exists a valid tiling of any non-zero height, and **reject** it if there's none.

---
EXAMPLE: EVEN SIZE OF INPUT
---

**[e11]:** Looking at this example, the program will accept the input, if and only if it has even length. It should be pretty obvious why -- we have to start with the first tile and end with the second tile. Now notice that the tiles switched roles and we can again place the first and the second tile like so. Since we're always forced to add tiles by twos for the middle colors to match, the input length must be even, else the tiling cannot exist.

---
EXAMPLE: NUMBER OF ONES DIVISIBLE BY 3
---

**[e21]:** Another, slightly more advanced example is this one, where the program accepts the input, if and only if the number of ones is divisible by three. The idea is to count how many ones we've seen when tiling from the left. When counting, we'll loop back to 0 when the count reaches 3, because we're only interested in the remainder after division.

**[e22]:** This means that we have to end with a 0, because a remainder 0 after division happens if and only if the number is wholly divisible.

**[e23]:** The tiles are divided into two groups: we carry over the number of ones we've seen when the input contains a zero, and increment when it contains a one.

**[e24]:** Let's see the tiling in action to better understand how it works.

**[e25]:** As you can see, the number of ones we're carrying in the tiles correspond to the actual number when counting from the left, which is exactly what we want. Additionally, there is always exactly one tile to place at any given point in the tiling, since it's uniquely determined by the previous tile and the input.

**[e26]:** Because there are 6 ones, which is indeed divisible by 3, the input is accepted.

---
TIME COMPLEXITY
---

**[t1]:** Let's talk a bit about time complexity.

**[t2]:** For traditional programming models, a reasonable way to define time complexity of a problem is the minimum number of instructions needed to compute the solution, based on the size of the input.

**[t3]:** For example, bubble sort will sort an input of size $n$ in $O(n^2)$ operations, and binary search will find an item in a sorted array in $O(log(n))$ operations.

**[t4]:** For our programming model, this definition doesn't make sense, since the tiling either exists or it doesn't. What we'll do here instead is measure the minimum number of rows needed to accept the input, again based on its size.

**[t5]:** When the input is not accepted, there will be no rows to count since the tiling doesn't exist. We'll therefore exclude rejected inputs from the calculation altogether, since there is no good way to measure them.

**[t6]:** But so far, we've only seen problems requiring exactly one row, so let's look at one that requires a bit more.

---
EXAMPLE: BALANCED PARENTHESES
---

**[e31]:** The task is to create a program that accepts the input, if and only if it contains parentheses that are balanced (meaning that for each opening one, there is a corresponding closing one to the right of it).

**[e32]:** One solution might look like this. Although daunting at first, the best way to understand it is to look at a successful tiling.

**[e33]:** As you can see, the tiles are defined in such a way that they connect each corresponding pair of parentheses using the wall itself. For example, these two parentheses are connected via this path.

**[e34]:** We can again separate the tiles into a few groups. The first two tiles just connect adjacent opening and closing parentheses, since we don't need more than one layer for that.

**[e35]:** Then we have tiles for non-adjacent opening and losing parentheses, and tiles to connect them.

**[e36]:** Finally, we have a blank tile to fill in the gaps.

**[e37]:** The reason for different colors for opening and closing parentheses is that if the colors were the same, they would be interchangeable and the input could be unbalanced.

**[e38]:** As for time complexity, there can be at most $n/2$ pairs of parentheses and we need at most one row for each, so this solution runs in time $O(n)$.

**[e39]:** Interestingly, this is not the fastest way this problem can be solved. There is an arguably more beautiful optimal solution that only requires time $O(\log n)$, which I'm not going to show in this video but would instead love you, the viewer, to think about on your own.

**[e310]:** I will leave a link to solution to this problem and many more in the description, if you're interested in solving some of them.

---
COMPUTATIONAL POWER
---

**[c1]:** So... how strong is our model? Which problems can it solve and which can it not? Is it as strong as Python, or stronger, or is it not even close?

**[c2]:** Well, our model turns out to be equivalent to a linearly bounded Turing machine. By this we mean a non-deterministic Turing machine with a finite tape that is as long as the input.

**[c3]:** This means that it is not as strong as Python (and basically every other modern programming language), since Python is Turing complete and thus equivalent to a regular Turing machine.

**[c4]:** Despite this limitation, it can still solve a surprisingly large set of problems, like checking whether a number is prime, whether a maze contains a path from one point to another, or even whether a boolean expression has an assignment of variables that make it true.

**[c5]:** One neat consequence of this limitation is that there exists an algorithm to tell you, whether a given tileset will tile for a given input. This is not true for a regular Turing machine, where no such algorithm exists.

---
TO INFINITY
---

**[inf1]:** Let's extend the bathroom wall to infinity in all directions.

**[inf2]:** The question about tiling still remains, but two new, seemingly unrelated ones arise:

1. If a tileset can fill the plane, can it also fill it periodically?
2. Is there an algorithm to check if a tiling exists (just as for the previous, finite model)?

**[inf3]:** These questions, first asked by Hao Wang in the 1970, both have the sad answer "no." It turns out that the first question implies the second, since if it were true then could just use bruteforce to look for the periodic pattern which would be the algorithm. However, if the second were true then this would contradict the halting problem, which can be proven by reducing regular Turing machines to infinite tiling programs. Thus, since the second is false, the first one must be false too.

**[inf4]:** Here is an example of one such tileset that does fill the plane aperiodically, but not periodically.

---
OUTRO
---

**[o1]:** There are many other rabbit holes that I had to stop myself from going into to keep the video at a reasonable length. Nevertheless, I hope you enjoyed a look into this fascinating programming model and who knows, maybe we'll all be programming in T++ some time in the future.
