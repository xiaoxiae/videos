---
INTRODUCTION
---

The boolean satisfiability problem, or SAT for short, is arguably one of the most important computer science problems.
It is NP-complete, meaning that it lies in NP and any problem from NP can be reduced to it (in polynomial time).
Unlike other problems that are NP-complete, however, there exist very optimized solvers that can compute the solution for real-world inputs very efficiently (although still exponentially). TODO: green for sat and red for others

When solving SAT, we usually need our algorithm to provide the optimal solution.
Sometimes, however, it is sufficient to exchange an improved running time for a solution that is close to, but not quite the optimum.

What is fascinating about SAT in particular and will be the main topic of this video is that the optimal SAT approximation algorithm is a clever combination of two other, completely unrelated approximation algorithms.

But let's slow down for just a bit and get our definitions out of the way.

---
DEFINITIONS
---

For the sake of this video, SAT is a problem of satisfying a formula in CNF, which is just a cojunction of clauses, each of which being a disjunction of positive and negative literals.
An easy way to think of it is that you have groups of literals and at least one from each group has to be satisfied.
The goal is to output an assignment of literals that satisfies all clauses.
For our example, this is rather simple -- one such assignment is setting a, d and e to 1 and the rest to anything.

As you might notice, this formulation can't really be approximated, since the assignment of variables either exist or it doesn't.
We'll therefore generalize SAT to MAX-SAT, will no longer require that every group is satisfied, but instead that as many as possible are -- this, finally, is something that we can approximate.


---
RAND-SAT
---

When thinking about approximation algorithms for MAX-SAT, a good way to start is with the simplest thing you can think of -- assign values randomly and hope for the best.

I wrote a Python program to simulate RAND-SAT on our example expression.
We have a generate_random_values function that randomly generates n boolean values.
We then have a count_satisfied_clauses function that counts the number of satisfied clauses of the expression.
Running the experiment 10000 times, we randomly assign values and count the number of satisfied clauses.

If we run the program, we can see that the average number of satisfied clauses is about TODO percent, which is not bad.

Formally, when looking at a single clause of $k$ literals, the algorithm doesn't satisfy it if and only if all of the variables are set to false.
Since the probabilities of each assignment are independent, the probability of the clause not being satisfied is $\frac{1}{2^k}$.
Therefore the probability that it its satisfied is $1 - (\frac{1}{2})^2$.

Since each clause contains at least one literal, the program will (in expectation) satisfy at least $\frac{1}{2}$ of the clauses.


---
LP-SAT
---

The second algorithm that we'll examine is LP-SAT.
Before that, however, we need a slight interlude into linear programming.

A linear programming problem contains real variables, linear inequalities that restrict them and a linear expression (called the objective function) that we want to maximize.

Using Python to solve this particular example, the optimal solution yields he following objective function and the following assignment of variables.

Linear programming is a useful tool for formulating and solving a huge variety of problems, because it can be solved very efficiently.
To formulate MAX-SAT in terms of linear programming (again taking our example expression), we'll create two types of binary variables: one for each literal in the formula, and one for each clause.

The inequalities will reflect the clauses: we'll restrict the clause variables by the formula variables, depending on how the clause looks.
The expression to maximize will be the sum of clause literals, which corresponds to the number of satisfied clauses.

If we, for example, take a look at the first inequality, the only way for x to be 1 is if at least one of its literals is satisfied (so either a is 1, b is 0 or c is 0).

Running the program yields the objective function of 3 (so all clauses can be satisfied) and the following assignment of variables.
This seems like we've succeeded in creating a fast algorithm for MAX-SAT that always yields the optimal solution, but that's just because we cheated -- arbitrarily setting the variables to be integers (binary, to be more specific) makes linear programming NP complete, so this doesn't quite work.

To work around this issue, we'll relax the variables to allow real numbers (from 0 to 1, which we can do by adding inequalities) and then use the results as "hints" for our program, which will assign the literal value 1 with the probability of the variable from the .

TODO: talk about the program


---
LP-SAT PROOF
---

For this part of the video, I present the proof for how well LP-sat performs based on the size of the clauses.
It is quite technical, so you aren't interested and would like to see the conclusion of the video, feel free to skip ahead.

For the proof, we'll use the following two facts (there will be links in the description for those interested).

We built the following linear program and would like to see, how well it performs.

Consider the solution of the relaxed linear program and a clause with k literals.
The probability of it not being satisfied is the following product.
Using fact A, 
