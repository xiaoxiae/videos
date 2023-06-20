---
title: The Art of Linear Programming
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \usepackage{todonotes}
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=70mm, top=15mm, bottom=15mm, marginparwidth=60mm}
- \newcommand{\fix}[1]{\todo[color=green!40]{#1}}
- \newcommand{\note}[1]{\todo[color=blue!40]{#1}}
---

\hrule
\vspace{1.5em}


---
INTRODUCTION
---

Would you like to win a Nobel price in economics?
Or be able to formulate and solve NP-hard problems in an efficient way?
Or perhaps transcend the mortal plane and achieve eternal life?

Well in this video, I'll cover the first two (the third being left as an excercise for the reader), since they both utilize the powerful technique of Linear Programming.

To see what it's all about, let's start with a simple problem.

\newpage


---
BASICS
---

With the planting season steadily approaching, your farmer friend presents you with the following task.
You have 3 tons of potato seeds and 4 tons of carrot seeds.
To grow the crops efficiently, you also have 5 tons of fertilizer, which has to be used when planting in a 1:1 ratio (i.e. 1 kilogram of potato or carrot seeds requires 1 kilogram of fertilizer).
The profit is 1.2\$/kg for potato seeds and 1.7\$/kg for carrot seeds.
Your goal is to maximize your profit this season -- how much potatoes and carrots should you plant?

To solve this problem, let's first formalize it.
We'll start by creating variables $x_p$ and $x_c$ for the amount of potatoes and carrots planted (in Kgs).
Both are non-negative real numbers, since planting a negative amount of seeds is difficult, and are bounded by the amount we have.
Additionally, their sum is bounded by the amount of fertilizer we have, since it has to be used in a 1:1 ratio for both potatoes and carrots.
The profit can then be described as $1.2 x_p + 1.7 x_c$ and we'll call it the objective function, since it's the function we're trying to maximize.

\newpage


---
GEOMETRIC SOLUTION
---

Now that the problem is formalized, it might be helpful to visualize it.
Since we have two variables, it's probably a good idea to use a plane with one axis for each.

To display the inequalities, we can notice that they are all linear, which means that they are just a weighted sum of the variables and each one defines a line with valid values on one side (a half-plane, to be exact).
To satisfy all of the inequalities, we're interested in the intersection of these half-planes, which is the following region.

This is pretty useful, since we now know that any solution to our problem will be contained here, but our main task is to maximize the objective function.
Pause here and see if you can figure out what it means geometrically in terms of this visualization.

Since the objective function is also linear, it defines a direction in which its value increases.
To solve the problem, all we then have to do is move in this direction and record the last intersection, which is the optimum (in our case, $1000$ Kgs of potato seeds and $4000$ Kgs of carrot seeds, bringing the total profit to $8000$ dollars.

And, surprisingly, that's all there is to linear programming -- we want to find the value of real variables that are subject to linear inequalities and that maximize a linear function.

Now this is a pretty simple example, but a linear program can be much more complex.
\todo{animation of lifting up to 3D space and showing the region (override the surface class)}
It can contain any number of inequalities, which complicate the shape of our region, and also any number of variables, which bring us from 2D for 2 variables to 3D for 3 and beyond... so while the general concept stays the same, our simple geometric solution won't do for larger programs.

\newpage


---
ALGORITHMIC SOLUTION (SIMPLEX METHOD)
---

Instead, let's look at how to solve a linear program algorithmically using the Simplex method.

Similar to the geometric solution, we will again be moving in the direction of the objective function, but we'll do so in a smarter way.
For this, we'll use the fact that at the optimum will be achieved in at least one vertex.
It can sometimes be more, like a whole line, but some vertex will still achieve it, as we see by doing a full rotation.

This means that we can move from vertex to vertex (which is called pivotting), always picking one that brings us closer to our goal, until we can't any longer, at which point we know we found the optimum.

But before I tell you how it works, let me tell you a short story.

\note{the background will be blurred and there will be the silhouettes doing stuff}

It's 1939 and a student of mathematics arrives late to a lecture.
He sees two problems on the board and, assuming they are homework, writes them down.
They prove to be more challenging than usual, but he perseveres and hands them back a week later, with an apology that they took him so long.
A few weeks go by and the student is surprised by a knock on the door by the professor himself, who reveals to him that they were two famous unsolved problems in the field of statistics.

\note{long pause}

You might have heard this story, or a version of it, since it's an urban legend in the mathematical world, but what you might not know is that the student was Goerge B. Dantzig, the inventor of the algorithm I just described.
I stumbled upon this story about Dantzig and many more when doing research for this video and it was too good to exclude, so if there's something you should to take away, it's that George B. Dantzig was a really cool guy.

Getting back to the topic at hand, we'll first rename the variables to $x_1$ and $x_2$, which is the standard way of naming variables in a linear program.

To understand how pivotting works numerically, let's consider what happens when we're in a vertex.
Taking $(0, 0)$ as an example, we see that two of the inequalities are tight, which means that the left side is equal to the right side (in this case because both $x_1$ and $x_2$ are 0).

Now say we want to pivot from this vertex to an adjacent one.
To perform the pivot, we first have to loosen one inequality (which determines the direction we move in) and tighten another (which determines how far we go).

This is the crucial idea behind the simplex algorithm -- loosen one and tighten another, until we reach the optimum.

In order to calculate which variables to loosen and which to tighten, we'll slightly modify our program to make the math easier.
We'll introduce new variables for each inequality called slack variables, which act as the difference between the left and the right side, turning the inequalities into equalities.
This means that a tight inequality before is the same as a variable being set to zero now -- as you see, since $s_1$ and $s_2$ are zero, the first and third equalities become tight.

Feel free to pause here for a second and make sure that this transformation makes sense to you.

Let's now get to the actual computation.
We again start in $(0, 0)$, which means that the initial tight variables will be $x_1$ and $x_2$.
The tight variables are usually called non-basic and the loose are called basic, but we'll stick with tight and loose for now (since that's what they geometrically mean).

Before we start the first pivot, we'll do two things: first, we'll hide the positive inequalities -- they still apply, mind you, but we don't need them for the actual computation, so there's no point in keeping them on the screen.
Second, we'll further rewrite the equalities such that the left side only contains loose variables with a coefficient of $1$ -- this makes calculating the current solution trivial, since we can just set the tight variables to $0$ and look at the constants.

Okay, now we're finally ready for the pivot.

\note{again, we'll blur and have a cropped animation of the previous pivot, with some borders}
First, we need to loosen a variable to determine which direction to go.
There is a number of methods for selecting which variable to loosen, but we'll stick with the most commonly used one called called Dantzig's pivot rule, after the inventor himself.
The rule is very simple -- we select the variable with the largest positive coefficient in the objective function (i.e. the one representing the steepest direction towards the optimum).

In our case, this is $x_2$, which we loosen and start heading in its direction.

\note{yet again, we'll blur and have a cropped animation of the end of the pivot}
Now that we've selected the direction to move in, we have to determine how far, which we'll do by tightening.
To see what choices we have, we'll look at equalities where $x_2$ appears, which are $s_2$ and $s_3$, since these are the loose variables constraining it.
We want to make either $s_2$ or $s_3$ tight but, as we see, only one of them keeps us in the area of valid solutions... so how can we calculate which one it is?

Well let's simulate what happens when we move further in the selected direction.
We see that $x_2$ is increasing and its value eventually reaches $4000$, which makes it equal to the constant value for the second equality, making $s_2$ tight.
Now if we were to go further, $s_2$ would have to go negative for the equality to still work, which is not allowed since all variables have to be non-negative!

So, in other words, to calculate which variable to tighten, we're interested in the ratio between $x_2$ and the constants -- the closer to $0$ it is, the sooner we reach it.
And, as we've seen, it is indeed $s_2$, which we tighten.

\todo{do this -- pan down, add the inequality and show that it's on the other side}
Note that if it is greater than zero (for example if we had another equality like this one), we wouldn't want it since we could increase $x_2$ however we wanted but we still wouldn't reach the constant value.

Now that we've loosened $x_2$ and tightened $s_2$, we still have to fix the equalities and the objective function -- remember that loose variables belong only on the left side, which now isn't the case, as you can see by the highlighted $s_2$s and $x_2$s.
Swapping them solves the problem for the second equality, which we can now use as substitutes for the remaining $x_2$s.

After simplifying, we have successfully completed the pivot.
As a sanity check, we see that setting the tight variables to zero again determines the vertex we're in, with the objective function's value increasing to $6800$.

At this point, I highly urge you to pause the video and do the next pivot yourself, since it's a great way of checking how well you understand the algorithm.
To help you out a bit, here are the steps you need to take:

- first, loosen a variable using Dantzig's pivot rule
- second, tighten a variable given the largest non-positive ratio and finally
- fix the equalities by swapping and substituting

\note{pause here}
Okay -- for the next pivot, we repeat exactly what we did for the first one:

- we determine the variable to loosen by the largest positive coefficient in the objective function, which is $x_1$,
- we look at where $x_1$ appears in the equalities and compare the ratios -- the largest non-positive one corresponds to $s_3$, which we tighten and finally
- we fix the equalities and the objective function such that the loose variables are only on the left side...

and we're done!
We can see this because all of the coefficients of the objective function are now negative so we can't improve any further.
The optimum is $8000$, again achieved in $(1000, 4000)$ (we don't care about the slack variable) which is the same as the one from our geometric solution, which is a good indicator that the algorithm works as intended.

\newpage


---
DUALITY
---

\note{blur and fade to the stupid joke}
So at this point, we have solved the problem both geometrically and algorithmically, but it would be pretty hard to convince someone else that we really did if we were to just show them the result.
It would be nice if we could prove that the solution we found is truly optimal.

One thing that comes to mind is combining the inequalities in a way that creates an upper bound on the objective function, because that would show that we literally can not get a better result.
As an example, if we multiply the first inequality by 1.2 and the second by 1.7 and we sum them up, we get that the objective function is less than or equal to 10 400, which tells us that the objective function can never be greater than that.
Or, let's say 0.2 times the first plus 0.7 times the second plus the third gives a better estimate of 8400.

This looks promising so let's formalize and turn these numbers into variables.
They have to be non-negative (otherwise the inequality flips) and must be set in such a way that the left side is at least the objective function (since we want to constrain it).
Finally, we want to minimize the right side, which is the following expression and... we just created a linear program.

This is called the dual linear program and is, in my opinion, perhaps the most beautiful thing about linear programming.
The dual bounds our original linear program (which we'll call the primal from now on) and vice versa -- solutions to the primal will always be less than or equal to the solutions of the dual and this is referred to as the weak duality theorem.

Now this is not quite what we had in mind -- we actually wanted an equality, because only then would we be able to confirm that the solution we found is truly the optimum.
This is referred to as the strong duality theorem and, incredibly, if the primal has an optimum, it holds true, meaning that we can always find the proof that we were looking for.

Besides proving optimality, duality has a number of other interesting uses that are sadly beyond the scope of this video, but will likely be in the next one.

\newpage


---
INTEGER LINEAR PROGRAMMING
---

It's now safe to say that we've thoroughly covered the farmer's problem, but it turns out that we were actually pretty lucky.
When formulating the problem, we decided that the variables can be real numbers, since planting a fraction of a Kg makes sense.
However, imagine that the things we wanted to plant were trees -- in that case, we would like to restrict the solutions to integers only (since planting a portion of a tree is difficult).

This is referred to as integer linear programming (or ILP for short) and it naturally poses two questions: is the problem easier or harder than linear programming and can we still solve it efficiently?

Well, to illustrate that it gets a whole lot harder, we'll formulate the knapsack problem (an infamous NP-hard problem), as an integer linear program.

The task is this: we're given $n$ items, each having a weight and a price.
Given a backpack with a carry weight (say 17 kg), our task is to maximize the price of the items we take without exceeding the carry weight.

For this problem, using binary variables will be very useful.
We can achieve this by creating a variable and adding inequalities such that its value is between 0 and 1.
Since it's an integer linear program, the only values the variable can have will therefore be 0 and 1.

There will be one binary variable for each item, having value $1$ if we take it and $0$ if we don't.
There will only be one additional inequality, which is that the weight of the items we carry doesn't exceed the backpack's carry weight.
This can be done by multiplying the binary variables with their weights -- if the item is not taken, its variable will be $0$ and its weight won't be counted, otherwise it will be.
Similarly, the function to maximize is the price of the items we carry, again done by multiplying the binary variables with their prices.

Alternatively, if we put the variables into a vector, the linear program can be stated like this, which is quite a bit more concise.

And since there's been enough theory, let's write some Python code that solves this problem using the `pulp` package, which is an excellent tool for formulating and solving linear programs of all shapes and sizes.

Taking the data from the example we've seen, we'll formulate the variables, the single inequality and the objective function and finally solve the problem.

Printing the output, the optimal value of the items in this case is $84$, if we take item $2$, $4$, $5$, and $6$.

So while the problem is still NP-hard, there is a significant amount of optimizations that the solver can do, which makes it run very fast on real-world data (and likely much faster compared to whatever program you and I can write).

As another `pulp` example, this is an implementation of the farmer's problem that we saw earlier in the video.

\note{show my website (actually) -- a recording as I'm scrolling by}
There are many more examples of problems that can be solved with both regular and integer linear programming and if you're interested, I left a link to my website showcasing the interesting ones in the description.


\newpage


---
OUTRO
---

So as an introduction to linear programming, I think we've covered most of the important topics, that being the simplex method, duality and integer linear programming.
However, we've covered them rather superficially and there is a great deal of nuance to each of them.

For the simplex method, what if $(0, 0)$ isn't a vertex -- how do we start?
Also, the way we described it, it might run in exponential time or even get stuck in an infinite loop -- how do we fix this?

For duality, does every linear program have a dual and if so, how do we create it?
And once we do, how can we use it in developing fast algorithms?

And, last but not least, are there classes of ILP problems that can be solved in polynomial time?
And for those that aren't in such class, can we at least approximate them in polynomial time?

I like to think that most topics, linear programming included, can be thought of as an iceberg (in this case a convex one) -- the surface contains simple concepts that everyone can see, but if you dive down, you can discover a whole new world, a part of which we'll explore in the next video.

So if you found this interesting, stay tuned and thank you for watching!
