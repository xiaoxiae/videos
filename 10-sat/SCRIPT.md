---
INTRODUCTION
---

SAT, or the boolean satisfiability problem is arguably one of the most important computer science problems when talking about P vs. NP. This is because a lot of problems from NP can easily be converted to SAT and there exists optimized solvers that you can use to compute the solution.

Sometimes, however, we need our algorithms to run in polynomial time, in exchange for the solution being close to, but not quite the optimum. This is what we call approximation algorithms -- they run fast, but produce a solution that is not optimal.

What is fascinating about SAT in particular and will be the main topic of this video is that the optimal SAT approximation algorithm is a clever combination of two other, seemingly unrelated approximation algorithms, which intuitively shouldn't work well, but turns out to be the optimal way to do things.

But let's slow down just a bit and get our definitions out of the way.

---
DEFINITIONS
---

For the sake of this video, the input for SAT will be a formula in CNF, which is just a cojunction of disjunctions. The goal is output an assignment of variables that satisfies all clauses. An easy way to think of it is that you have groups of variables and at least one from each group has to be satisfied.

This formulation can't really be approximated, since the assignment of variables either exist or doesn't. We'll therefore generalize SAT to MAX-SAT and will no longer require that every group is satisfied, but instead that as many as possible are.

When talking about approximation algorithms, there are generally two types. The first is deterministic, for which we require that the solution they produce is (for our purposes) at most a constant times worse than the optimum. The other is randomized -- here we also want a result that is a constant times worse than the optimum, but in the expectation, since we could get really unlucky when randomizing, but we want good results in the average case.

---
RAND-SAT
---

When thinking about approximate algorithms for MAX-SAT, a good way to start is with the simplest thing you can think of -- assign the values randomly ($1/2$ for $0$ and $1/2$ for $1$) and hope for the best.

This approach is called RAND-SAT and, despite its simplicity, performs quite admirably. When looking at a single clause of $k$ literals, the chance that the algorithm doesn't satisfy it is that if all of the variables are set to false, so $\frac{1}{2^k}$. Therefore the probability that it does satisfy at least one variable is at least $1 - \frac{1}{2^k}$.

Since each clause contains at least one literal, the chance to satisfy each clause is at least $\frac{1}{2}$.

One thing to note is that this algorithm performs best when the clause is long. For example, if it contains 3 literals, the chance of satisfying it is close to $90%$! Keep this observation in mind, since it will be important later on.

---
LP-SAT
---

The second algorithm that we'll look at is LP-SAT. It will again be random, but we need a slight interlude about linear programming before describing it.

A linear programming problem contains real variables, linear inequalities that restrict them and a linear expression that you want to maximize. For this example, one optimal solution is TODO.

Linear programming can be used to elegantly formulate a lot of problems that might be tricky to solve using other means.

What we want to do is formulate MAX-SAT in terms of linear programming and solve it that way. To do this, we'll create two types of variables: one for each literal in the boolean formula, and one for each clause.

The inequalities should reflect the clauses from the boolean expression: we'll restrict clause variables by the formula variables, depending on how the clause looks.

The expression to maximize will be the sum of clause literals.

This formulation of the problem obviously only makes sense if the variables are integers (each literal variable can be only 0 or 1, and so can each clause). This slight change from real variables to zeroes and ones, however, makes this problem NP complete.

-- we can't assign a decimal value to the variable from the formula... or can we?
