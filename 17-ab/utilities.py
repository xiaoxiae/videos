from manim import *
from typing import *


BIG_OPACITY = 0.2
FAST_RUNTIME = 0.33


KEYS_IN_NODE_BUFF = 0.3


def _create_node(keys):
    # leaf
    if keys is None:
        keys_vgroup = Dot().set_opacity(0)

        corner_width = 0.0
        lr_buff=0
        ud_buff=0
    else:
        keys_vgroup = VGroup(*[Tex(str(k)) for k in keys]).arrange(buff=KEYS_IN_NODE_BUFF)

        corner_width = 0.35
        lr_buff=-0.1
        ud_buff=0.07

    left = Dot().next_to(keys_vgroup, LEFT, buff=lr_buff).get_center()
    right = Dot().next_to(keys_vgroup, RIGHT, buff=lr_buff).get_center()
    down = Dot().next_to(keys_vgroup, DOWN, buff=ud_buff).get_center()
    up = Dot().next_to(keys_vgroup, UP, buff=ud_buff).get_center()

    border = VMobject().set_points([down + right,
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
                                    down + right]).set_z_index(1)

    return VGroup(keys_vgroup, border)


class ABTree(VMobject):

    def _create_edges(self, node):
        node_keys = self.nodes_to_keys[node]

        top = VGroup(*[Dot().scale(0.001)
                       for _ in range(len(node_keys) + 1)])\
                .arrange(RIGHT, KEYS_IN_NODE_BUFF)\
                .move_to(node)\
                .align_to(node, DOWN)

        node_subtree = self.node_subtree_mobjects[node]

        bottom = VGroup(*[Dot().scale(0.001).move_to(node).align_to(node, UP)
                          for node in node_subtree[1]])

        edges = VGroup(*[Line(start=a.get_center(), end=b.get_center())
                         for a, b in zip(top, bottom)])

        self.node_edges[node] = edges

        return edges

    def node_by_index(self, layer: int, position: int):
        return self.layer_mobjects[layer][position]

    def subtree_by_index(self, layer: int, position: int):
        return self.node_subtree_mobjects[self.layer_mobjects[layer][position]]

    def __init__(self, a, b, layers: List[List[List[int]]], **kwargs):
        super().__init__(**kwargs)

        leafs_layer = []
        for node in layers[-1]:
            leafs_layer += [None] * (len(node) + 1)

        layers.append(leafs_layer)

        self.a = a
        self.b = b

        self.layers = layers
        self.layer_mobjects = VGroup()

        self.nodes_to_keys = {}

        # create node objects
        for layer in layers:
            layer_mobject = VGroup()
            for node in layer:
                node_mobject = _create_node(node)

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

                # otherwise, take k+1 values from the next layer to a group
                node_children = VGroup(
                    *[self.node_subtree_mobjects[next_layer_mobject[k]]
                      for k in range(pos_in_layer, pos_in_layer + len(node_keys) + 1)]
                )

                leaf_buffer = 0.25
                node_buffer = 0.4

                # arrange them (they're the children of the node)
                node_children.arrange(RIGHT, buff=leaf_buffer if i == len(layers) - 2 else node_buffer)

                node_vgroup = VGroup(node_mobject, node_children).arrange(DOWN, buff=0.4)

                self.node_subtree_mobjects[node_mobject] = node_vgroup


                pos_in_layer += len(node_keys) + 1

        self.node_edges = {}
        self.edges = VGroup()

        self.node_mobjects = list(self.nodes_to_keys)

        for node in self.node_mobjects:
            if self.nodes_to_keys[node] is None:
                self.node_edges[node] = None
                continue

            edges = self._create_edges(node)
            self.edges.add(edges)
            self.node_subtree_mobjects[node].add(edges)


        self.add(self.layer_mobjects)
        self.add(self.edges)
