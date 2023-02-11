---
title: The most elegant search data structure | (a,b)-trees
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}


---
FEVER DREAM
---

\marginpar{\texttt{Fever}}
Has this ever happened to you?  <!-- grainy footage of AVL rotations -->

You're balancing your AVL tree, making sure it's nice and neat and suddenly: oh no, you made a wrong rotation!
The tree bursts into flames before you can even blink and you're left wondering: is there a better way?

Well, there is!

Introducing the (a,b)-tree.
It's fast!
It's simple!
And most importantly: it doesn't have rotations!

AVL, go to hell, AVL, go to hell, AVL, go to hell!


---
INTRODUCTION
---

\marginpar{\texttt{Intro}}

Wow that was a weird dream.

Anyway, in today's video, I'll introduce you to $(a,b)$-trees, which are a more generalized version of binary search trees.
As you can see, they are no longer binary, since their nodes have more than two children.

Just like binary trees, they are used for quickly storing and locating items based on their keys.
If we want to find a key (for example 5) in a binary tree, we start in the root and go right if the target is larger than the current node, else we go left.
In this case, the key is found.
However, if we tried the same with a key that isn't in the tree, we soon reach a leaf, at which point we know the key is not present.

For an $(a,b)$-tree, this procedure is very similar, the only difference being that either the key is in the current node, or it's not and we follow the edge between the keys where it should be, again either finding it or getting to a leaf. <!-- again animate getting to a leaf -->

$(a,b)$-trees address a number of shortcomings of binary trees, mainly the fact that they can easily become unbalanced -- repeatedly inserting items into a binary tree without other operations can make them lean to one side, rendering all operations significantly slower.
There are a number of ways to address this problem (like AVL trees or R&B trees), but they are not nearly as elegant as $(a,b)$-trees. <!-- show -->

So, without further ado, let's dive in.


---
BASICS
---

\marginpar{\texttt{Basics}}

This is an $(a,b)$-tree.
It is made up of nodes, which contain keys that are always sorted from left to right.
The only exception are the leafs, which don't contain any keys.

Each key separates two subtrees, the left one having keys that are less than it and the right one having keys that are greater than it.

The parameters $a$ and $b$ denote the number of children each non-leaf node can have.
This is therefore a $(2,4)$-tree, since each node has between $2$ and $4$ children.
There is one exception, which is the root -- while other nodes can have between $a$ and $b$ children, the root can have between $2$ and $b$ children, otherwise building $(a,b)$-trees containing certain numbers of keys wouldn't be possible.

To keep the operations on the tree fast, there are some things the tree must satisfy at all times, the first being that all leafs to be in the same depth -- this forces the tree to have logarithmic depth (in the number of keys).
Feel free to pause here and prove this yourself as a sanity check.

The second condition is that $a \ge 2$ and $b \ge 2a - 1$.
The limit on $a$ is intuitive, since we don't want the tree to have nodes with 0 keys (other than leafs).
The limit on $b$ is a little more cryptic, but will make sense when we start looking into the tree's operations.

Speaking of the operations, the ones that I will cover in this video are

- searching for a key,
- inserting a key and
- deleting a key


---
SEARCH
---

\marginpar{\texttt{Search}}

Let's start with the simplest operation, searching.
We've already seen an example, but let's cover it more formally.

To search for a key, we start in the root and do the following:

- first, find where in the current node the key should be (using either normal or binary search):
	- if it's there, we're done!
	- if it's not there, go to the subtree where it should be and repeat

Eventually, we'll either find it, or arrive in a leaf, at which point we know it's not present in the tree.

Since we visited each layer at most once, the operation runs in time $\mathcal{O}(\log n)$.


---
INSERTION
---

Let's now try to insert a key.

Assuming that the key is not present, we'll run search and end up in one of the tree's leafs.
Then we simply insert the key to the leaf's parent node, creating a new leaf in the process.

Now it might seem like we're be done, but remember that a node can have at most $b$ children.
If this is still the case then great, we're actually done.
Otherwise, we split the node in two (down the middle) and, since this adds a new child to the node above, we move the middle key up.
Since this might make the node above break the condition, we have to repeat the process until we reach the root.

This is where the cryptic $b \ge 2a - 1$ condition comes in handy, since splitting the node down the middle and removing one key makes the sides have at least $\lfloor b / 2 \rfloor$ nodes, which the condition ensures is at least $a$.
Also, if we happen to split the root node, we'll have to create a new root node that will have two children, which we can only do because the root node can have between $2$ and $b$ children.


---
DELETION
---

As for deletion, it is a little trickier.

Let's assume that the key is present and we run search to find it.

If it's in the second to last layer, we can simply delete it, along with one of its leafs.
If it's not, we'll use the same trick as when removing a key from a binary tree: we'll replace it with the leftmost key of its right subtree, thus reducing the problem to the previous case.
If you haven't seen this trick before, feel free to pause here and make sure that this operation makes sense.

After removing the key, we could again break the condition on the number of children, this time having less than $a$.
Since the node has at least one other an adjacent node, we can do one of two things to fix our problem:

- merge the two nodes or
- steal one of the adjacent node's keys

If the neighbouring node has $a$ children, we can't just steal a key, so we'll have to merge.
This removes a key from the node above, moving it down, which might again break its condition, so we'll have to recursively fix the same problem on the node above.

Otherwise, if it has more than $a$ children, we'll just take its key and we're done.


---
PERFORMANCE
---

One thing that makes $(a,b)$-trees great is the fact that they are very cache-friendly, and here is why.

Essentially, a cache is made up of lines of some size (usually 64B).
The speed of retrieving a single byte from the cache is the same as retrieving an entire line, meaning that the parameters $a,b$ can be chosen such that a node fits into a single cache line, which drastically speeds up the operations.

To show you what I mean by 'drastic', I used an open-source C++ $(a,b)$-tree implementation (link in the description) to run benchmarks on my laptop for varying $a$ and $b$.

The graph shows a very complex behavior that I'm not going to explain, but the most important thing is that the best parameter choice is a $(8,16)$-tree.
This makes sense, since the size of my laptop's cache lines is 64B, and a node of a $(4,8)$-tree is just $8$ 64b pointers to its children, which takes up exactly 64B.


---
R&B TREE == $(2,4)$-TREE
---

For those interested, here is one more fun thing about (a,b)-trees: TODO
