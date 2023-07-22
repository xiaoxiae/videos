---
title: Demystifying Photogrammetry | From 2D Images to 3D Models
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \usepackage{todonotes}
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=70mm, top=15mm, bottom=15mm, marginparwidth=60mm}
- \newcommand{\fix}[1]{\todo[color=green!40]{#1}}
- \newcommand{\note}[1]{\todo[color=blue!40]{#1}}
---

\hrule
\vspace{1.5em}

---
INTRODUCTION
---

> Thumbnail images on left -> object on the right? Or an object on a pedestal and images from different angles?
> The second thing maybe better (+ render in blender for nice effect)
> maybe half wireframe half the model (same thing as in my thesis)
> Do this with a nice rock outside (so there is a lot of detail)

> Will Bosi and BoD

You probably don't know this about me, but I like to boulder.
Like a lot.
Honestly, a little too much.

Anyway, one of the things that fascinate me is the rise of replica boulders, which are made by scanning the holds on the real boulder and creating an exact indoor replica for training.

> A video of me taking pictures of a hold to the 3D model, (showing the images that I take)
> Then something like COLMAP drag-n-drop and watch it reconstruct the models

Now the simplest way to obtain the models without expensive sensors is to take images of the holds and use one of the readily available photogrammetry programs to generate their 3D models... but how do they actually work?

> Left side images, right side model, something like ? in the middle, then zoom into the thingy

Like this is one of the problems where if you told me to solve it, I'd have literally no idea where to even begin, and I bet that you feel the same way.
But, as with many things in life, the magic is just math, which I'll attempt to explain in this video.


---
OVERVIEW
---

> left side images, right side the 3D model (interactively rendered and moved?)

As I've previously mentioned, our goal is to start with a bunch of 2D images of an object, taken from different angles, and end up with a 3D model that resembles the object as closely as possible.
There are a number of problems we'll need to tackle as we go, but they can be broadly separated into two parts: sparse reconstruction and dense reconstruction.

For sparse reconstruction, we want to determine a handful of important features of the object and the 3D positions of the cameras.

We can then use those in dense reconstruction to generate a much larger number of features and from those a textured model.

Every photogrammetry software does more-or-less exactly this but uses slightly different techniques and algorithms.
For the sake of this video, I will cover the most common techniques and share additional resources in the description for those interested.

Okay, let's start with sparse reconstruction.


---
SPARSE RECONSTRUCTION
---

> show an image of the rock
> flash in SIFT descriptors of the image
> fade in another image and match multiple descriptors from one to another
> transform the images into cameras and project onto points that are seen by both

The core of sparse reconstruction are features.
We can think of features spots in the images that are somehow interesting and distinctive.
We do this because if we can match the same feature across multiple different images, we can triangulate where the cameras have to be for the geometry to make sense.

> now zoom back to the image
> show the places we're talking about

For a position in the image to be considered a feature, we want it to be somehow interesting.
As an example, this <TODO> is not very interesting, while this sharp corner is.

> TODO: explain how this is done via the scale space
> mention that it's a gaussian scale space, what a DoG is (no, not that dog)
> mention 3b1b video about convolutions
> also mention that the details are a bit tricky, but the main point is that we have a feature point if it's the local maximum in the adjacent scales
> since this creates a lot of points (some of which aren't all that great), additionally filter by using threshold (is it very bright/dark?)

Once we determine where the features are, we'll calculate their descriptors.
These can be thought of as the descriptions of the feature and it surroundings, and it should stay the same if the feature is present in multiple images (so that we can match it).

> scale-space differences (good features should be present in low-res versions)
> dominant orientations (rotation + affine transformation-invariant)

This is honestly very sensible since moving from one angle to another can change any and all of those, so we have to be mindful of that.

Okay, so at this point we have managed to detect features and their descriptors in all of their images and we'd like to detect the same features across multiple different images.
This is a pretty standard problem called the "Nearest neighbor search," where the task is to find the closest TODO this is too long
Now we could, for every feature, check all other features and mark those that are similar as matches, but since each image can have thousands of points, this would be very slow.

Instead, we'll use a clever datastructure which allows us to do this much quicker.

> we want to identify nearest neighbours -- use a k-d tree and best-bin-first
> they should also be much better than others (ration between first and second)

So we've detected the features and matched them across images... and now what?
We'd like to look at the matched points across the images and use them to infer their position in space, but this is not as easy as it sounds.
To understand why, we'll have to make a slight detour into how a standard camera creates images.

> the pinhole model
> that we want the center of the image
> https://scipy-cookbook.readthedocs.io/items/bundle_adjustment.html
> https://www.comp.nus.edu.sg/~cs4243/lecture/camera.pdf

Bundle adjustment

---
DENSE RECONSTRUCTION
---

TODO
