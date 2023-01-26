---
title: The (a,b)-tree – most elegant search data structure
subtitle: Video Script
author: Tomáš Sláma
header-includes:
- \pagenumbering{gobble}
- \newgeometry{left=15mm, right=40mm, top=15mm, bottom=15mm, marginparwidth=30mm}
---

\hrule
\vspace{1.5em}

<!-- general notes:
- the binary trees have to have leafs (like actual leafs), just like the a,b trees
-->

---
FEVER DREAM
---

\marginpar{\texttt{Fever}}
Has this ever happened to you?  <!-- grainy footage of AVL rotations -->

You're balancing your AVL tree, making sure it's nice and neat and suddenly: oh oh, you made a wrong rotation! <!-- make the wrong rotation and an old timey oh oh! text -->
The tree bursts into flames before you can even blink and you're left wondering: is there a better way?

Well, there is!

Introducing the (a,b)-tree.
It's fast!
It's intuitive!
And most importantly: it doesn't have rotations!

AVL, go to hell, AVL, go to hell, AVL, go to hell! <!-- fade out the chant and have ripples + some fadeout music  -->

---
INTRODUCTION
---

\marginpar{\texttt{Intro}}

Wow that was a weird dream.

Anyway, in today's video, I'll introduce you to $(a,b)$-trees, which are a more generalized version of binary search trees. <!-- first write a,b tree and then show an actual a,b tree -->
As you can see, they are no longer binary -- each node has a variable number of keys, depending on the values of $a$ and $b$. <!-- highlight the node and key -->

Just like binary trees, they are used for storing and quickly locating items based on their keys. <!-- show a binary tree containing the same information -->
In a binary tree, if you want to find a key (for example 4), you go left if the key in the current node is larger, otherwise you go right, eventually either finding the key or reaching a leaf, at which point you know the key is not present. <!-- show target: 4 and path in the binary tree -->

For an $(a,b)$-tree, this procedure is very similar, the only difference being that either the key is in the current node, or it's not and you follow the edge between the keys where it should be, again either finding it or getting to a leaf. <!-- show the search in the a,b tree; make it have values 1,2,3,4,5... -->

$(a,b)$-trees address a number of shortcomings of binary trees, mainly the fact that they can easily become unbalanced -- repeatedly inserting items into a binary tree without other operations can make them lean to one side, rendering all operations significantly slower. <!-- show the imbalance -- keep inserting smaller values -->
There are a number of ways to address this problem, but they are pretty messy and not as elegant as $(a,b)$-trees.

So, without further ado, let's dive in.

---
BASICS
---

This is an $(a,b)$-tree.
It is made up of nodes which contain keys that are always sorted from left to right.
The only exception are the leafs, which don't contain any keys.
Each key separates two subtrees, the left one having keys that are less than it and the right one having keys that are greater than it.

The parameters $a$ and $b$ denote the number of children each non-leaf node can have.
This is therefore a $(2,4)$-tree, since each node has between $2$ and $4$ children.
There is one exception, which is the root -- while nodes can have between $a$ and $b$ children, the root can have between $2$ and $b$ children.
This seems a little arbitrary but it will make sense as we go through the tree's operations. <!-- make a list of the axioms to the left -->

To keep the operations on the tree fast, we require all leafs to be in the same depth. <!-- yet again, write this to the right -->
This, in combination with the restriction on the number of children, forces the tree to have logarithmic depth (in the number of its keys).
Feel free to pause here and prove this yourself, it's a nice sanity check.

And, finally, we require that $a \ge 2$ and $b \ge 2a - 1$.
The limit on $a$ is intuitive, since we don't want the tree to have non-leaf nodes with no keys.
The limit on $b$ is a little more cryptic, but will again make sense when we start looking into the operations.

Speaking of the operations, the ones that I will cover in this video are

- searching for a key,
- inserting a key and
- deleting a key


---
SEARCH
---

Let's start with the simplest operation, searching.

To search for a key, we start in the root node and do the following:

- find where in the current node the key should be (using either normal or binary search):
	- if it's there, we're done!
	- if it's not there, follow the edge between the keys where it should be and repeat

Eventually, we'll either find it, or arrive in a leaf, at which point we know it's not present in the tree.

Since we visited each layer at most once, the operation runs in time $\mathcal{O}(\log n)$.


---
INSERTION
---

Let's now try to insert a key.

Assuming that the key is not present, we'll run search and end up in one of the tree's leafs.
Now we simply insert the key to the leaf's parent node, additionally creating a new leaf.

If this didn't break the condition on the number of children of a node (i.e. if the node still has at most $b$ children), we're done.
Otherwise, we split the node in two (down the middle) and, since this adds a new child to the node above, we move the middle key up
Since this might make the node above break the condition, we have to repeat the process until we reach the root.

This is where the $b \ge 2a - 1$ condition comes in handy, since splitting the node down the middle and removing one key makes the sides have at least $\lfloor b / 2 \rfloor$ nodes, which is at least $a$.
Also, if we split the root node, we'll have to create a new root node that will have only two children, which we can only do because the root node can have between $2$ and $b$ children.


---
DELETION
---

As for deletion, it is a little trickier.

Let's again assume that the key is present and we run search to find it.

If it's in the second to last layer, we can simply delete it, along with one of the leafs.
If it's not, we'll do it the same way as removing a key from a binary tree: we'll replace it with with the leftmost key of its right subtree and thus reducing the problem to the previous case.

Either of those two could have broken the condition on the number of children of a node, having less than $a$ children. TODO: the two cases fml


---
PERFORMANCE
---

One thing that makes $(a,b)$-trees great is the fact that they are very cache-friendly.

To simplify: a cache is made up of lines of some size (usually 64B).
The speed of retrieving a single byte from the cache is the same as retrieving an entire line, meaning that the parameters $a,b$ can be chosen such that a node fits into a single cache line, which drastically speeds up the operations.

To show you what I mean by 'drastic', I used an open-source C++ $(a,b)$-tree implementation (link in the description) to run benchmarks on my laptop for varying $a$ and $b$.
As the graph shows, the best choice is a $(4,8)$-tree.
This makes sense, since the size of my laptop's cache lines is 64B and a node of a $(4,8)$-tree is just $8$ 64b pointers to its children, which takes up exactly 64B.


---
R&B TREE == $(2,4)$-TREE
---

For those interested, here is one more fun thing about (a,b)-trees: TODO
