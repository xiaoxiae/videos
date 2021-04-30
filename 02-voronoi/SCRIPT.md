# Voronoi Diagrams

## Intro (Intro)

[intro1] Voronoi diagrams are a way of partitioning a plane into regions, depending on how close they are to a given set of points.

[intro2] Although the concept is simple, there is a lot of things to think about when trying to generate a neat-looking Voronoi diagram.

## Creating a simple Voronoi diagram (Simple)

[simple1] To create a simple Voronoi diagram, let's first randomly pick the points (called seeds) that decide how to partition the plane. For clarity, we'll give each seed a color.

[simple2] Each point on the plane then belongs to the region of the closest seed.

## Distributing points more evenly (Points + 2)

[points1] This looks quite nice, but picking seeds randomly isn't usually what we want, since it can sometimes create uneven regions. Let's try something different.

[points2] When generating a seed, let's actually generate more candidates, and pick the one that is furthest from the others. This approach is called Mitchel's best candidate algorithm and is a way of producing more natural-looking point distributions.

[points3] Note that the number of candidates we're generating is proportional to how many have already been generated, since the more seeds we have, the harder it is to find a proper place for a new one.

## Metric (Chosing a different metric)
[intro8] Another thing that we can tweak is the way we measure the distance between two points (called a metric).

[intro9] Until now, we've been using the euclidean metric, where the distance of two points is the length of the line between them. 

[intro10] This is very natural, but is definitely not the only way to do it.

[metric3] Let's look at the Manhattan (or taxicab) distance instead. Here, the distance is the absolute value of $x$ and $y$

## Colors (Assigning colors)
One thing you might have noticed is that in previous examples, the colors of the adjacent regions were always different.
This was no coincidence -- they weren't selected randomly, but in a way that no two adjacent areas have the same one. This is something that can make the pattern look much better, since we don't have large areas having the same color.

A way to do this is convert the regions into a graph, color it such that no two adjacent vertices have the same color and use the colors on the diagram.

An interesting thing to note is that 4 colours should always be enough, as every graph that can be drawn on the plane without intersecting itself can be colored using four colors. This is called the four-color theorem.

- https://blog.demofox.org/2017/10/20/generating-blue-noise-sample-points-with-mitchells-best-candidate-algorithm/
