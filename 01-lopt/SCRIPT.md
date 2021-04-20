# Practical Linear Programming

	MANIM: Intro
	TAG: Intro

<read the intro>

While this may seem dauting at first, it is rather easy to explain visually.

Consider this problem: <read the intro>

	MANIM: Visualize

We can visualize the constraints first as equalities defining lines, and then restricting to the appropriate part of the plane.

The solution that maximizes the expression $x + 3y$ is simply the point that is furthest valid point in the direction specified by the expression.

	MANIM: Visualizepy

To solve this programatically, we'll use Python and the package pulp.

We first import the entirety of the pulp package to work with.

We then define a linear programming problem, where the goal is to maximize.

Our variables are x and y, and our constraints and expression to maximize are as mentioned before

We then call the model's solve method with a parameter to suppress unnecessary debug messages and finally print out the found values of x and y.

	MANIM: KNAPSACK
	TAG: The Knapsack Problem

Linear programming gets much more interesting when we restrict our solutions to integers only. In the previous example, we saw that the solution was fractional, but this is not always useful for real-world problems, like the knapsack problem. In this problem, <read>

When restricting our solutions to integers, we could model this problem using linear programming.

We first define the data that we work with and create a new model. Again, our goal is to maximize.

The variables will be binary (0 or 1) and will denote, whether we include a given item in the knapsack or not.

The constraints are exactly what the problem states they are: the sum of the weights of the items we include cannot exceede the load capacity.

Finally, the expression we want to maximize are the prices of the items that we take

	CHROMATIC_NUMBER
	TAG: Chromatic Number

Lets look at one more problem that we can also model with integral linear programming. Chromatic nummber (denoted chi) is <read>.

For example, given the following graph, we can color it using a minimum of three colors (feel free to stop the video and think about why), so the chromatic number is 3.

TODO: We're minimizing!

The code is a little longer then the previous two examples, but is still pretty straigt forward.

TODO stuff for the chromatic number


