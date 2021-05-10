=== Voronoi Diagrams ===

--- Intro ---

# Intro (Intro)

Voronoi diagrams are a way of partitioning a plane into regions, depending on how close they are to a given set of points. Although they seem like a simple TODO -- že se hodí

TODO: ty animace různých Voroného diagramů

# Creating a simple Voronoi diagram (Simple)

To create a simple Voronoi diagram, let's first randomly pick the points (called seeds) that decide how to partition the plane. For clarity, we'll give each seed a color.

Each point on the plane then belongs to the region of the closest seed.

--- Points  ---

# Distributing points more evenly (Points)

This looks quite nice, but picking seeds randomly isn't usually what we want, since it can sometimes create uneven regions. Let's try something different.

When generating a seed, let's actually generate more candidates, and pick the one that is furthest from the others. This approach is called Mitchel's best candidate algorithm and is a way of producing more natural-looking point distributions.

Note that the number of candidates we're generating is proportional to how many have already been generated, since the more seeds we have, the harder it is to find a proper place for a new one.

TODO: animace toho, jaké jsou rozdíly

--- Metric  ---

# Chosing a different metric (Metric)
Another thing that we can tweak is the way we measure the distance between two points (called a metric).

Until now, we've been using the euclidean metric, where the distance of two points is the length of the line between them.

This is very natural, but is definitely not the only way to do it.

Let's look at the Manhattan (or taxicab) distance instead. Here, the distance is the absolute value of $x$ and $y$.

TODO: lajna

TODO: side-by-side porovnávání stejných seedů a různých metrik

--- Assigning colors  ---

# Assigning colors (Colors)
One thing you might have noticed is that in previous examples, the colors of the adjacent regions were always different.

This was no coincidence -- they weren't selected randomly, but in a way that no two adjacent areas have the same one. This is something that can make the pattern look much better, since we don't have large areas having the same color.

TODO: animace těch seedů

A way to do this is convert the regions into a graph, color it such that no two adjacent vertices have the same color and use the colors on the diagram. Note that 4 colours should always be enough, as every planar graph can be colored using four colors.

--- Applications  ---

# Applications (Applications)
Voronoi diagram can be found in many places in nature, including things like the wings of a dragonfly, giraffe patterns, dried-up clay and foam bubbles.

Another place where they come up is in maps - for exampe, a map of the nearest airports for all places on earth.


One more example is their use in stippling algorithms, a very nice one being the Weighted Linde-Buzo-Gray Stippling.
