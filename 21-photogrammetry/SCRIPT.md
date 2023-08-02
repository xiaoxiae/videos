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

Anyway, one of the things that fascinate me is the rise of replica boulders, which are made by scanning the holds on the real boulder and creating an exact indoor replica for training.

> A video of me taking pictures of a hold to the 3D model (showing the images that I take)
> Probably take tripod + camera + a clip microphone and take images with a phone
> Then something like COLMAP drag-n-drop and watch it reconstruct the models (again from the side)
> First walk there, take pictures, walk back, then at the PC doing the drag-n-drop (visually from phone to PC would be funny)
>   then somthing

Now the simplest way to obtain the models is to take images of the holds with a camera, place them into one of the readily available photogrammetry programs, wait a little (or a lot, depending on how many images you have) and viola, you've got the model... but how did we go from images to the models? TODO clunky

> Left side images, right side model, something like ? in the middle, then zoom into the thingy

Like this is one of the problems where if you told me to solve it, I'd have literally no idea where to even begin, and I bet that you feel the same way.
But, as with many things in life, the magic is just math, which I'll attempt to explain in this video.


---
OVERVIEW
---

> left side images, right side the 3D model (interactively rendered and moved?)
> black box in the middle, then move into the blackbox 

> a line should appear in the middle separating the sparse and dense reconstruction

As I've previously mentioned, our goal is to start with a bunch of 2D images of an object, taken from different angles, and end up with a 3D model that resembles the object as closely as possible.
There are a number of problems we'll need to tackle as we go, but they can be broadly separated into two parts: sparse reconstruction and dense reconstruction.

For sparse reconstruction, we want to obtain a handful of important features of the object and the 3D positions of the cameras.

We can then use those in dense reconstruction to generate a much larger number of features and from those a textured model.

> show some common photogrammetry software in a grid (in font)
> then fade these out and show a "link in the description"

Every photogrammetry software does more-or-less exactly this but with slightly different techniques and algorithms.
So for the sake of this video, I will cover the most common techniques and share additional resources in the description for those interested.

Okay, let's start with sparse reconstruction.


---
SPARSE RECONSTRUCTION
---

> show an image
> flash in SIFT descriptors of the image
> fade in another image and match multiple descriptors from one to another (via green lines), maybe don't match some
> transform the images into cameras and project onto points that are seen by both

The core of sparse reconstruction are features.
We can think of features as spots in the images that are in some way interesting.
We do this because if we can match the same features across multiple different images, we can triangulate where the cameras have to be for the geometry to make sense.

> go back to the image

But we're getting ahead of ourselves.
Let's first figure out how to find the features.

> grayscale the image (smoothly)
> show two pixels (drag them out) and why it's hard for RGB images
> find the correct value for the size of the images - we want enough features for it to be interesting (not too much, not too little)
> maybe something like 400x300
> we can animate the shrinking as literally scale and then zoom (or, well, scale back) while showing the dimensions and having the image slightly faded

For the sake of simplicity, we'll be working with grayscale images for the rest of the video, otherwise comparing values of pixels becomes complicated.
Let's also shrink them down a bit to see the pixel values better.

> show the places we're talking about

As we've previously mentioned, we want to find positions in the image that are somehow interesting.

> visually add noise/scale down / do the transformations

A simple algorithm could, for example, look at all pixels and pick those that are smaller/larger than all of their neighbors (i.e. local extremes).
This might work if the image has good quality, but if you add just a little bit of noise or change the image using some basic transformations, you can see that the features change quite drastically, which means that they are unstable.

> TODO: explain how this is done via the scale space (that we want features that are present even if we downscale)
> mention that it's a gaussian scale space, what a DoG is (no, not that dog)
> also mention that the details are a bit tricky, but the main point is that we have a feature point if it's the local maximum in the adjacent scales
> since this creates a lot of points (some of which aren't all that great), additionally filter by using threshold (is it very bright/dark?)

We obviously don't want that, so we'll use a better approach called SIFT, which stands for Scale-Invariant Feature Transform.
SIFT is based on the idea that a good feature should still be present when we reduce the image detail by scaling down or blurring.

> TODO: visually show that SIFT is much more resilient to this using the same operations (side by side)

Here is a side-by-side comparison.


> animate some numbers appearing for each feature
> then take a specific one and show a line + zoom in on the images

Now that we've determined where the features are, we need to calculate their descriptors.
Descriptors store information about the feature and its surroundings and, ideally, a feature should have very similar descriptors across multiple images and they should also be very different from other features, so we can correctly match them.

For example, a simple descriptor could just be the average value of the pixels near its position.
This is unsurprisingly as bad as it is simple, and we can see this by trying it on these two images -- yeah, that doesn't look great.

This approach is bad for a few reasons, the most important being that numbers aren't enough.
We want to be able to encode more than just brightness and so we'll need to use vectors.

> add something like a note about the Sobel operator, which is how we calculated.
> then do the same operations on the image

An improved descriptor could then be a vector with a magnitude of the average value and orientation set to the image gradient (i.e. the direction of the color change).
This should at least somewhat improve stability when rotating or scaling the image, but, again, not by much

Let's improve this a bit and say that a descriptor is actually a lot of vectors ...


Okay, so at this point we have managed to detect features and compute their descriptors in all of their images, and we'd like to match the same features across multiple different images by comparing their descriptors.
Now we could, for every feature, check all other features and mark those whose descriptors are similar as matches, but since each image can have thousands of features, this would be extremely slow.

So, to speed things up, we'll use a clever datastructure.

> explain best-bin-first - that it's greedy but it speeds things up by orders of magnitude and doesn't incur a significant error
> they should also be much better than others (ration between first and second)

So we've detected the features and matched them across images... and now what?
We'd like to look at the matched features across the images and use them to infer their position in space, but this is not as easy as it sounds.
To understand why, we'll have to make a slight detour into how a standard camera creates images.

> the pinhole model + homogeneous coordinates
> how far into homogeneous coordinates do I want to go?
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
