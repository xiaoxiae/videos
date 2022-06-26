from utilities import *


class StarsExample(Scene):
    def construct(self):
        trees = VGroup(*BinaryTree.generate_binary_trees(3)).arrange(buff=0.8)

        self.play(AnimationGroup(*[Write(t) for t in trees], lag_ratio=0.1))

        stars_animations = []
        for t in trees:
            StarUtilities.add_stars_to_graph(t)
            stars_animations.append(CreateStars(t))

        self.play(*stars_animations)

        #self.play(ChangeStars(trees[2], 5))

        self.play(*[FadeOut(t) for t in trees])


class BuildStarsExample(Scene):
    def construct(self):
        tree = BinaryTree.generate_binary_trees(7)[72]

        self.play(Write(tree))

        StarUtilities.add_stars_to_graph(tree)

        self.play(CreateStars(tree))

        for i in range(6):
            self.play(*SwapChildren(tree, tree.get_parent(StarUtilities.get_highest_star(tree)), move_height=0))
            self.play(*SwapChildren(tree, tree.get_parent(StarUtilities.get_highest_star(tree)), move_height=0))
            self.play(*RemoveHighestStar(tree))


class DyckPathExample(Scene):
    def construct(self):
        path = DyckPath([1, 1, 1, -1,-1, -1, 1, -1, 1, 1, -1, -1], labels=True)

        self.play(Write(path))


class TriangulatedPolygonExample(Scene):
    def construct(self):
        p = VGroup(*LinedPolygon.generate_triangulated_polygons(7)).arrange_in_grid(rows=5).scale(0.5)

        self.play(Write(p))
