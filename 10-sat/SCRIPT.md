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
SAT is the problem of satisfying a boolean formula in CNF, which is a conjunction of clauses, each of which being a disjunction of positive and negative literals. <!-- silnější kroužky -->
An easy way to think of it is that you have groups of literals and at least one from each group has to be satisfied.
For this example, one such assignment is setting $a$, $d$ and $e$ to 1 (so their negations are 0) and the rest to anything.

\marginpar{back to \texttt{Factories}}
Going back to the factories problem, each product will be a clause and each factory producing it a literal.
If a factory produces a single product, it will be added to the appropriate clause.
If it produces two, one will be positive and one negative, since a factory can only produce one product at a time.
As you can see, a product is produced if and only if at least one of its factories are producing it.

\marginpar{\texttt{SATSad}}
Unfortunately, SAT is NP-hard and thus runs in exponential time, meaning that solving it for a large number of factories and products could take a few millennia.

One thing we could do in cases like these is to use an approximation algorithm, which exchanges an improved running time for a solution that is close to, but not quite the optimum. <!-- redo this -- include this in a graph with an exponential thingy -->
What is fascinating about SAT in particular and will be the main topic of this video is that one of its best approximation algorithms is a random combination of two of its other, worse approximation algorithms, which seems crazy at first but will make more sense as we go on.

\newpage

---
RAND-SAT
---

\marginpar{\texttt{SATAgain}}
As previously mentioned, SAT is the problem of satisfying a boolean formula in CNF.
This formulation can't really be approximated, since the satisfying assignment either exists or it doesn't.
We'll therefore generalize SAT to MAX-SAT, which will no longer require that every group is satisfied, but instead that as many as possible are.
In terms of our factory problem, this means that we'll be maximizing the number of diverse products the factories produce.

\marginpar{Program \texttt{RAND-SAT}}
<!-- intro -rand sat and what it does + transfer to the bottom right -->
When thinking about approximation algorithms for any problem, a good way to start is with the simplest thing you can think of -- in our case, we can assign values randomly and hope for the best.

I wrote a Python program to simulate this algorithm (called RAND-SAT) on our example expression.
We have a `generate_random_values` function that randomly generates $n$ boolean values.
We then have a `count_satisfied_clauses` function that counts the number of satisfied clauses of the expression.
Running $10\ 000$ times in total, we randomly assign boolean values to the literals and count the number of satisfied clauses.

If we run the program, we see that the average number of satisfied clauses is about TODO percent, which is pretty good, considering how simple the algorithm is.

\marginpar{\texttt{RANDSATFormal}}
Formally, the algorithm doesn't satisfy a clause of $k$ literals if and only if all of the literals are set to false.
since the probabilities of each assignment are independent, the probability of the clause not being satisfied is $(\frac{1}{2})^k$.
Therefore the probability that it its satisfied is $1 - (\frac{1}{2})^k$.

Since each clause contains at least one literal, it is satisfied with the probability of at least $1/2$, meaning the algorithm will (in expectation) satisfy at least $1/2$ of the clauses.


\newpage

---
LP-SAT
---

\marginpar{\texttt{LPSAT}}
The second algorithm that we'll examine is LP-SAT.
To understand it, however, we need a slight interlude about linear programming.

A linear program conains real variables and linear inequalities that restrict them.
The goal is to maximize a linear expression (called the objective function).

\marginpar{Fade z animace do programu \texttt{LP Example}}
<!-- transform from Manim to code (variables, inequalities, objective function) --> 
Using Python and its package PULP to solve this particular example, the optimal solution yields the following objective function and assignment of variables.


\marginpar{Program \texttt{MAX-SAT using LP}}
Linear programming is, for our intents and purposes, polynomial, so it would be great if we could use it to formulate MAX-SAT.
To do this, we'll create two types of binary variables: one for each literal in the formula, and one for each clause.
The expression to maximize will be the sum of clause literals, which corresponds to the number of satisfied clauses.

The inequalities will reflect the clauses: we'll restrict the clause variables by the formula variables, depending on the clause literals.
If we, for example, take a look at the first inequality, the only way for the clause variable $x$ to be 1 is if at least one of the literal variables are satisfied (so either $a$ is 1, $b$ is 0 or $c$ is 0).
If none of them are, then the right side will be 0, forcing $x$ to be 0 as well.

Running the program yields the objective function of 3 (so all clauses can be satisfied).

\marginpar{Overlay cross (\texttt{CrossText}), because we cheated}
This seems like we've succeeded in creating a fast algorithm for MAX-SAT that always yields the optimal solution, but that's just because we cheated -- arbitrarily setting the variables to be integers (binary, to be more specific) makes linear programming NP-hard, so this doesn't work.

\marginpar{Program \texttt{Relaxed MAX-SAT} }
Let's think about what happens when we relax the variables to allow real numbers (from 0 to 1).
This makes the linear program fast again, but we'll no longer be solving MAX-SAT, but instead a variant with real values instead of boolean values. <!-- Show a line with max sat optimum, relaxed max sat optimum and our approximation -->
Since the optimum of this variant will be at least as good as the optimum of MAX-SAT, we can use it to help us randomly assign variables -- for example, if it says that $a$ should be $0.5$ and so should $b$, we'll say that $a$ will be $1$ with the probability of $0.5$ (else 0) and analogically for $b$.

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
It is a little technical, so if you aren't interested and would like to see the conclusion of the video, feel free to skip ahead.

For the proof, we'll use the following two facts.
Fact A is the inequality of arithmetic and geometric means, which states that for any sequence of non-negative real numbers, the geometric mean is less than or equal to the arithmetic mean.
Fact B is Jensen's inequality, which states that if a function is concave on the interval $[0,1]$, $f(0)=a$ and $f(1)=a+b$, then the following inequality holds.
It actually has this simple geometric interpretation, feel free to pause here and think it through.

If you recall, the linear program we used as hints for LP-SAT had variables for literals and clauses, inequalities for each clause and an objective function as the sum of clause variables.

Now consider the optimal solution of the relaxed linear program and a clause containing $k_j$ literals.
For it to not be satisfied, LP-SAT has to decide that all its positive literals be false and its negative literals be true, the probability of which is the following product.
Using fact A, the products turn into sums, which can further be turned into the following expression.
Now you can notice that the expression in the parentheses is just the $j$-th inequality, so we can simplify in the following way.

Now let's calculate the probability that it is satisfied.
If we take it as a function of $z_j^*$, we can observe that $f(0) = 0$ and that it is concave (by checking that the second derivative is positive, which is left as an exercise for the listener).
This means that we can use Jensen's inequality and get this bound.

As $k_j$ goes to infinity, the highlighted expression gets larger and larger, converging to the well-known constant of $1/e$, which is approximately $0.63$.
This is exactly what we wanted, because the expected number of satisfied clauses is equal to the sum of their probabilities, which using our inequality yields the following.
Now since the sum of $z_j^*$ is exactly equal to the optimum of the relaxed program, we get the following bound on LP-SAT.
<!-- TODO: the -->

\newpage

---
BEST-SAT
---

\marginpar{\texttt{BestSat}}
Looking at both RAND-SAT and LP-SAT, the probability that a clause with $k$ literals is satisfied is at least the following for each respective algorithms. <!-- TODO: side by side. -->
For easier computation, we'll add the $z_j^*$ term to RAND-SAT too, which we can do since it is smaller than $1$.

Since RAND-SAT performs better for longer clauses and LP-SAT performs better for shorter ones, we'll create BEST-SAT by randomly deciding to use either of the two with probability 1/2 for each clause separately <!-- TODO: animate adding parentheses and 1/2. -->
If we calculate the probability for $k = 1$, we see that this is at least $3/4 z_j^*$. Doing this for $2$, $3$ and so on, we can again see


\newpage

---
CLOSING REMARKS
---

It is hard to really appreciate how good BEST-SAT really is.
One thing that puts it into perspective is the following whitepaper

It's (NP) hard to do it much better (7/8)

LP is actually not strongly polynomial
