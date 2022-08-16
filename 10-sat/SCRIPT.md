---
title: The Remarkable BEST-SAT Algorithm
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

---
INTRODUCTION
---

\marginpar{\texttt{Factories}}
**i1:** Imagine you're the manager of a company that owns a number of factories, each of which can produce one of at most two products.
You'd like your company to produce all possible unique products to maximize profit, but determining how to do this by hand would be tedious at best and impossible at worst -- how can you do this efficiently?

\marginpar{\texttt{SAT}}
**i2:** One way of doing so would be to formulate it in terms of the boolean satisfiability problem (or SAT for short).
SAT is the problem of satisfying a boolean formula in CNF, which is a conjunction of clauses, each of which being a disjunction of positive and negative literals.
An easy way to think of it is that you have groups of literals and at least one from each group has to be satisfied.
For this example, one such assignment is setting $a$, $d$ and $e$ to 1 (so their negations are 0) and the rest to anything.

\marginpar{back to \texttt{Factories}}
**i3:** Going back to the factories problem, each product will be a clause and each factory producing it a literal.
If a factory produces a single product, it will be added to the appropriate clause.
If it produces two, one will be positive and one negative, since a factory can only produce one product at a time.
As you can see, a product is produced if and only if at least one of its factories are producing it.
In this simple example, the problem doesn't have a solution, because a single factory produces two unique products.

\marginpar{\texttt{SATSad}}
**i4:** SAT runs in exponential time and so solving it for a large number of factories and products could take a few millennia.
One thing we could do in cases like these is to use an approximation algorithm, which exchanges an improved running time for a solution that is close to, but not quite the optimum.
Interestingly, one of SAT's best approximation algorithms is a random combination of two of its other, worse approximation algorithms, which is, in my opinion, remarkable.

**i5:** So.. let's start approximating!

\marginpar{\texttt{SATAgain}}
**m1:** As previously mentioned, SAT is the problem of satisfying a boolean formula in CNF.
This formulation can't really be approximated, since the satisfying assignment either exists or it doesn't, as we've seen in the factories problem.
We'll therefore generalize SAT to MAX-SAT, which will no longer require that every group is satisfied, but instead that as many as possible are.
In this case, by setting the literals like so, three out of four clauses can be satisfied!


\newpage

---
RAND-SAT
---

\marginpar{\texttt{TransparentRANDSAT}}
**r1:** Our first algorithm to solve MAX-SAT will be entirely random, assigning true and false values with the probability of $1/2$.

\marginpar{Program \texttt{RAND-SAT}}
**r2:** I wrote a Python program to simulate it on the expression from before.
We have a `generate_random_values` function that randomly generates $n$ boolean values.
We then have a `count_satisfied_clauses` function that counts the number of satisfied clauses of the expression.
Running $10\ 000$ times in total, we randomly assign boolean values to the literals and count the number of satisfied clauses, printing the satisfied percentage at the end.

**r3:** If we run the program, we see that the average number of satisfied clauses for this expression is about 56 %, which is pretty good, considering how simple the algorithm is and that the best it can do in this case is 75 %.

\marginpar{\texttt{RANDSATFormal}}
**r4:** Looking at the algorithm more formally, RAND-SAT doesn't satisfy a clause of $k$ literals if and only if all of them are set to false, the probability of which is is $(\frac{1}{2})^k$.
Therefore the probability that it its satisfied is $1 - (\frac{1}{2})^k$.

**r5:** Since each clause contains at least one literal, it is satisfied with the probability of at least $1/2$, meaning the algorithm will (in expectation) satisfy at least $1/2$ of the clauses.



\newpage

---
LP-SAT
---

\marginpar{\texttt{TransparentLPSAT}}
**l1:** Our second algorithm, LP-SAT, will be a little more complicated.
To fully understand it, we need a slight interlude about linear programming.

**l2:** A linear program conains real variables and linear inequalities that restrict them.
The goal is to maximize a linear expression (called the objective function).

\marginpar{Fade z animace do programu \texttt{LP Example}}
**l3:** Using Python and its package PULP to solve this particular example, the optimal solution yields the following objective function and assignment of variables.

**l4:** Since linear programming is polynomial, we'll use it to solve MAX-SAT.
\marginpar{Fade to program \texttt{MAX-SAT using LP}}
Taking our familiar expression, we'll convert it to a linear program in the following way.
We'll create a binary variable for each literal and clause in the formula.
The expression to maximize will be the sum of clause variables, which corresponds to the number of satisfied clauses.

**l5:** The inequalities will reflect the clauses: we'll restrict the clause variables by the formula variables, depending on the clause literals.
If we, for example, take a look at the third inequality, the only way for $y$ to be 1 is if at least one of the literal variables are satisfied (so either $b$ is 1 or $c$ is 0).
If none of them are, then the right side will be 0, forcing $y$ to be 0 as well.

**l6:** Running the program yields the objective function of 3, meaning that only three of the four clauses can be satisfied (which we already know).

\marginpar{Overlay cross (\texttt{TransparentCrossText}), because we cheated}
**l7:** At first glance, it seems like we've created a fast exact algorithm for MAX-SAT, but that's only because we cheated -- arbitrarily setting the variables to be integers (binary, to be more specific) makes linear programming exponential, so this won't work.

\marginpar{\texttt{TransparentRelaxedMAXSAT}}
**l8:** Well, let's fix it.
Writing the linear program formally, we have binary variables for literals and clauses, inequalities for each clause and an objective function as the sum of clause variables.

**l9:** Since the problem is the variables being integer, let's just relax them to allow real numbers (from 0 to 1).
This will make the linear program fast again, but it won't be solving MAX-SAT anymore, since the variables can now be any number from 0 to 1.

**l10:** We can demonstrate this on the following expression, constructing this relaxed linear program.
The optimum is $2.5$, with $a$ and $b$ both set to $0.5$.

**l11:** Now we obviously can't satisfy two and a half clauses, but what we can do is use $a$ and $b$ to help us assign true and false values to the corresponding literals.
<!-- TODO: animation! -->
Since the variable $a$ is $0.5$, we'll assign the literal $a$ true with this probability and false otherwise and the same for $b$.

\marginpar{Program \texttt{LP-SAT} (fade from the previous program).}
**l12:** This is the core idea behind LP-SAT -- we have an `assign_variables_based_on_lp` function which returns boolean values for each literal based on this exact idea, with the rest of the program being the same as RAND-SAT.

**l13:** Running the program, we see that the average number of satisfied clauses for this expression is about 66 %.


\newpage

\marginpar{\texttt{Proof}}
**p1:** For this part of the video, I present a proof for how well LP-SAT performs on the size of the clauses (same as we've done for RAND-SAT).
It is a little technical, so if you aren't sure about some of its steps, don't worry too much -- the conclusion is what matters most.

**p2:** For the proof, we'll use the following two facts.
Fact A is the inequality of arithmetic and geometric means, which states that for any sequence of non-negative real numbers, the geometric mean is less than or equal to the arithmetic mean.
Fact B is Jensen's inequality, which states that if a function is concave on the interval $[0,1]$, $f(0)=a$ and $f(1)=a+b$, then the following inequality holds.
It actually has this simple geometric interpretation, feel free to pause here and think it through.

**p3:** If you recall, this is the relaxed linear program we used as hints for LP-SAT
Now consider the optimal solution of the relaxed linear program and a clause containing $k_j$ literals.
For it to not be satisfied, LP-SAT has to decide that all its positive literals be false and its negative literals be true, the probability of which is the following product.
Using fact A, the products turn into sums, which can further be turned into the following expression.
Now you can notice that the expression in the parentheses is just the $j$-th inequality, so we can simplify in the following way.

**p4:** Now let's calculate the probability that it is satisfied.
If we take it as a function of $z_j^*$, we can observe that $f(0) = 0$ and that it is concave (by checking that the second derivative is positive).
This means that we can use Jensen's inequality and get this bound.

**p5:** As $k_j$ goes to infinity, the highlighted expression gets larger and larger, converging to the well-known constant of $1/e$, which is approximately $0.63$.
This is exactly what we wanted, because the expected number of satisfied clauses is equal to the sum of the probabilities that they are satisfied, which, using our inequality yields the following.
Taking the constant out, we get the sum of clause variables, which is the objective function and so the optimum, meaning that the algorithm satisfies (in expectation) at least $(1 - 1/e)$ clauses of the optimum, so around 63 %.
This is better, but still not quite there.

\newpage

---
BEST-SAT
---

\marginpar{\texttt{BestSat}}
**b1:** Looking at both RAND-SAT and LP-SAT, the probability that a clause with $k_j$ literals is satisfied is at least the following for each respective algorithm.
As a reminder, $z_j^*$ is a number between $0$ and $1$ which tells us how well can the clause be satisfied in the optimal case (the sum of $z_j^*$ being the optimum).
Since it's less than $1$, we'll add it to RAND-SAT too for easier calculations.

**b2:** Let's look at how the algorithms perform on clauses of varying size.
As you can see, RAND-SAT seems to be performing better the larger the clause is.
This is no surprise, since the more variables there are, the higher chance is for RAND-SAT to pick one correctly.
On the other hand, LP-SAT performs worse the larger the clause is, ultimately converging to the constant we arrived at during the proof.

**b3:** This prompts an intersting idea -- since RAND-SAT performs better for longer clauses and LP-SAT performs better for shorter ones, let's just average them.
And thus BEST-SAT is born. It works by randomly deciding to use either RAND-SAT or LP-SAT for each clause independently.

**b4:** Substituting the bound for larger $k$s of LP-SAT and calculating the probabilities for BEST-SAT by averaging RAND-SAT and LP-SAT, we see that it is at least $3/4$ the optimum for each $k$. This means that BEST-SAT satisfies at least $3/4$ of the clauses as the optimum, which is just wild, considering how bad the to individual algorithms are.


\newpage

---
OUTRO
---

\marginpar{camera}
**out:** I really hope you enjoyed this video, as it took a while to make and hope it inspired you to further explore the wonderful world of approximation algorithms.
