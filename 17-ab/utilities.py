from manim import *
from typing import *
from copy import deepcopy


BIG_OPACITY = 0.15
FAST_RUNTIME = 0.33


KEYS_IN_NODE_BUFF = 0.3


DARK_COLOR = DARKER_GRAY


def create_node(keys, fill_background=True, half=None, short=False):
    oops = False

    # leaf
    if keys is None:
        keys_vgroup = Dot().set_opacity(0).scale(0.8)

        corner_width = 0.01
        lr_buff=0
        ud_buff=0
    else:
        if len(keys) == 0:
            oops = True
            keys = [0]

        keys_vgroup = VGroup(*[Tex(str(k)) for k in keys]).arrange(buff=KEYS_IN_NODE_BUFF)\
            .set_z_index(2)

        if oops:
            keys_vgroup[0].stretch_to_fit_width(keys_vgroup[0].get_width() / 2)
            keys = []

        corner_width = 0.35
        lr_buff=-0.1
        ud_buff=0.07

    left = Dot().next_to(keys_vgroup, LEFT, buff=lr_buff).get_center()
    right = Dot().next_to(keys_vgroup, RIGHT, buff=lr_buff).get_center()
    down = Dot().next_to(keys_vgroup, DOWN, buff=ud_buff).get_center()
    up = Dot().next_to(keys_vgroup, UP, buff=ud_buff).get_center()

    if half is None:
        points = [down + right,
                  down + right + RIGHT * corner_width,
                  up + right + RIGHT * corner_width,
                  up + right,
                  up + right,
                  up + right,
                  up + left,
                  up + left,
                  up + left,
                  up + left + LEFT * corner_width,
                  down + left + LEFT * corner_width,
                  down + left,
                  down + left,
                  down + left,
                  down + right,
                  down + right]
    elif half is LEFT:
        if short:
            points = [up + left,
                      up + left,
                      up + left,
                      up + left,
                      up + left,
                      up + left + LEFT * corner_width,
                      down + left + LEFT * corner_width,
                      down + left,
                      down + left,
                      down + left,
                      down + left,
                      down + left]
        else:
            points = [up,
                      up,
                      up + left,
                      up + left,
                      up + left,
                      up + left + LEFT * corner_width,
                      down + left + LEFT * corner_width,
                      down + left,
                      down + left,
                      down + left,
                      down,
                      down]
    else:
        if short:
            points = [down + right,
                      down + right,
                      down + right,
                      down + right,
                      down + right,
                      down + right + RIGHT * corner_width,
                      up + right + RIGHT * corner_width,
                      up + right,
                      up + right,
                      up + right,
                      up + right,
                      up + right]
        else:
            points = [down,
                      down,
                      down + right,
                      down + right,
                      down + right,
                      down + right + RIGHT * corner_width,
                      up + right + RIGHT * corner_width,
                      up + right,
                      up + right,
                      up + right,
                      up,
                      up]

    border = VMobject().set_points(points).set_z_index(1)

    if fill_background:
        border.set_opacity(1).set_fill_color(BLACK)

    if half is None:
        if oops:
            keys_vgroup = VGroup()

        return VGroup(keys_vgroup, border)
    else:
        return border


class ABTree(VMobject):
    def __init__(self, layers: List[List[List[int]]], fill_background=True, **kwargs):
        super().__init__(**kwargs)

        leafs_layer = []
        for node in layers[-1]:
            leafs_layer += [None] * (len(node) + 1)

        layers.append(leafs_layer)

        self.layers = layers
        self.layer_mobjects = VGroup()

        self.nodes_to_keys = {}

        self.index_neighbours = {}

        # create node objects
        for layer in layers:
            layer_mobject = VGroup()
            for node in layer:
                node_mobject = create_node(node, fill_background)

                self.nodes_to_keys[node_mobject] = node
                layer_mobject.add(node_mobject)
            self.layer_mobjects.add(layer_mobject)

        self.node_subtree_mobjects = {}

        # arrange nodes nicely
        for i in reversed(range(len(layers))):
            layer = self.layers[i]
            layer_mobject = self.layer_mobjects[i]

            pos_in_layer = 0

            for j in range(len(layer_mobject)):
                node_mobject = layer_mobject[j]
                node_keys = layer[j]

                # leafs are only leafs
                if i == len(layers) - 1:
                    self.node_subtree_mobjects[node_mobject] = node_mobject
                    continue

                next_layer_mobject = self.layer_mobjects[i + 1]

                children_indices = list(range(pos_in_layer, pos_in_layer + len(node_keys) + 1))

                self.index_neighbours[i, j] = [(i + 1, c) for c in children_indices]

                # otherwise, take k+1 values from the next layer to a group
                node_children = VGroup(
                    *[self.node_subtree_mobjects[next_layer_mobject[k]]
                      for k in children_indices]
                )

                leaf_buffer = 0.25
                node_buffer = 0.4

                # arrange them (they're the children of the node)
                node_children.arrange(RIGHT, buff=leaf_buffer if i == len(layers) - 2 else node_buffer)

                node_vgroup = VGroup(node_mobject, node_children).arrange(DOWN, buff=0.4)

                self.node_subtree_mobjects[node_mobject] = node_vgroup

                pos_in_layer += len(node_keys) + 1

        self.reversed_index_neighbours = {}

        for key in self.index_neighbours:
            for value in self.index_neighbours[key]:
                self.reversed_index_neighbours[value] = key

        self.node_edges = {}
        self.edges = VGroup()
        self.nodes = list(self.nodes_to_keys)

        self.leafs = VGroup()
        for leaf in self.layer_mobjects[-1]:
            self.leafs.add(leaf)

        for node in self.nodes:
            if self.nodes_to_keys[node] is None:
                self.node_edges[node] = None
                continue

            edges = self._create_edges(node)
            self.edges.add(edges)
            self.node_subtree_mobjects[node].add(edges)


        self.add(self.layer_mobjects)
        self.add(self.edges)

    def _create_edges(self, node, fill_background=True):
        node_keys = self.nodes_to_keys[node]

        top = VGroup(*[Dot().scale(0.001)
                       for _ in range(len(node_keys) + 1)])\
                .arrange(RIGHT, KEYS_IN_NODE_BUFF)\
                .move_to(node)\
                .align_to(node, DOWN)\

        node_subtree = self.node_subtree_mobjects[node]

        bottom = VGroup(*[Dot().scale(0.001).move_to(node).align_to(node, UP)
                          for node in node_subtree[1]])

        edges = VGroup(*[Line(start=a.get_center(), end=b.get_center())
                         for a, b in zip(top, bottom)])

        self.node_edges[node] = edges

        return edges

    def node_to_index(self, n1: Mobject):
        for i, layer in enumerate(self.layer_mobjects):
            for j, n2 in enumerate(layer):
                if n1 is n2:
                    return (i, j)

    def node_by_index(self, layer: int, position: int):
        return self.layer_mobjects[layer][position]

    def edges_by_node_index(self, layer: int, position: int):
        return self.node_edges[self.node_by_index(layer, position)]

    def subtree_by_index(self, layer: int, position: int):
        return self.node_subtree_mobjects[self.layer_mobjects[layer][position]]

    def is_index_leaf(self, layer: int, position: int):
        return layer == len(self.layers) - 1

    def search_but_like_animate(self, target_int: int, scene, scale=1, speedup=1, no_cleanup=False):
        target = Tex(f"${str(target_int)}$").next_to(self.node_by_index(0, 0), UP).scale(1.2).set_z_index(100)
        thicc = 6

        self.save_state()

        def get_tmp(keys, index):
            n = len(keys) + 1
            tmp = ABTree(
                [
                    [keys + [0]],
                ],
                fill_background=False,
            ).scale(scale)
            tmp.node_by_index(0, 0).move_to(self.node_by_index(*index))

            return tmp

        def get_qs(tmp, keys):
            n = len(keys) + 1
            qs = VGroup(*[Tex("?") for _ in range(n)])\
                    .set_color(GRAY).set_z_index(15).scale(0.9)

            for i in range(n):
                qs[i].move_to(tmp.node_by_index(0, 0)[0][i])

                if i == 0:
                    qs[i].align_to(tmp.node_by_index(0, 0)[0][i], LEFT)

                if i == n - 1:
                    qs[i].align_to(tmp.node_by_index(0, 0)[0][i], RIGHT)

            return qs

        scene.play(
            FadeIn(target, shift=UP * 0.1),
        )

        # same code as search
        current_index = (0, 0)
        current = self.nodes_to_keys[self.node_by_index(*current_index)]

        while True:
            tmp = get_tmp(current, current_index)
            qs = get_qs(tmp, current)
            n = len(current) + 1

            # save original node shape and positions
            self.node_by_index(*current_index)[1].save_state()
            for i in range(n - 1):
                self.node_by_index(*current_index)[0][i].save_state()

            scene.play(
                AnimationGroup(
                    AnimationGroup(
                        Transform(self.node_by_index(*current_index)[1], tmp.node_by_index(0, 0)[1]),
                        *[self.node_by_index(*current_index)[0][i].animate.move_to(VGroup(qs[i], qs[i + 1])) for i in range(n - 1)]
                    ),
                    FadeIn(qs),
                    lag_ratio=0.5,
                ),
                run_time=1/speedup,
            )

            for i, e2 in enumerate(current + [float('inf')]):
                color = BLUE
                if target_int < e2:
                    if current_index[0] == len(self.layers) - 2:
                        color = RED
                    else:
                        color = ORANGE

                scene.play(
                    self.node_by_index(*current_index)[0].animate.set_color(WHITE),
                    target.animate.move_to(qs[i]).align_to(target, DOWN).set_color(WHITE if color is not RED else RED),
                    self.edges_by_node_index(*current_index)[i].animate.set_color(color).set_stroke_width(thicc),
                    self.subtree_by_index(*current_index)[1][i].animate.set_color(color),
                    qs[i].animate.set_color(color),
                    run_time=(1 if i == 0 else 0.66) / speedup
                )

                if target_int < e2:
                    break

                scene.play(
                    target.animate.move_to(self.node_by_index(*current_index)[0][i]).align_to(target, DOWN).set_color(GREEN if target_int == e2 else WHITE),
                    qs.animate.set_color(GRAY),
                    self.node_by_index(*current_index)[0][i].animate.set_color(GREEN if target_int == e2 else BLUE),
                    *[e.animate.set_color(WHITE).set_stroke_width(4) for e in self.edges_by_node_index(*current_index)],
                    self.subtree_by_index(*current_index)[1].animate.set_color(WHITE),
                    run_time=0.66 / speedup,
                )

                if target_int == e2:
                    break

            old_index = current_index

            where_we_ended_up = i

            current_index = self.index_neighbours[current_index][i]
            current = self.nodes_to_keys[self.node_by_index(*current_index)]

            # we're in a leaf!
            if current is None or target_int == e2:
                if no_cleanup:
                    return target, qs

                scene.play(
                    AnimationGroup(
                        AnimationGroup(
                            FadeOut(qs),
                            FadeOut(target),
                        ),
                        self.animate.restore(),
                        lag_ratio=0.5,
                    )
                )

                return

            bezier = CubicBezier(
                target.get_center(),
                Dot().move_to(self.node_by_index(*current_index)).align_to(target, DOWN).get_center(),
                Dot().move_to(self.node_by_index(*current_index)).align_to(target, DOWN).get_center(),
                target.copy().next_to(self.node_by_index(*current_index), UP).get_center(),
            )

            tmp2 = get_tmp(current, current_index)
            qs2 = get_qs(tmp2, current)
            new_n = len(current) + 1

            scene.play(
                MoveAlongPath(target, bezier),
                self.node_by_index(*old_index)[1].animate.restore().set_stroke_color(DARKER_GRAY),
                *[self.node_by_index(*old_index)[0][i].animate.restore().set_color(DARKER_GRAY) for i in range(n - 1)],

                *[self.subtree_by_index(*n).animate.set_color(DARKER_GRAY)
                  for i, n in zip(range(n), self.index_neighbours[old_index])
                  if i != where_we_ended_up],

                *[self.subtree_by_index(*n).animate.set_color(WHITE)
                  for i, n in zip(range(n), self.index_neighbours[old_index])
                  if i == where_we_ended_up],

                *[e.animate.set_color(DARKER_GRAY).set_stroke_width(4)
                  for e in self.edges_by_node_index(*old_index)],

                FadeOut(qs),

                run_time=1/speedup,
            )

        return current_index

    def search(self, e1) -> Tuple[Tuple[int, int], int]:
        """Return the position of where an element is/should be in the tree."""
        current_index = (0, 0)
        current = self.nodes_to_keys[self.node_by_index(*current_index)]

        while current is not None:
            for i, e2 in enumerate(current + [float('inf')]):
                if e1 <= e2:
                    break

            if e1 == e2:
                return current_index

            current_index = self.index_neighbours[current_index][i]
            current = self.nodes_to_keys[self.node_by_index(*current_index)]

        return current_index

    def bubble_delete(self, a, scale=1, pause_between_shift=False, tree_transform_function=None):
        if isinstance(a, int):
            target = None

            for i, layer in enumerate(self.layers[:-1]):
                for j, node in enumerate(layer):
                    if len(node) == a - 2:
                        target = (i, j)

            if target is None:
                return
        else:
            target = a

        i, j = target

        to_merge_index = (i, j)
        to_merge_parent_index = self.reversed_index_neighbours[to_merge_index]

        for index, child in enumerate(self.index_neighbours[to_merge_parent_index]):
            if child == to_merge_index:
                break

        new_layers = deepcopy(self.layers)[:-1]
        from_top = new_layers[to_merge_parent_index[0]][to_merge_parent_index[1]].pop(index)
        from_l = new_layers[to_merge_index[0]].pop(to_merge_index[1] + 1)

        new_layers[to_merge_index[0]][to_merge_index[1]] += [from_top]
        new_layers[to_merge_index[0]][to_merge_index[1]] += from_l

        new_ab_tree = ABTree(new_layers, fill_background=False).scale(scale).move_to(self).align_to(self, UP)

        if tree_transform_function:
            tree_transform_function(new_ab_tree)

        # that's right, I'm cheating and you can't stop me
        a, t = new_ab_tree.bubble_insert(to_merge_index, scale=scale, pause_between_shift=pause_between_shift, tree_transform_function=tree_transform_function)

        return AnimationGroup(a, rate_func = lambda x: 1 - x), new_ab_tree

    def bubble_insert(self, b, scale=1, pause_between_shift=False, tree_transform_function=None):
        """Return an animation that bubbles a full node up after insertion (or null if the tree is fine)."""
        if isinstance(b, int):
            target = None

            for i, layer in enumerate(self.layers[:-1]):
                for j, node in enumerate(layer):
                    if len(node) == b:
                        target = (i, j)

            if target is None:
                return
        else:
            target = b

        i, j = target

        to_split_index = (i, j)
        to_split = self.layers[i][j]

        aaa = create_node(self.layers[i][j], half=LEFT).scale(scale).set_stroke_color(self.node_by_index(*to_split_index)[0].get_color())
        bbb = create_node(self.layers[i][j], half=RIGHT).scale(scale).set_stroke_color(self.node_by_index(*to_split_index)[0].get_color())
        VGroup(aaa, bbb).arrange(buff=0).move_to(self.node_by_index(*to_split_index))

        to_split_a = to_split_index
        to_split_b = (i, j + 1)

        mid_index = len(to_split) // 2 - 1
        a, mid, b = to_split[:mid_index], to_split[mid_index], to_split[mid_index + 1:]

        a_length = len(a)
        b_length = len(b)

        new_layers = deepcopy(self.layers)[:-1]  # remove leafs

        new_layers[i].pop(j)
        new_layers[i].insert(j, b)
        new_layers[i].insert(j, a)

        # splitting root
        if i == 0:
            new_layers.insert(0, [[mid]])

            new_ab_tree = ABTree(new_layers, fill_background=False).scale(scale).align_to(self, DOWN)

            if tree_transform_function:
                tree_transform_function(new_ab_tree)

            to_split_a = (i + 1, j)
            to_split_b = (i + 1, j + 1)

            aaa_short = create_node(new_ab_tree.layers[i + 1][j], half=LEFT).scale(scale)
            bbb_short = create_node(new_ab_tree.layers[i + 1][j + 1], half=RIGHT).scale(scale)

            aaa_short.move_to(new_ab_tree.node_by_index(*to_split_a)).align_to(new_ab_tree.node_by_index(*to_split_a)[1], LEFT).set_opacity(1)
            bbb_short.move_to(new_ab_tree.node_by_index(*to_split_b)).align_to(new_ab_tree.node_by_index(*to_split_b)[1], RIGHT).set_opacity(1)

            return AnimationGroup(
                AnimationGroup(
                    # lord forgive me
                FadeOut(self.node_by_index(*to_split_index)[1], run_time=0.001),

                # split borders
                Transform(aaa, aaa_short),
                Transform(bbb, bbb_short),

                Transform(self.node_by_index(*to_split_index)[0][:mid_index],
                            new_ab_tree.node_by_index(*to_split_a)[0]),

                Transform(self.node_by_index(*to_split_index)[0][mid_index + 1:],
                            new_ab_tree.node_by_index(*to_split_b)[0]),

                Transform(self.node_by_index(*to_split_index)[0][mid_index],
                            new_ab_tree.node_by_index(0, 0)[0][0]),

                # to split subtrees
                *[Transform(self.subtree_by_index(*to_split_index)[1][k],
                            new_ab_tree.subtree_by_index(*to_split_a)[1][k])
                  for k in range(a_length + 1)],
                *[Transform(self.subtree_by_index(*to_split_index)[1][k + a_length + 1],
                            new_ab_tree.subtree_by_index(*to_split_b)[1][k])
                  for k in range(b_length + 1)],
                *[Transform(self.edges_by_node_index(*to_split_index)[k],
                            new_ab_tree.edges_by_node_index(*to_split_a)[k])
                  for k in range(a_length + 1)],
                *[Transform(self.edges_by_node_index(*to_split_index)[k + a_length + 1],
                            new_ab_tree.edges_by_node_index(*to_split_b)[k])
                  for k in range(b_length + 1)],
                ),
                AnimationGroup(
                    Wait(1),
                    AnimationGroup(
                        FadeIn(new_ab_tree.node_by_index(0, 0)[1]),
                        FadeIn(new_ab_tree.edges_by_node_index(0, 0)),
                        FadeIn(new_ab_tree.node_by_index(*to_split_a)[1]),
                        FadeIn(new_ab_tree.node_by_index(*to_split_b)[1]),
                        run_time=0.75,
                    ),
                    lag_ratio=0.6,
                ),
            ), new_ab_tree
        else:
            parent = self.reversed_index_neighbours[to_split_index]
            ip, jp = parent

            new_layers[ip][jp].append(mid)
            new_layers[ip][jp].sort()

            mid_parent_index = new_layers[ip][jp].index(mid)

            new_ab_tree = ABTree(new_layers, fill_background=False).scale(scale).move_to(self).align_to(self, DOWN)

            if tree_transform_function:
                tree_transform_function(new_ab_tree)

            aaa_short = create_node(new_ab_tree.layers[i][j], half=LEFT).scale(scale)
            bbb_short = create_node(new_ab_tree.layers[i][j + 1], half=RIGHT).scale(scale)

            aaa_short.move_to(new_ab_tree.node_by_index(*to_split_a)).align_to(new_ab_tree.node_by_index(*to_split_a)[1], LEFT).set_opacity(1)
            bbb_short.move_to(new_ab_tree.node_by_index(*to_split_b)).align_to(new_ab_tree.node_by_index(*to_split_b)[1], RIGHT).set_opacity(1)

            if not pause_between_shift:
                a = Transform(self.node_by_index(*to_split_index)[0][mid_index],
                            new_ab_tree.node_by_index(*parent)[0][mid_parent_index])
            else:
                a = Succession(Wait(1.25), Transform(self.node_by_index(*to_split_index)[0][mid_index],
                            new_ab_tree.node_by_index(*parent)[0][mid_parent_index]))

            return AnimationGroup(
                AnimationGroup(
                # resize parent
                Transform(self.node_by_index(*parent)[1],
                          new_ab_tree.node_by_index(*parent)[1]),

                    # lord forgive me
                FadeOut(self.node_by_index(*to_split_index)[1], run_time=0.001),

                # split borders
                Transform(aaa, aaa_short),
                Transform(bbb, bbb_short),

                # other parent subtrees + edges
                *[Transform(self.subtree_by_index(*parent)[1][k],
                            new_ab_tree.subtree_by_index(*parent)[1][k])
                  for k in range(0, mid_parent_index)],
                *[Transform(self.edges_by_node_index(*parent)[k],
                            new_ab_tree.edges_by_node_index(*parent)[k])
                  for k in range(0, mid_parent_index)],
                *[Transform(self.subtree_by_index(*parent)[1][k],
                            new_ab_tree.subtree_by_index(*parent)[1][k + 1])
                  for k in range(mid_parent_index + 1, len(self.subtree_by_index(*parent)[1]))],
                *[Transform(self.edges_by_node_index(*parent)[k],
                            new_ab_tree.edges_by_node_index(*parent)[k + 1])
                  for k in range(mid_parent_index, len(self.edges_by_node_index(*parent)))],
                Transform(self.edges_by_node_index(*parent)[mid_parent_index].copy(),
                            new_ab_tree.edges_by_node_index(*parent)[mid_parent_index]),

                # move number up
                a,

                Transform(self.node_by_index(*to_split_index)[0][:mid_index],
                            new_ab_tree.node_by_index(*to_split_a)[0]),

                Transform(self.node_by_index(*to_split_index)[0][mid_index + 1:],
                            new_ab_tree.node_by_index(*to_split_b)[0]),

                # move numbers in parent
                *[Transform(self.node_by_index(*parent)[0][k],
                            new_ab_tree.node_by_index(*parent)[0][k])
                  for k in range(0, mid_parent_index)],
                *[Transform(self.node_by_index(*parent)[0][k],
                            new_ab_tree.node_by_index(*parent)[0][k + 1])
                  for k in range(mid_parent_index, len(self.node_by_index(*parent)[0]))],

                # to split subtrees
                *[Transform(self.subtree_by_index(*to_split_index)[1][k],
                            new_ab_tree.subtree_by_index(*to_split_a)[1][k])
                  for k in range(a_length + 1)],
                *[Transform(self.subtree_by_index(*to_split_index)[1][k + a_length + 1],
                            new_ab_tree.subtree_by_index(*to_split_b)[1][k])
                  for k in range(b_length + 1)],
                *[Transform(self.edges_by_node_index(*to_split_index)[k],
                            new_ab_tree.edges_by_node_index(*to_split_a)[k])
                  for k in range(a_length + 1)],
                *[Transform(self.edges_by_node_index(*to_split_index)[k + a_length + 1],
                            new_ab_tree.edges_by_node_index(*to_split_b)[k])
                  for k in range(b_length + 1)],
                ),
                AnimationGroup(
                    Wait(1),
                    AnimationGroup(
                        FadeIn(new_ab_tree.node_by_index(*to_split_a)[1]),
                        FadeIn(new_ab_tree.node_by_index(*to_split_b)[1]),
                        run_time=0.75,
                    ),
                    lag_ratio=0.6,
                ),
            ), new_ab_tree

    def delete(self, element, scale=1, tree_transform_function=None):
        orig_element = element

        if isinstance(element, int):
            where_to_delete = self.search(element)
        else:
            where_to_delete, element = element

        new_layers = deepcopy(self.layers)[:-1]
        new_layers[where_to_delete[0]][where_to_delete[1]].remove(element)

        new_ab_tree = ABTree(new_layers, fill_background=False).scale(scale).move_to(self).align_to(self, UP)

        if tree_transform_function is not None:
            tree_transform_function(new_ab_tree)

        tree_to_return = new_ab_tree.copy()

        # that's right, I'm cheating and you can't stop me
        a, _ = new_ab_tree.insert(orig_element, scale=scale, tree_transform_function=lambda x: x.become(self.copy()))

        return AnimationGroup(a, rate_func = lambda x: 1 - x), tree_to_return


    def insert(self, element, scale=1, transform_instead=None, tree_transform_function=None):
        """A function that animates inserting an element into the tree. DOESN'T BALANCE, use balance_insert for this!"""
        if isinstance(element, int):
            where_to_put = self.reversed_index_neighbours[self.search(element)]
        else:
            where_to_put, element = element

        new_layers = deepcopy(self.layers)[:-1]  # remove leafs
        new_layers[where_to_put[0]][where_to_put[1]].append(element)
        new_layers[where_to_put[0]][where_to_put[1]].sort()

        index = new_layers[where_to_put[0]][where_to_put[1]].index(element)
        index_in_layer = 0
        for j, node in enumerate(self.layers[-2]):
            if j == where_to_put[1]:
                break

            index_in_layer += len(self.layers[-2][j]) + 1

        index_in_layer_start = index_in_layer
        index_in_layer_end = index_in_layer + len(self.layers[-2][j]) + 1
        index_in_layer += index

        new_ab_tree = ABTree(new_layers, fill_background=False).scale(scale).move_to(self).align_to(self, UP)

        if tree_transform_function is not None:
            tree_transform_function(new_ab_tree)

        tree_indices = []

        for i, layer in enumerate(self.layer_mobjects):
            for j, n2 in enumerate(layer):
                tree_indices.append((i, j))

        leaf_index = len(self.layers)

        if transform_instead is not None:
            a = Transform(transform_instead, new_ab_tree.node_by_index(*where_to_put)[0][index])
        else:
            a = FadeIn(new_ab_tree.node_by_index(*where_to_put)[0][index])

        return AnimationGroup(
            AnimationGroup(
                # non-leafs
                *[Transform(self.node_by_index(i, j),
                            new_ab_tree.node_by_index(i, j))
                  for (i, j) in tree_indices
                  if not self.is_index_leaf(i, j) and (i, j) != where_to_put],
                *[Transform(self.edges_by_node_index(i, j),
                            new_ab_tree.edges_by_node_index(i, j))
                  for (i, j) in tree_indices
                  if not self.is_index_leaf(i, j) and (i, j) != where_to_put],
                *[Transform(self.node_by_index(i, j),
                            new_ab_tree.node_by_index(i, j))
                  for (i, j) in tree_indices
                  if not self.is_index_leaf(i, j) and (i, j) != where_to_put],

                # leafs
                Transform(self.node_by_index(*where_to_put)[1],
                          new_ab_tree.node_by_index(*where_to_put)[1]),
                *[Transform(self.subtree_by_index(i, j),
                            new_ab_tree.subtree_by_index(i, j))
                  for (i, j) in tree_indices
                  if (i == len(self.layers) - 2) and (i, j) != where_to_put],

                *[Transform(self.node_by_index(*where_to_put)[0][k],
                            new_ab_tree.node_by_index(*where_to_put)[0][k])
                  for k in range(0, index)],
                *[Transform(self.node_by_index(*where_to_put)[0][k],
                            new_ab_tree.node_by_index(*where_to_put)[0][k + 1])
                  for k in range(index, len(self.node_by_index(*where_to_put)[0]))],

                *[Transform(self.edges_by_node_index(*where_to_put)[k],
                            new_ab_tree.edges_by_node_index(*where_to_put)[k])
                  for k in range(0, index + 1)],
                *[Transform(self.edges_by_node_index(*where_to_put)[k],
                            new_ab_tree.edges_by_node_index(*where_to_put)[k + 1])
                  for k in range(index + 1, len(self.edges_by_node_index(*where_to_put)))],

                *[Transform(self.node_by_index(leaf_index - 1, k),
                            new_ab_tree.node_by_index(leaf_index - 1, k))
                  for k in range(index_in_layer_start, index_in_layer + 1)],
                *[Transform(self.node_by_index(leaf_index - 1, k),
                            new_ab_tree.node_by_index(leaf_index - 1, k + 1))
                  for k in range(index_in_layer + 1, index_in_layer_end)],
            ),
            AnimationGroup(
                a,
                FadeIn(new_ab_tree.edges_by_node_index(*where_to_put)[index + 1]),
                FadeIn(new_ab_tree.subtree_by_index(*where_to_put)[1][index + 1]),
            ),
            lag_ratio=0.5,
        ), new_ab_tree


def get_fade_rect(*args, opacity=1 - BIG_OPACITY, z_index=100):
    if len(args) == 0:
        return Square(fill_opacity=opacity, color=BLACK).scale(1000).set_z_index(z_index)
    else:
        return SurroundingRectangle(VGroup(*args), fill_opacity=opacity, color=BLACK).set_z_index(z_index)


def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)

        if config.quality and not config.quality.startswith("medium"):
            self.play(*map(FadeOut, self.mobjects))

    return inner


def get_tree_bubbles(tree):
    def get_bubble(symbol):
        dot = Dot().scale(2)
        symbol = Tex(f"${symbol}$", color=BLACK).scale(0.5).set_z_index(1).move_to(dot)

        return VGroup(dot, symbol)

    bubbles = VGroup()
    node_bubbles = {}

    for layer in range(len(tree.layers)):
        for position in range(len(tree.layers[layer])):
            node = tree.node_by_index(layer, position)
            edges = tree.node_edges[node]

            if edges is None:
                continue

            node_bubbles[node] = VGroup()

            for e in edges:
                node_bubbles[node].add(
                    get_bubble("<").move_to(e).scale(0.8 - layer * 0.2).set_z_index(2)
                )

            bubbles.add(node_bubbles[node])

    return bubbles, node_bubbles


class MoveAndFade(Animation):
    """Make one mobject move along the path of another mobject.
    """

    def __init__(
        self,
        mobject: Mobject,
        path: VMobject,
        suspend_mobject_updating: bool | None = False,
        **kwargs,
    ) -> None:
        self.path = path
        self.original = mobject.copy()
        super().__init__(
            mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.point_from_proportion(self.rate_func(alpha))
        self.mobject.become(self.original.copy().move_to(point).set_opacity(1 - alpha * 1.2))


def align_object_by_coords(obj, current, desired, animation=False):
    """Align an object such that it's current coordinate coordinate will be the desired."""
    if isinstance(current, Mobject):
        current = current.get_center()

    if isinstance(desired, Mobject):
        desired = desired.get_center()

    if animation:
        return obj.animate.shift(desired - current)
    else:
        obj.shift(desired - current)


def CreateHighlight(obj):
    return SurroundingRectangle(
        obj,
        color=YELLOW,
        fill_opacity=0.15
    ).set_z_index(1)
