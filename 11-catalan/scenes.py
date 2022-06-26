from utilities import *


class GraphStarsScene(Scene):
    def construct(self):
        trees = VGroup(*BinaryTree.generate_binary_trees(3)).arrange(buff=0.8)

        self.play(AnimationGroup(*[Write(t) for t in trees], lag_ratio=0.1))

        stars_animations = []
        for t in trees:
            StarUtilities.add_stars_to_graph(t)
            stars_animations.append(CreateStars(t))

        self.play(*stars_animations)

        self.wait(1)

        self.play(*SwapChildren(trees[2], ""))

        self.wait(1)

        self.play(ChangeStars(trees[2], 5))
