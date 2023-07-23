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

> Me climbing zooming out (as a grid)
> Yes, there are all unique text at the bottom

You probably don't know this about me, but I like to boulder.
Like a lot.
Honestly, a little too much.

> The Lattice training video

One of the things that fascinate me is the rise of replica boulders, which are made by scanning the holds on the real boulder and creating an exact indoor replica for training.

> A video of me taking pictures of a hold to the 3D model (showing the images that I take)
> Probably take tripod + camera + a clip microphone and take images with a phone
> Then something like COLMAP drag-n-drop and watch it reconstruct the models (again from the side)
> First walk there, take pictures, walk back, then at the PC doing the drag-n-drop (visually from phone to PC would be funny)
>   then somthing

Now the simplest way to obtain the models is to take images of the holds with a camera, place them into one of the readily available photogrammetry programs, wait a little (or a lot, depending on how many images you have) and viola, you've got the model... but how do you go from 2D images to 3D models?

> Left side images, right side model, something like ? in the middle, then zoom into the thingy

Like this is one of the problems where if you told me to solve it, I'd have literally no idea where to even begin, and I bet that you feel the same way.
But, as with many things in life, the magic is just math, which I'll attempt to explain in this video.


---
OVERVIEW
---

> left side images, right side the 3D model (interactively rendered and moved?)
> black box in the middle, then move into the blackbox

As I've previously mentioned, our goal is to start with a bunch of 2D images of an object, taken from different angles, and end up with a 3D model that resembles the object as closely as possible.
There are a number of problems we'll need to tackle as we go, but they can be broadly separated into two parts: sparse reconstruction and dense reconstruction.

For sparse reconstruction, we want to determine a handful of important features of the object and the 3D positions of the cameras.

We can then use those in dense reconstruction to generate a much larger number of features and from those a textured model.

Every photogrammetry software does more-or-less exactly this but with slightly different techniques and algorithms.
So for the sake of this video, I will cover the most common techniques and share additional resources in the description for those interested.

Okay, let's start with sparse reconstruction.


---
SPARSE RECONSTRUCTION
---

> show an image
> flash in SIFT descriptors of the image
> fade in another image and match multiple descriptors from one to another
> transform the images into cameras and project onto points that are seen by both

The core of sparse reconstruction are features.
We can think of features as spots in the images that are in some way interesting.
We do this because if we can match same features across multiple different images, we can triangulate where the cameras have to be for the geometry to make sense.

> go back to the image

But we're getting ahead of ourselves.
Let's first figure out how to find features.

> show the places we're talking about

As we've previously mentioned, we want positions in the image that are somehow interesting.

> TODO: explain how this is done via the scale space
> mention that it's a gaussian scale space, what a DoG is (no, not that dog)
> mention 3b1b video about convolutions
> also mention that the details are a bit tricky, but the main point is that we have a feature point if it's the local maximum in the adjacent scales
> since this creates a lot of points (some of which aren't all that great), additionally filter by using threshold (is it very bright/dark?)

One way would be to look at pixels that are smaller/larger than all of their neighbours (i.e. the local extremes).
This might work if the image was clean, but if you add any sort of noise or scale the image then all the features change, which probably shouldn't be happening.


TODO: stuff with the scale space

Now that we've determined where the features are, we'll calculate their descriptors.
These can be thought of as information about the feature and its surroundings, and it should be the same if the feature is present in multiple images (so that we can match it).

> make these centered at the feature we're looking at

We need these to be resilient to transforms like rotation, scaling, brightness and changes in perspective
This is honestly very sensible since moving from one angle to another can change any and all of those, so we have to be mindful of that.

> dominant orientations (rotation + affine transformation-invariant)


Okay, so at this point we have managed to detect features and compute their descriptors in all of their images, and we'd like to match features across multiple different images.
Now we could, for every feature, check all other features and mark those whose descriptors are similar as matches, but since each image can have thousands of features, this would be extremely slow.

Instead, we'll use a clever datastructure which speeds things up quite a bit.

> we want to identify nearest neighbours -- use a k-d tree and best-bin-first
> they should also be much better than others (ration between first and second)

So we've detected the features and matched them across images... and now what?
We'd like to look at the matched points across the images and use them to infer their position in space, but this is not as easy as it sounds.
To understand why, we'll have to make a slight detour into how a standard camera creates images.

> the pinhole model
> how far into affine coordinates do I want to go?
> that we want the center of the image, but it doesn't work like that
> sparse reconstruction lecture 3 -- show the pinhole model
> explain some basic math behind it (what happens when we change the focal length)
> explain how to get the matrix that we multiply by

...

> https://scipy-cookbook.readthedocs.io/items/bundle_adjustment.html
> https://www.comp.nus.edu.sg/~cs4243/lecture/camera.pdf

Bundle adjustment

---
DENSE RECONSTRUCTION
---



---
OTHER APPROACHES
---

> iPhone's lidar
> NERF (although not technically photogrammetry)
