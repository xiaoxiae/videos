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

> Will Bosi and BoD

You probably don't know this about me but I like to boulder.
Like a lot.
Honestly probably way too much.

Anyway, one of the things that fascinates me is the recent rise of replica boulders, which are made by scanning the holds on the real boulder and creating an exact indoor replica for training.

> A video of me taking pictures of a hold to the 3D model (directly project)

Now the simplest way to obtain the models without expensive sensors is to take images of the holds and use one of the readily available photogrammetry programs to generate their 3D models... buy how do they actually work?

Like this is one of the problems where if you told me to solve it, I'd have literally no idea where to even begin and I'd bet that you feel the same way.
But, as with many things in life, the magic is just math, which I'll attempt to explain in this video.


---
OVERVIEW
---

> left side images, right side the 3D model (interactively rendered and moved?)

As I've previously mentioned, our goal is to start with a bunch of 2D images of the hold (or... well... any object), taken from different angles, and end up with a textured 3D model that resembles the object as closely as possible.
There are a number of problems we'll need to tackle as we go, but they can be separated into two parts: sparse reconstruction and dense reconstruction.

For sparse reconstruction, we want to determine the 3D positions of the cameras and a small number of important features of the object.

We can then use those in dense reconstruction to generate a much larger number of features and convert them into a textured model.

Every photogrammetry software does exactly this but uses slighlty different techniques for each of the steps that usually trade speed, computational intensity and precision
For this video, I will cover the basics and share additional resources in the description for those interested.

Okay, let's start with sparse reconstruction.


---
SPARSE RECONSTRUCTION
---

> show an image of the rock

The basis of sparse reconstruction are features.
We can think of features as interesting spots in the images.
We do this because if we can match the same feature across multiple different images, we can triangulate where the cameras have to be for the geometry to make sense.

> actual window in a zoomed-in image
> mark some spots as features
> calculate some float value for each

> is this a window though?
To detect features in an image, we'll scan pixel by pixel, and say it's a feature if it's somehow interesting.
As an example, a white pixel surrounded by other white pixels is pretty not very interesting, while this sharp corner is.

> do like a mosaic of 4 by 4

Once we determine that this pixel should be a feature, we'll calculate its descriptor, which is a unique number for that feature that stays the same across all of the images so we can say that these features across these four images are the same one.
This is honestly very sensible since moving from one angle to another can change any and all of those, so we have to be mindful of that.

> scale-space differences (good features should be present in low-res versions)
> reference 3b1b for convolution
> dominant orientations (rotation + affine transformation-invariant)

Okay, so at this point we have managed to detect features and their descriptors in all of their images and we'd like to detect the same features across multiple images.
Now we could, for every feature, check all of the other features and mark those that are similar as matches, but there can be hundreds of thousands of points and so this won't work.
Instead, we'll use a clever datastructure which allows us to do this quickly.

> we want to identify nearest neighbours -- use a k-d tree and best-bin-first
> they should also be much better than others (ration between first and second)

So we've detected the features and matched them across images... and now what?
We'd like to TODO

Bundle adjustment

> do this visually somehow

We can then do some model verification but we don't want to do that for now

---
DENSE RECONSTRUCTION
---

TODO
