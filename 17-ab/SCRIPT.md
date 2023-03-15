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

<!--
TODO: dark gray -> darker gray
TODO: target fadeins vs writes (fadeins better?)
-->



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

For an $(a,b)$-tree, this procedure is very similar, the only difference being that either the key is in the current node, or it's not and we follow the edge where it should be, again either finding it or getting to a leaf. <!-- again animate getting to a leaf -->

$(a,b)$-trees address a number of shortcomings of binary trees, mainly the fact that they can easily become unbalanced -- repeatedly inserting items into a binary tree without other operations can make them lean to one side, rendering all operations significantly slower.
There are a number of ways to address this problem (like AVL trees or R&B trees), but they are not nearly as elegant as $(a,b)$-trees.

So, without further ado, let's dive in.


---
BASICS
---

\marginpar{\texttt{Basics}}

This is an $(a,b)$-tree.
It is made up of nodes, which contain keys that are always sorted from left to right.
The only exception are the leafs, which don't contain any keys.

Each key separates two subtrees, the left one having smaller keys and the right one having larger.

The parameters $a$ and $b$ denote the number of children each non-leaf node can have, with $a$ being the minimum and $b$ the maximum.
This is therefore a $(2,4)$-tree, since each node has between $2$ and $4$ children.
There is one exception, which is the root -- while other nodes can have between $a$ and $b$ children, the root can have between $2$ and $b$ children, otherwise building $(a,b)$-trees with certain numbers of keys wouldn't be possible.

To keep the operations on the tree fast, there are some things the tree must satisfy at all times.
Firstly, all leafs must be on the same layer, which forces the tree to have logarithmic depth.

Secondly, $a \ge 2$ and $b \ge 2a - 1$.
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

<!-- TODO: case one: present, case two, not present -->

Let's start with the simplest operation, searching.
We've already seen an example, but let's cover it more formally.

To search for a key, we start in the root and do the following: first, find where in the current node the key should be:
- if it's not there (as in this case), go to the subtree where it should be and repeat the process <!-- TODO: ORANGE color? -->
- on the other hand, if it's there, we're done!

Let's see what happens when we search for a key that isn't in the tree.
Again, we repeat the steps... ending up in a leaf with nowhere else to go, so we know with absolute certainty that the key is not present.


---
INSERTION
---

\marginpar{\texttt{Insertion}}

Since just searching for keys is boring, let's try to insert one.

Assuming that the key is not present, we'll run search and end up in one of the tree's leafs. <!-- TODO: again red color, just like previously -->
Then we simply insert the key into the leaf's parent node, creating a new leaf in the process.

Now it might seem like we're be done, but remember that a node can have at most $b$ children, which this node doesn't satisfy.

Pause here and try to solve this problem; chances are the first thing you think of is the correct solution.

That's right, the answer is violence!
We split the node down the middle, moving one key up to accomodate for the newly created node.
This might make the node above break the condition (which luckily hasn't happened here), so we have to repeat the process until there are no more broken nodes. <!-- highlight the top node -->

Let's insert a few more values to better illustrate what the operation does to the tree.

Notice here that splitting the root node is a somewhat special case since it creates a new root node.

While all this seems sensible, what we've done here is only possible thanks to our carefuly selected conditions:

The first is tha $b \ge 2a - 1$, since removing a key and splitting a node down the middle makes the sides have at least $\lfloor (b + 1 - 1) / 2 \rfloor$ nodes, which the condition ensures is at least $a$
The second is the root can have $2$ or more children, which happens when it's split.


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
