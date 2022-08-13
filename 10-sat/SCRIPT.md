---
title: The Surprising BEST-SAT Approximation Algorithm
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
Imagine you're the manager of a company that owns a number of factories, each of which can produce one of at most two products.
You'd like your company to produce all possible unique products to maximize profit, but calculating this by hand would be tedious at best and impossible at worst -- how can you do this efficiently?

\marginpar{\texttt{SAT}}
One way of doing so is to formulate it in terms of the boolean satisfiability problem (or SAT for short).
SAT is the problem of satisfying a boolean formula in CNF, which is a conjunction of clauses, each of which being a disjunction of positive and negative literals.
An easy way to think of it is that you have groups of literals and at least one from each group has to be satisfied.
For this example, one such assignment is setting $a$, $d$ and $e$ to 1 (so their negations are 0) and the rest to anything.

\marginpar{back to \texttt{Factories}}
Going back to the factories problem, each product will be a clause and each factory producing it a literal.
If a factory produces a single product, it will be added to the appropriate clause.
If it produces two, one will be positive and one negative, since a factory can only produce one product at a time.
As you can see, a product is produced if and only if at least one of its factories are producing it.
In this simple example, the problem doesn't have a solution, because a single factory produces two unique products.

\marginpar{\texttt{SATSad}}
Unfortunately, SAT is NP-hard, which means that it runs in exponential time and solving it for a large number of factories and products could take a few millennia.
One thing we could do in cases like these is to use an approximation algorithm, which exchanges an improved running time for a solution that is close to, but not quite the optimum.
Interestingly, one of SAT's best approximation algorithms is a random combination of two of its other, worse approximation algorithms, which is truly remarkable.

\newpage

---
MAX-SAT
---

\marginpar{\texttt{SATAgain}}
As previously mentioned, SAT is the problem of satisfying a boolean formula in CNF.
This formulation can't really be approximated, since the satisfying assignment either exists or it doesn't, as we've seen in the factories example.
We'll therefore generalize SAT to MAX-SAT, which will no longer require that every group is satisfied, but instead that as many as possible are.
In this case, three out of four expressions can be satisfied, which is nice!


---
RAND-SAT
---

\marginpar{\texttt{TransparentRANDSAT}}
<!-- write RAND-SAT, show description and then fade it out and move RAND-SAT to the corner -->
Our first algorithm to solve MAX-SAT will be entirely random, assigning True/False values with the probability of 0.5.

\marginpar{Program \texttt{RAND-SAT}}
I wrote a Python program to simulate it on the expression from before.
We have a `generate_random_values` function that randomly generates $n$ boolean values.
We then have a `count_satisfied_clauses` function that counts the number of satisfied clauses of the expression.
Running $10\ 000$ times in total, we randomly assign boolean values to the literals and count the number of satisfied clauses, printing the satisfied percentage at the end.

If we run the program, we see that the average number of satisfied clauses is about 56 %, which is pretty good, considering how simple the algorithm is and that the best it can do in this case is 3/4.

\marginpar{\texttt{RANDSATFormal}}
Formally, the algorithm doesn't satisfy a clause of $k$ literals if and only if all of them are set to false, the probability of which is is $(\frac{1}{2})^k$.
Therefore the probability that it its satisfied is $1 - (\frac{1}{2})^k$.

Since each clause contains at least one literal, it is satisfied with the probability of at least $1/2$, meaning the algorithm will (in expectation) satisfy at least $1/2$ of the clauses.



\newpage

---
LP-SAT
---

\marginpar{\texttt{TransparentLPSAT}}
Our second algorithm, LP-SAT, will be a little more complicated.
To fully understand it, we need a slight interlude about linear programming.

A linear program conains real variables and linear inequalities that restrict them.
The goal is to maximize a linear expression (called the objective function).

\marginpar{Fade z animace do programu \texttt{LP Example}}
Using Python and its package PULP to solve this particular example, the optimal solution yields the following objective function and assignment of variables.

\marginpar{TODO animation}
 <!-- animations -->
Since linear programming is polynomial, we'll use it to solve MAX-SAT.
\marginpar{Fade to program \texttt{MAX-SAT using LP}}
Taking our familiar expression once again, we'll convert it to a linear program in the following way.
We'll create a binary variable for each literal and clause in the formula.
The expression to maximize will be the sum of clause literals, which corresponds to the number of satisfied clauses.

The inequalities will reflect the clauses: we'll restrict the clause variables by the formula variables, depending on the clause literals.
If we, for example, take a look at the third inequality, the only way for $y$ to be 1 is if at least one of the literal variables are satisfied (so either $b$ is 1 or $c$ is 0).
If none of them are, then the right side will be 0, forcing $y$ to be 0 as well.

Running the program yields the objective function of 3, meaning that only three of the four clauses can be satisfied at the same time (which we already know).

\marginpar{Overlay cross (\texttt{TransparentCrossText}), because we cheated}
At first glance, it seems like we've created a fast exact algorithm for MAX-SAT, but that's only because we cheated -- arbitrarily setting the variables to be integers (binary, to be more specific) makes linear programming NP-hard (and thus exponential), so this doesn't work.

\marginpar{\texttt{RelaxedMAXSAT}}
Let's fix it.
Writing our MAX-SAT program formally, we have binary variables for literals and clauses, inequalities for each clause and an objective function as the sum of clause variables.

Since the problem is the variables being integer, let's just relax them to allow real numbers again (from 0 to 1).
This will make the linear program fast again, but it will be solving some weird MAX-SAT variant with real values instead of boolean values.

<!-- literally modify it in the video -->
Modifying the linear program to allow for real variables and running it, we see that $a$ be $0.5$ and so should $b$.
Since the optimum of the relaxed linear program will be always better than the one of the non-relaxed one (since we allow more values), we will use this result for generating our approximation.

\marginpar{Program \texttt{LP-SAT} }
Adding the rest of LP-SAT, we first solve the relaxed MAX-SAT, yielding some assignment of variables.
We then have an `assign_variables_based_on_lp` function, which returns boolean values based on the linear program variables, as mentioned previously.
The rest of the program is the same as RAND-SAT.

Running the program, we see that the average number of satisfied clauses is 2/3, which is worse than RAND-SAT, but that's just because I explicitly selected an example where only 2 out of 3 clauses can be satisfied for you to see the algorithm in action.


\newpage

---
LP-SAT PROOF
---

<!-- TODO: intro for proof -->
\marginpar{\texttt{Proof}}
For this part of the video, I present a proof for how well LP-SAT performs based on the size of the clauses.
It is a little technical, so if you aren't sure about some of its steps, don't worry too much.

For the proof, we'll use the following two facts.
Fact A is the inequality of arithmetic and geometric means, which states that for any sequence of non-negative real numbers, the geometric mean is less than or equal to the arithmetic mean.
Fact B is Jensen's inequality, which states that if a function is concave on the interval $[0,1]$, $f(0)=a$ and $f(1)=a+b$, then the following inequality holds.
It actually has this simple geometric interpretation, feel free to pause here and think it through.

If you recall, this is the linear program we used as hints for LP-SAT

Now consider the optimal solution of the relaxed linear program and a clause containing $k_j$ literals.
For it to not be satisfied, LP-SAT has to decide that all its positive literals be false and its negative literals be true, the probability of which is the following product.
Using fact A, the products turn into sums, which can further be turned into the following expression.
Now you can notice that the expression in the parentheses is just the $j$-th inequality, so we can simplify in the following way.

Now let's calculate the probability that it is satisfied.
If we take it as a function of $z_j^*$, we can observe that $f(0) = 0$ and that it is concave (by checking that the second derivative is positive, which is left as an exercise for the listener).
This means that we can use Jensen's inequality and get this bound.

As $k_j$ goes to infinity, the highlighted expression gets larger and larger, converging to the well-known constant of $1/e$, which is approximately $0.63$.
This is exactly what we wanted, because the expected number of satisfied clauses is equal to the sum of their probabilities, which using our inequality yields the following.
Now since the sum of $z_j^*$ is exactly equal to the optimum of the relaxed program, which is at least the real optimum of MAX-SAT, we get the following bound on LP-SAT.
<!-- TODO: the -->

\newpage

---
BEST-SAT
---

\marginpar{\texttt{BestSat}}
Looking at both RAND-SAT and LP-SAT, the probability that a clause with $k$ literals is satisfied is at least the following for each respective algorithms.
As a reminder, $z_j^*$ is a number between $0$ and $1$ which tells us how well can the clause be satisfied in the optimal case.
Since it's less than $1$, we'll add it to RAND-SAT too for easier calculations.

Let's look at how the algorithms perform on clauses of varying size.
As you can see, RAND-SAT seems to be performing better the larger the clause is.
This is no surprise, since the more variables there are, the higher chance is for RAND-SAT to pick one correctly.
On the other hand, LP-SAT performs worse the larger the clause is, ultimately converging to the constant we arrived at during the proof.

Since RAND-SAT performs better for longer clauses and LP-SAT performs better for shorter ones, we'll create BEST-SAT by randomly deciding to use either of the two for each clause with the probability of 1/2.
<!-- animate adding another row and combining the two on top with the one below -->

If we calculate the probability for $k = 1$, we see that this is at least $3/4 z_j^*$. Doing this for $2$, $3$ and so on, we can again see


\newpage

---
CLOSING REMARKS
---

It is hard to really appreciate how good BEST-SAT really is.
One thing that puts it into perspective is the following whitepaper

It's (NP) hard to do it much better (7/8)

LP is actually not strongly polynomial
