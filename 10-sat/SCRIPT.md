---
INTRODUCTION
---

SAT, or the boolean satisfiability problem is arguably one of the most important computer science problems when talking about P vs. NP. This is because a lot of problems from NP can easily be converted to SAT and there exists optimized solvers that you can use to compute the solution.

Sometimes, however, we need our algorithms to run in polynomial time, in exchange for the solution being close to, but not quite the optimum. This is what we call approximation algorithms -- they run fast, but produce a solution that is (for our purposes) at most a constant times worse than the optimum.

What is fascinating about SAT in particular and will be the main topic of this video is that the optimal SAT approximation algorithm is a clever combination of two other, seemingly unrelated approximation algorithms, which intuitively shouldn't work well, but turns out to be the optimal way to do things.

But let's slow down just a bit and get our definitions out of the way.

---
DEFINITIONS
---

For the sake of this video, SAT will be the problem of satisfying a formula in CNF, which is just a cojunction of disjunctions. An easy way to think of it is that you have groups of variables and at least one from each group has to be satisfied.

MAX-SAT is the generalization of this problem. We no longer require that every group is satisfied, but instead that as many as possible are, which we'll try to maximize.

When talking about approximation algorithms, there are generally two types. The first is deterministic, for which we require that the solution they produce is at most a constant times worse than the optimum. The other is randomized -- here we also want a result that is a constant times worse than the optimum, but in the expectation, since we could get really unlucky when randomizing, but we want good results in the average case.

---
RAND-SAT
---

When thinking about approximate algorithms for MAX-SAT, a good way to start is with the simplest thing you can think of -- assign the values randomly ($1/2$ for true and $1/2$ for false) and hope for the best.

This approach is called RAND-SAT and, despite its simplicity, performs quite admirably. When looking at a single clause of $k$ literals, the chance that the algorithm doesn't satisfy it is that if all of the variables are set to false, so $\frac{1}{2^k}$. Therefore the probability that it does satisfy at least one variable is $1 - \frac{1}{2^k}$.

Since each clause contains at least one literal, the chance to satisfy each clause is at least $\frac{1}{2}$.

One thing to note is that this algorithm performs best when the clause is long. For example, if it contains 5 literals, the chance of satisfying it is almost $97%$! Keep this observation in mind, since it will be important later on.

---
LP-SAT
---

The second algorithm that we'll look at is LP-SAT. It will again be random, but we'll need a slight interlude about linear programming before describing it.

Linear programming is, in its nature, similar to MAX-SAT -- you have variables, linear inequalities that restrict them and a linear expression that you want to maximize. For this example, one optimal solution is TODO. TODO: denoted ...

What we want to do is use linear programming to solve MAX-SAT. For this we'll create two types of variables: one variable for each variable in the boolean formula that will be set to 0 if it's false and 1 if true, and one for each clause that will be set to 0 if it's not satisfied and 1 if it is.

TODO: animation of the variables and inequalities that appear when I'm talking about them
TODO: 0 <= x_i <= 1 is a rule too

The expression to maximize will be easy: we want to maximize the number of satisfied clauses. The other inequalities should reflect the boolean expression: we'll restrict clause variables by the formula variables depending on how the clause looks.

This obviously only makes sense if the variables are integers -- we can't assign a decimal value to the variable from the formula... or can we?

The problem with our approach is that solving linear programming when restricting the variables to integers is NP complete. We'll therefore
