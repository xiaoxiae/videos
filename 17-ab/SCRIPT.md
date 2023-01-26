---
title: (a,b)-trees – the most elegant search data structure
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

There is!

Introducing the (a,b)-tree!
It's fast!
It's intuitive!
And most importantly: it doesn't have rotations!

AVL, go to hell, AVL, go to hell, AVL, go to hell!

---
INTRODUCTION
---

\marginpar{\texttt{Intro}}

Wow that was a weird dream.

Anyway, in today's video, I'd like to show you $(a,b)$-trees, which are a more generalized version of binary search trees. <!-- first write a,b tree and then show an actual a,b tree -->
As you can see, they are no longer binary -- each node has a variable number of keys, depending the values of $a$ and $b$. <!-- highlight the node and key -->

Just like binary trees, they are used for quickly locating keys they contain. <!-- show a binary tree containing the same information -->
If you want to find a key (say 4) in this binary tree, you go left if the key in the current node is larger, else you go right, eventually either finding the key or reaching the bottom, at which point you know is not present. <!-- show target: 4 and path in the binary tree -->

For an (a,b)-tree, this procedure is very similar, except you follow the edge between the keys in the node where it should be. TODO: comment on the procedure <!-- show the search in the a,b tree; make it have values 1,2,3,4,5... -->

(a,b)-trees address a number of shortcomings of binary trees, mainly the fact that binary trees can easily become unbalanced -- repeatedly adding items to a binary tree without other operations can make them unbalanced (i.e.) lean to one side, making all operations significantly slower. <!-- show the imbalance -- keep adding smaller values -->
There are a number of ways of addressing this problem, but they are arguably not as nice as the simplicity of a,b trees.

Without further ado, let's dive in.

---
BASICS
---

This is an $(a,b)$-tree.
More specifically, a $(2,4)$-tree, since the parameters $(a,b)$ denote the number of children each node can have (in this case, between 2 and 4).
There is one exception, the root -- while regular nodes can have from $a$ to $b$ children, the root can have from $2$ to $b$, since if $a$ was large, we wouldn't be able to create trees with a small number of keys, which we obviously don't want. <!-- make a list of the axioms to the left -->

To make the terminology concrete, an $(a,b)$-tree has nodes which contain keys, sorted from left to right, and leafs which have no keys. c
A subtree of a node that is between keys $x$ and $y$ contains only keys that are between $x$ and $y$ (inclusive). <!-- again, write this to the right -->

To keep the operations on the tree quick, we additionally require that all leafs are in the same depth. <!-- yet again, write this to the right -->

And, finally, we require that $a \ge 2$ and $b \ge 2a - 1$.
The limit on $a$ is intuitive, since we don't want the tree to have non-leaf nodes with no keys.
The limit on $b$ is a little more cryptic, but will make sense when we start looking into the operations -- it ensures that the operations we make on the nodes make sense.

Speaking of the operations, there are three that we aim to cover in this video:

- searching for a key,
- adding a key and
- removing a key


---
SEARCHING
---

Let's start with the simplest operation, searching.

To search for a key, starting in the root node, find where in the node the key should be (using binary search, since the keys in the nodes are sorted) -- if it's not there, follow the edge between the keys where it should be, eventually either finding it or getting to a leaf, at which point you know it's not there.


---
ADDING
---

Let's now look at adding a key to the tree.

Assuming that the key is not present, we'll run seach and end up in one of the tree's leafs.
Now we can simply add the key to the leaf's parent node.

If this didn't break the condition on the number of children of the node (i.e. if the node has at most $b$ children), we're done.
Otherwise, we split the node in two (down the middle) and move the middle key to the node one level up, again possibly splitting this node and going further up.

This, by the way, is where we're using the mysterious $b \ge 2a - 1$ condition, since splitting the node down the middle makes either side have $\lceil b / 2 \rceil$ nodes, which is therefore at least $a$.


---
REMOVING
---

Removing will be a little trickier.

Let's again assume that the key is present and we run search to find it.

If it's in the second to last layer, we can remove it and one of the leafs next to it.
If it's not, we'll do a similar trick that binary trees do: we'll replace it with with the leftmost child of its right subtree, again reducing the problem to removing a key from the second to last layer.

Similarly to adding, this could have broken the condition on the number of children of a node, having less than $a$ children.

TODO: 


---
IMPLEMENTATION DETAILS
---


---
CACHING, PERFORMANCE
---
