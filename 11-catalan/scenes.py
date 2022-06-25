from utilities import *


class GraphStarsScene(Scene):
    def construct(self):
        trees = VGroup(*generate_binary_trees(3)).arrange(buff=0.8)

        self.play(AnimationGroup(*[Write(t) for t in trees], lag_ratio=0.1))

        stars_anim = []
        for t in trees:
            stars_anim.append(AnimationGroup(*AnimateStars(t, add_stars(t)), lag_ratio=0.1))

        self.play(*stars_anim)

        self.wait(1)

        self.play(*SwapChildren(trees[2], ""))

        self.wait(1)
