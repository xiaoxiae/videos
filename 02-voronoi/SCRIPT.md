# Voronoi Diagrams

## Intro (Intro)

Voronoi diagrams are a way of partitioning a plane into regions, depending on how close they are to a given set of points.

Although the concept is very simple, there is a lot of things to think about when trying to generate a neat-looking Voronoi diagram.

## Creating a simple Voronoi diagram (Simple)

To create a simple Voronoi diagrams, let's first randomly pick the points (called seeds) that decide how to partition the plane. For clarity, we'll give each seed a color.

Each point on the plane belongs to the region of the closest seed.

## Distributing points more evenly (Points + 2)

This looks quite nice, but picking seeds randomly isn't usually what we want, since it can sometimes create uneven regions. Let's try something different.

When generating a seed, let's actually generate more candidate seeds, and pick the one that is furthest from the rest of the seeds. This approach is called Mitchel's best candidate algorithm and is a way to produce more natural-looking distribution.

Note that the number of candidates we're generating is proportional to how many have already been generated, since the more seeds we have, the harder it is to find a proper place for a new one.

## Metric (Chosing a different metric)
Another thing that we can tweak is the way we measure the distance between two points (called a metric).

For now, we've been using the euclidean metric, where the distance of two points is denoted by the distance of the line between them. This is very natural, but is definitely not the only way to do it.

## Borders (Adding borders)


## Colors (Making adjacent region colors different)
One thing you might have noticed is that in previous examples, the colors of the adjacent regions were always different.
This is something makes the pattern look better, since you don't have large areas in the same color.

A way to do this is convert the regions into a graph, color it such that no two adjacent vertices have the same color and use the colors on the diagram.

An interesting thing to note is that 4 colours should be enough, as every planar graph can be colored using four colors.


- https://blog.demofox.org/2017/10/20/generating-blue-noise-sample-points-with-mitchells-best-candidate-algorithm/
