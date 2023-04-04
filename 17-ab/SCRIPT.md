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
Has this ever happened to you?

You're balancing your AVL tree, making sure it's nice and neat and suddenly: oh no, you made the wrong rotation!
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
As you can see, they are no longer binary, since their nodes can have more than two children.

Just like binary trees, they are used for quickly storing and locating items based on their keys.
If we want to find a key (for example 5) in a binary tree, we start in the root and go right if the target is larger than the current node, else we go left.
In this case, the key is found.
However, if we tried the same with a key that isn't in the tree, we soon reach a leaf, at which point we know the key is not present.

For an $(a,b)$-tree, this procedure is very similar, the only difference being that either the key is in the current node, or it's not and we follow the edge where it should be, again either finding it or getting to a leaf.

$(a,b)$-trees address a number of shortcomings of binary trees, mainly the fact that they can easily become unbalanced -- repeatedly inserting items into a binary tree without other operations can make them lean to one side, rendering all operations significantly slower.
There are ways to address this problem (like AVL trees or R&B trees), but they are not nearly as elegant as $(a,b)$-trees.

So, without further ado, let's dive in.


---
BASICS
---

\marginpar{\texttt{Basics}}

This is $(a,b)$-tree.
Whoops, wrong emphasis... this is $(a,b)$-tree.

It is made up of nodes, which contain keys that are always sorted from left to right.
The only exception are the leafs, which don't contain any keys.

Each key separates two subtrees, the left one containing keys that are smaller and the right one containing keys that are larger.

Each node has a number of children, which are determined by the parameters $a$ and $b$ -- $a$ is the minimum number of children a node can have and $b$ is the maximum.
This is therefore a $(2,4)$-tree, since each node has between $2$ and $4$ children.
There are, however, two exceptions: first, the leafs have no children, because we don't want an infinite tree.
The second is the root -- while other nodes can have between $a$ and $b$ children, the root can have between $2$ and $b$, otherwise building trees with certain numbers of keys wouldn't be possible.

To keep the operations on the tree fast, there are some things it must satisfy at all times.

Firstly, all leafs must be on the same layer.
This forces the tree to have logarithmic depth and proving it is a nice exercise, feel free to pause here and try.

Secondly, $a \ge 2$ and $b \ge 2a - 1$.
The limit on $a$ is intuitive, since a node with only one child would have no keys, which doesn't make sense.
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

To search for a key, we start in the root and do the following: first, find where in the current node the key should be.
If it's not there, go to the subtree where it should be and repeat the process.

In this case, the key has been found.

Let's now see what happens when we search for a key that isn't in the tree.
As you see, we end up in a leaf with nowhere else to go, so we know with absolute certainty that the key is not present.


---
INSERTION
---

\marginpar{\texttt{Insertion}}

Since just searching for keys is boring, let's try to insert one.

Assuming that it's not present, we'll again run search and end up in one of the tree's leafs.
Then we simply insert the key into the leaf's parent node, creating a new leaf in the process.

Now it might seem like we're be done, but remember that a node can have at most $b$ children, which this node now doesn't satisfy.

Pause here and try to solve this problem; chances are the first thing you think of is the correct solution.

That's right, the answer is violence!
We split the node down the middle, moving one key up to accommodate for the newly created node.
This adds a key to the node above, which might in turn brake its condition, so we have to repeat the process until there are no more broken nodes.

Let's insert a few more values to better illustrate what the operation does to the tree.

While all this seems sensible, what we've done here is only possible thanks to our carefully selected conditions:
Firstly, splitting a node makes the two resulting nodes have at least $\lfloor (b+1)/2 \rfloor$ children, which, thanks to our inequality on $b$, is at least $a$, making them valid.
Secondly, the root can have from $2$ to $b$ children (instead of $a$ to $b$), having $2$ right after it is split, as you can see here.


---
DELETION
---

Adding this many keys to the tree is making it a little crowded, so let's in delete some keys.
Let's assume that the key we want to delete is present and we run search to find it.

If it's in the second to last layer, we can simply delete it, along with one of its leafs.

If it's not in the second to last layer, we'll remove it but since this leaves and empty spot, we'd like to replace it with a key from the second to last layer to reduce the problem to the previous case.
Pause here and think about which key we can put in its place.

The answer is actually twofold -- it's both the closets smaller and the closest larger key, since moving either of them to the missing spot would preserve the tree's ordering.

Let's assume that we want the closest larger key.
To find it in the tree, we know that since it's larger than our missing key, it's in its right subtree.
We also know that it's the smallest key in this subtree, so it's the leftmost one.
Replacing the missing key neatly reduces our problem to the previous case and is a well-known trick for removing things from search trees.

Now we can simply remove the leftover leaf and... yikes, that doesn't look healthy.

It seems that removing this key broke the condition on the number of children, with node having less than $a$, so let's fix it.
Since the problem node has at least one adjacent node, we can do one of two things:

a) either merge the two nodes or,
b) steal one of the adjacent node's keys

If the adjacent node has $a$ children (like in this case), we can't just steal a key since it would bring the adjacent node below the limit, so we'll have to merge, which looks as follows.
Notice that this moves a key from the node above, which might again break its condition (similar to insert), so we might have to recursively fix the same problem in the nodes above.

To see the other case in action, let's remove another key.
As we see, its adjacent node has more than $a$ children, meaning that we can steal the closest neighbouring key.
We do so by moving the closest key up and the key above down, which again perserves the ordering of the tree.

One thing to note is that in cases where both operations are possible (i.e. you have two neighbours and can steal from one and merge with the other), you should always steal, which is generally bad life advice but in this case saves you from possibly having to fix the parent node.


---
SELECTING A, B
---

And there you have it, we've covered the common operations of the $(a,b)$-tree.

Now that we know how they work, one question still remains -- what should we set $a$ and $b$ to?
While it doesn't really matter in terms of theoretical analysis since all of the operations will be logarithmic, it very much does matter in practice.

Code runs on real hardware and the main way to make it fast is to make it cache-friendly -- ideally, a node should fit into a single cache line, regardless of its size.

For example, my cache lines are $64B$, which means that they can hold at most $8$ $64b$ values.
A node consists of keys and pointers to its children, each of which is a $64b$ number, meaning that the maximum $b$ value is $4$, making $a$ at most $2$.

To test this, I used an open-source $(a,b)$-tree implementation (link in the description) to run benchmarks on all of the common operations for varying sizes of $a$ and $b$.
Plotting the runtimes, I got a result that I didn't really expect -- it seems that the optimal value for $a,b$ is different for each of the operations and is definitely not $2,4$.

This is because the cache lines computation is an simplification of how a modern CPU behaves and there could be number a of reasons for this result.
Firstly, the library stores keys and values in separate arrays, which theoretically increases the optimal $a,b$ values by a factor of two.
Secondly, the behavior largely depends on the way the structure is used, which in my case consisted of $n$ insertions, $n$ searches and finally $n$ deletions for $n = 1\ 000\ 000$ and might not be representative of other uses.

There is much more to this and if you're interested, I linked a paper that covers this in great detail in the description, but the main point that you should take away is that while theory is good, real world is a mess that no amount of computations can spare you from.


---
OUTRO
---

And that's it.
Thanks for watching!

