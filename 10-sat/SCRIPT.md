---
INTRODUCTION
---

The boolean satisfiability problem, or SAT for short, is arguably one of the most important computer science problems.
It is NP-complete, meaning that it lies in NP and any problem from NP can be reduced to it (in polynomial time).
Unlike other problems that are NP-complete, however, there exist optimized solvers that can compute the solution for real-world inputs very efficiently (although still exponentially).

When solving SAT, we usually need our algorithm to provide the optimal solution.
Sometimes, however, it is sufficient to exchange an improved running time for a solution that is close to, but not quite the optimum.

What is fascinating about SAT in particular and will be the main topic of this video is that the optimal SAT approximation algorithm is a clever combination of two other, completely unrelated approximation algorithms.

But let's slow down for just a bit and get our definitions out of the way.

---
DEFINITIONS
---

For the sake of this video, SAT will be a problem of satisfying a formula in CNF, which is just a conjunction of clauses, each of which being a disjunction of positive and negative literals.
An easy way to think of it is that you have groups of literals and at least one from each group has to be satisfied.
For our example, this is rather simple~--~one such assignment is setting a, d and e to 1 and the rest to anything.

As you might notice, this formulation can't really be approximated, since the assignment of variables either exist or it doesn't.
We'll therefore generalize SAT to MAX-SAT, will no longer require that every group is satisfied, but instead that as many as possible are~--~this, finally, is something that we can approximate.


---
RAND-SAT
---

\begin{center}\textit{Showing program 1 (RAND-SAT), displaying its name.}\end{center}

When thinking about approximation algorithms for any problem, a good way to start is with the simplest thing you can think of~--~assign values randomly and hope for the best.

I wrote a Python program to simulate this algorithm (called RAND-SAT) on our example expression.
We have a `generate_random_values` function that randomly generates n boolean values.
We then have a `count_satisfied_clauses` function that counts the number of satisfied clauses of the expression.
Running 10000 times in total, we randomly assign values and count the number of satisfied clauses.

If we run the program, we see that the average number of satisfied clauses is about TODO percent, which is pretty good, considering how simple the algorithm is.

\begin{center}\textit{Blending back to the Manim animation.}\end{center}

Formally, the algorithm doesn't satisfy a clause of $k$ literals if and only if all of the variables are set to false.
Since the probabilities of each assignment are independent, the probability of the clause not being satisfied is $\frac{1}{2^k}$.
Therefore the probability that it its satisfied is $1 - (\frac{1}{2})^2$.

Since each clause contains at least one literal and is therefore satisfied with probability of at least 1/2, the algorithm will (in expectation) satisfy at least $\frac{1}{2}$ of the clauses.


---
LP-SAT
---

The second algorithm that we'll examine is LP-SAT.
To understand it, however, we'll need a slight interlude about linear programming.

A linear programming problem contains real variables, linear inequalities that restrict them and a linear expression (called the objective function) that we want to maximize.

\begin{center}\textit{Showing program 2 (LP), displaying "Example".}\end{center}

Using Python and its package PULP to solve this particular example, the optimal solution yields he following objective function and the following assignment of variables.

\begin{center}\textit{Blending to animation of example problems that we can solve.}\end{center}

Linear programming is a very useful tool for formulating and solving a huge variety of problems, because it can be solved very efficiently. TODO: examples of problems~--~new scene with the problems

\begin{center}\textit{Showing program 3 (MAX-SAT using LP).}\end{center}

To formulate MAX-SAT in terms of linear programming (again taking our example expression), we'll create two types of binary variables: one for each literal in the formula, and one for each clause.
The expression to maximize will be the sum of clause literals, which corresponds to the number of satisfied clauses.

The inequalities will reflect the clauses: we'll restrict the clause variables by the formula variables, depending on how the clause looks.
If we, for example, take a look at the first inequality, the only way for $x$ to be 1 is if at least one of its literals are satisfied (so either $a$ is 1, $b$ is 0 or $c$ is 0).
If none of them are, then the following expression will be 0 and $x$ must be 0 as well and is therefore not satisfied.

Running the program yields the objective function of 3 (so all clauses can be satisfied) and the following assignment of variables.

\begin{center}\textit{Showing the cross and fading the program, because it's incorrect.}\end{center}

This seems like we've succeeded in creating a fast algorithm for MAX-SAT that always yields the optimal solution, but that's just because we cheated~--~arbitrarily setting the variables to be integers (binary, to be more specific) makes linear programming is NP-hard itself, so this sadly doesn't work.
We can prove this by converting some well-known NP-complete problems (such as the Knapsack problem) to an integer linear program -- it is quite a fun exercise and I suggest you give it a go.

\begin{center}\textit{Showing program 4 (Relaxed MAX-SAT using LP), displaying its name.}\end{center}

To fix this, we'll relax the variables to allow real numbers (from 0 to 1, using inequalities) and then use the results as "hints"~--~for example, if the linear program says that $a$ should be 0.5 and so should $b$, we'll assign 1 to a with the probability of 0.5 and the same for $b$.

\begin{center}\textit{Showing program 5 (LP-SAT), displaying its name.}\end{center}

Adding the rest of LP-SAT, we have an `assign_variables_based_on_lp` function, which returns boolean values based on the hints from the linear program.
The rest of the program is same as RAND-SAT.

Running it, we see that the average number of satisfied clauses is 2/3, which is worse than RAND-SAT, but that's just because I explicitly selected an example where only 2 out of 3 clauses can be satisfied.


---
LP-SAT PROOF
---

For this part of the video, I present a proof for how well LP-sat performs based on the size of the clauses.
It is a bit technical, so if you aren't interested and would like to see the conclusion of the video, feel free to skip ahead.

For the proof, we'll use the following two facts.
Fact A is the inequality of arithmetic and geometric means, which states that for any sequence of non-negative real numbers, the geometric mean is less than or equal to the arithmetic mean.
Fact B is Jensen's inequality, which states that if a function is concave on the interval $[0,1]$, $f(0)=a$ and $f(1)=a+b$, then the following inequality holds.
It actually has a simple geometric interpretation, which is quite nice.

If you recall, the linear program we used as hints for LP-SAT had variables for literals and clauses, inequalities for each clause and an objective function as the sum of clause variables.

Now consider the optimal solution of the relaxed linear program and a clause containing $k$ literals.
For it to not be satisfied, LP-SAT has to decide that all its positive literals be false and its negative literals be true, the probability of which is the following product.
Using fact A, the products turn into sums, which can further be turned into the following expression.
Now you can notice that the expression in the parentheses is just the $j$-th inequality, so we can simplify in the following way.

If the probability that it is not satisfied is at most something, that the probability that it is satisfied is at least 1 - the something.
Now if we take this as a function of $z_j^*$, we can observe that $f(0) = 0$ and that it is concave (by checking that the second derivative is positive, which is left as an exercise for the reader)
This means that we can use Jensen's inequality and get this bound.

As $k_j$ goes to infinity, this expression gets larger and larger, converging to the well-known constant of $1/e$, which is approximately 0.63.
Since the optimal $z_j^*$ is at most one, we get this final inequality.

