from manim import *
from typing import *


BIG_OPACITY = 0.2
FAST_RUNTIME = 0.33

class ABTree(VMobject):
    def _create_node(keys):
        # leaf
        if keys is None:
            keys_vgroup = Dot().set_opacity(0)

            corner_width = 0.0
            lr_buff=0
            ud_buff=0
        else:
            keys_vgroup = VGroup(*[Tex(str(k)) for k in keys]).arrange(buff=0.3)

            corner_width = 0.35
            lr_buff=0
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
                                        down + right])

        return VGroup(keys_vgroup, border)

    def __init__(self, a, b, layers: List[List[List[int]]], **kwargs):
        super().__init__(**kwargs)

        self.a = a
        self.b = b

        self.layers = layers
        self.layer_mobjects = VGroup()

        for layer in layers:
            layer_mobject = VGroup()
            for node in layer:
                layer_mobject.add(ABTree._create_node(node))
            layer_mobject.arrange(buff=0.5)
            self.layer_mobjects.add(layer_mobject)

        self.layer_mobjects.arrange(DOWN, buff=0)

        self.add(self.layer_mobjects)
