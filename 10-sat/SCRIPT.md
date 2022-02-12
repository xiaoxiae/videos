---
INTRODUCTION
---

SAT is arguably one of the most important computer science problems when talking about P vs. NP. This is because a lot of problems from NP can easily be converted to SAT and there exists optimized solvers that you can use to compute the solution.

This means that when you're dealing with a problem you know is NP-complete, the easiest way is often to transform it to SAT and then feed it to one of the readily available SAT solvers, which will likely run much faster than any clever algorithm you come up with.

Sometimes, however, we really need our algorithms to run in polynomial time, in exchange for the solution being close to, but not quite the optimum. This is what we call approximation algorithms -- they run fast, but produce a solution that (for our purposes) at most a constant times worse than the optimum.

What is fascinating about SAT in particular and will be the main topic of this video is that the optimal SAT approximation algorithm is a clever combination of two other, seemingly unrelated approximation algorithms.

But let's slow down just a bit and get our definitions out of the way.

---
DEFINITIONS
---

For the sake of this video, SAT will be the problem of satisfying a formula in CNF form, which is just a cojunction of disjunctions. An easy way to think of it is that you have groups of variables and at least one from each group has to be satisfied.

MAX-SAT is the generalization of this problem. We no longer require that every group is satisfied, but instead that as many as possible are, which we'll try to maximize.

When talking about approximation algorithms, there are generally two kinds. The first kind is deterministic, for which we require that the solution they produce is at most a constant times worse than the optimum. The other is randomized -- here we also want a result that is a constant times worse, but in the expectation, since we could get really unlucky when randomizing, but we want good results „on the average“.

---
RAND-SAT
---

When thinking about approximate algorithms for MAX-SAT, a good way to start is with the simplest thing you can think of -- assign the values randomly ($1/2$ for true and $1/2$ for false) and hope for the best.

This approach is called RAND-SAT and, despite its simplicity, performs quite admirably. When looking at a single clause of $k$ literals, the chance that the algorithm doesn't satisfy it is that if all of the variables are set to false, the chance of which is $\frac{1}{2^k}$. Therefore the probability that it does satisfy at least one variable is $1 - \frac{1}{2^k}$.

Since each clause contains at least one literal, the chance to satisfy each clause is at least $\frac{1}{2}$.

One thing to note is that this algorithm performs best when the clause is long. For example, if it contains 5 literals, the chance of satisfying it is about $97%$! Keep this observation in mind, since it will be important later on.

---
LP-SAT
---

The second algorithm that we'll look at is LP-SAT. It will again be random, but we'll need a slight interlude about linear programming before describing it.

Linear programming is, in its nature, similar to SAT -- you have variables, linear inequalities that restrict them and an expression that you want to maximize. For this example, one optimal solution is TODO.

Now notice that we could relatively easily convert our DNF formula to be solved by linear programming: the variables will be the variables of the formula. Each clause will create one inequality that will be satisfied, if the sum of the variables will be at least one.
