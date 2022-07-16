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


class BuildStarsExample(MovingCameraScene):
    def construct(self):
        tree = BinaryTree.generate_binary_trees(7)[72]

        StarUtilities.add_stars_to_graph(tree)

        self.camera.frame.move_to(tree).set_height(tree.height * 1.5)

        self.play(
            AnimationGroup(
                Write(tree),
                lag_ratio=0.5,
            )
        )

        for i in range(6):
            new_tree = tree.copy()

            v = tree.get_parent(StarUtilities.get_highest_star(tree))

            self.play(*SwapChildren(tree, v))
            self.play(*SwapChildren(tree, v))

            self.play(*RemoveHighestStar(new_tree), run_time=0)
            self.play(FadeIn(new_tree), run_time=0)
            self.play(FadeOut(new_tree), run_time=0)

            self.play(
                *RemoveHighestStar(tree),
                self.camera.frame.animate.move_to(new_tree).set_height(max(new_tree.height * 1.6, 3)),
            )

        v = tree.get_parent(StarUtilities.get_highest_star(tree))
        self.play(*SwapChildren(tree, v))
        self.play(*SwapChildren(tree, v))


class DyckPathExamplesNew(MovingCameraScene):
    def construct(self):
        self.next_section()

        dyck_paths = Tex(r"Dyck Paths").scale(2)

        self.play(Write(dyck_paths))

        good_paths = VGroup(
            DyckPath([1, -1, 1, 1, -1, 1, -1, -1]),
            DyckPath([1, 1, 1, -1, -1, -1, 1, -1]),
        ).arrange(buff=1.5).shift(DOWN)

        good_paths[0].align_to(good_paths[1], DOWN)

        self.play(
            AnimationGroup(
                dyck_paths.animate.shift(UP * 1.25),
                AnimationGroup(*[Write(p) for p in good_paths], lag_ratio=0.3),
                lag_ratio=0.5,
            )
        )

        #self.play(
        #    good_paths.animate.arrange(DOWN, buff=0.54).move_to(LEFT * 3 + DOWN * 0.7),
        #    dyck_paths.animate.move_to(LEFT * 3 + UP * 1.5),
        #    run_time=1.25
        #)

        return

        bad_paths = VGroup(
            DyckPath([-1, 1, 1, -1, 1, -1]),
            DyckPath(list(reversed([-1, -1, 1, 1, 1, -1, -1]))),
            DyckPath([1, 1, -1, 1]),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3 + UP * 0.7)

        self.play(AnimationGroup(*[Write(p) for p in bad_paths], lag_ratio=0.1))

        cross = Tex(r"$\times$").next_to(bad_paths, DOWN, buff=0.7).scale(2).set_color(RED)

        self.play(FadeIn(cross, shift=DOWN * 0.2))

        self.next_section()

        featured_path = good_paths[0]

        # transition
        self.play(
            self.camera.frame.animate.move_to(featured_path).set_width(featured_path.width * 1.5),
            FadeOut(good_paths[1]),
            FadeOut(good_paths[2]),
            FadeOut(bad_paths),
            FadeOut(cross),
            FadeOut(dyck_paths),
        )

        self.play(
            AnimationGroup(
            *list(map(lambda x: AnimationGroup(*x), zip(
                [featured_path.path.edges[(u, v)].animate.set_color(GREEN if featured_path.deltas[u] == 1 else RED)
                  for (u, v) in featured_path.path.edges],
                [Flash(
                    featured_path.path.edges[(u, v)],
                    line_width=0.04, flash_radius=0.05, line_stroke_width=1, line_length=0.04,
                    color=(GREEN if featured_path.deltas[u] == 1 else RED)
                    )
                  for (u, v) in featured_path.path.edges],
                ))),
            lag_ratio=0.05,
            )
        )


class DyckPathExamples(MovingCameraScene):
    def construct(self):
        self.next_section()

        good_paths = VGroup(
            DyckPath([1, -1, 1, 1, -1, 1, -1, -1]),
            DyckPath([1, 1, 1, -1, -1, -1, 1, -1]),
            DyckPath([1, -1, 1, -1, 1, -1]),
        ).arrange()

        good_paths[0].shift(UP)
        good_paths[1].shift(DOWN)
        good_paths[2].shift(UP)

        self.play(AnimationGroup(*[Write(p) for p in good_paths], lag_ratio=0.1))

        # animate arrange paths in a slightly better-looking order
        good_paths = VGroup(good_paths[0], good_paths[2], good_paths[1])

        self.play(good_paths.animate.arrange(DOWN, buff=0.54).move_to(LEFT * 3 + DOWN * 0.7), run_time=1.25)

        dyck_paths = Tex(r"Dyck Paths").next_to(good_paths, UP, buff=0.7)

        self.play(Write(dyck_paths))

        bad_paths = VGroup(
            DyckPath([-1, 1, 1, -1, 1, -1]),
            DyckPath(list(reversed([-1, -1, 1, 1, 1, -1, -1]))),
            DyckPath([1, 1, -1, 1]),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3 + DOWN * 0.7)

        self.play(AnimationGroup(*[Write(p) for p in bad_paths], lag_ratio=0.1))

        cross = Tex(r"$\times$").next_to(bad_paths, UP, buff=0.7).scale(2).set_color(RED)

        self.play(FadeIn(cross, shift=UP * 0.2))

        self.next_section()

        featured_path = good_paths[0]

        # transition
        self.play(
            self.camera.frame.animate.move_to(featured_path).set_width(featured_path.width * 1.5),
            FadeOut(good_paths[1]),
            FadeOut(good_paths[2]),
            FadeOut(bad_paths),
            FadeOut(cross),
            FadeOut(dyck_paths),
        )

        self.play(
            AnimationGroup(
            *list(map(lambda x: AnimationGroup(*x), zip(
                [featured_path.path.edges[(u, v)].animate.set_color(GREEN if featured_path.deltas[u] == 1 else RED)
                  for (u, v) in featured_path.path.edges],
                [Flash(
                    featured_path.path.edges[(u, v)],
                    line_width=0.04, flash_radius=0.05, line_stroke_width=1, line_length=0.04,
                    color=(GREEN if featured_path.deltas[u] == 1 else RED)
                    )
                  for (u, v) in featured_path.path.edges],
                ))),
            lag_ratio=0.05,
            )
        )



class AllDyckPaths(Scene):
    def construct(self):
        dp = [
            VGroup(*DyckPath.generate_dyck_paths(1)).arrange_in_grid(cols=1).set_width(1),
            VGroup(*DyckPath.generate_dyck_paths(2)).arrange_in_grid(cols=1).set_width(1.2),
            VGroup(*DyckPath.generate_dyck_paths(3)).arrange_in_grid(cols=1).set_width(1.5),
            VGroup(*DyckPath.generate_dyck_paths(4)).arrange_in_grid(cols=2).set_width(2.4),
        ]

        table = Table(
            [dp],
            element_to_mobject = lambda x: x,
            row_labels=[VGroup(Tex("Dyck"), Tex("Paths")).arrange(DOWN)],
            col_labels=[Tex("1"), Tex("2"), Tex("5"), Tex("14")],
            v_buff=0.4, h_buff=0.65,
            top_left_entry=Tex("$C_n$"),
            include_outer_lines=True,
        )

        table.remove(*table.get_vertical_lines())

        self.play(
            FadeIn(table.get_entries()),
            AnimationGroup(
                Write(table.get_horizontal_lines()[0]),
                Write(table.get_horizontal_lines()[2]),
                Write(table.get_horizontal_lines()[1]),
                lag_ratio=0.25,
            ),
        )


class FullBinaryTreeExample(MovingCameraScene):
    def construct(self):
        text = Tex("Full Binary Tree").scale(4.60)
        tree = FullBinaryTree.generate_binary_trees(6)[50]

        self.camera.frame.set_width(text.width * 1.5)

        self.play(Write(text))

        points = text[0][5].get_subpaths()[1]

        avg = points[0]
        for i in points[1:]:
            avg += i
        avg /= len(points)

        diff = tree.vertices[""].get_center() - avg
        tree.shift(-diff).shift(LEFT * 0.02)

        self.add(tree.vertices[""])

        self.play(
            self.camera.frame.animate.move_to(tree.vertices[""]).scale(1/4),
            FadeOut(text),
        )

        show_first = [
            tree.vertices["l"], tree.vertices["r"],
            tree.edges[("", "l")], tree.edges[("", "r")],
        ]

        self.play(
            AnimationGroup(
                self.camera.frame.animate.shift(DOWN * 0.5),
                AnimationGroup(
                    *[Write(a) for a in show_first],
                    lag_ratio=0.1,
                ),
                lag_ratio=0.3,
            )
        )

        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(tree).set_height(tree.height * 1.5),
                AnimationGroup(
                    *[Write(a)
                        for a in list(tree.vertices.values()) + list(tree.edges.values())
                        if a not in show_first + [tree.vertices[""]]],
                    lag_ratio=0.1,
                    run_time=1.5,
                ),
                lag_ratio=0.3,
            )
        )


class DyckToBinary(MovingCameraScene):

    def construct(self):
        dpath = DyckPath([1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1])

        self.camera.frame.set_width(dpath.width * 1.3)

        self.play(Write(dpath, run_time=1.5))

        all_paths = VGroup(dpath)

        anim, todo = dpath.get_last_hill_animations()

        self.play(anim)

        todo()

        def parallel_animate_subpath_creation(paths: List[DyckPath], all_paths, scale, vertices, edges):
            return_paths = []

            path_tuples = []

            for path in paths:

                if len(path.deltas) == 0:
                    continue

                l_path, r_path = path.get_left_right_subpaths(scale)

                vertices.append(l_path)
                vertices.append(r_path)
                edges.append((path, l_path))
                edges.append((path, r_path))

                return_paths.append(l_path)
                return_paths.append(r_path)

                self.bring_to_back(l_path)
                l_pathcopy = l_path.copy().next_to(path, DOWN, buff=0.5).align_to(path, LEFT).scale(0.85)
                l_path.fade(1)

                self.bring_to_back(r_path)
                r_pathcopy = r_path.copy().next_to(path, DOWN, buff=0.5).align_to(path, RIGHT).scale(0.85)
                r_path.fade(1)

                if l_pathcopy.height > r_pathcopy.height:
                    r_pathcopy.align_to(l_pathcopy, DOWN)
                else:
                    l_pathcopy.align_to(r_pathcopy, DOWN)

                all_paths.add(l_pathcopy)
                all_paths.add(r_pathcopy)

                path_tuples.append((l_path, r_path, l_pathcopy, r_pathcopy))

            self.play(
                *[Transform(lp, lpc) for lp, rp, lpc, rpc in path_tuples],
                *[Transform(rp, rpc) for lp, rp, lpc, rpc in path_tuples],
                self.camera.frame.animate.move_to(all_paths).set_height(max(self.camera.frame.height, all_paths.height * 1.25)),
            )

            hill_anims = [lp.get_last_hill_animations() for lp, rp, lpc, rpc in path_tuples] + [rp.get_last_hill_animations() for lp, rp, lpc, rpc in path_tuples]

            self.play(*[a for (a, _) in hill_anims])

            for _, todo in hill_anims:
                todo()

            for lp, rp, lpc, rpc in path_tuples:
                all_paths.remove(lpc)
                all_paths.remove(rpc)
                all_paths.add(lp)
                all_paths.add(rp)

            return return_paths

        vertices = [dpath]
        edges = []

        paths = parallel_animate_subpath_creation([dpath], all_paths, 1          , vertices, edges)
        paths = parallel_animate_subpath_creation(paths, all_paths, 1 * 0.85 ** 1, vertices, edges)
        paths = parallel_animate_subpath_creation(paths, all_paths, 1 * 0.85 ** 2, vertices, edges)
        paths = parallel_animate_subpath_creation(paths, all_paths, 1 * 0.85 ** 3, vertices, edges)

        g = Graph([id(v) for v in vertices], [(id(u), id(v)) for u, v in edges])

        for path in all_paths:
            g.vertices[id(path)].move_to(path).align_to(path, DOWN)

        self.play(
            *[
            FadeTransform(path, g.vertices[id(path)])
            for path in all_paths
            ],
            self.camera.frame.animate.move_to(VGroup(*list(g.vertices.values()))).set_height(VGroup(*list(g.vertices.values())).height * 1.5),
            run_time=1.5,
        )

        for path in all_paths:
            g.remove(g.vertices[id(path)])

        self.play(
            Write(g, run_time=2)
        )


class ExpressionExample(MovingCameraScene):
    def construct(self):
        expression = Tex(r"$(7+16) \times ((9 - 3) \div 2)$").scale(2)

        g = Graph(
                ["", "l", "r", "ll", "lr", "rl", "rr", "rll", "rlr"],
                [("", "l"),
                 ("", "r"),
                 ("l", "ll"),
                 ("l", "lr"),
                 ("r", "rl"),
                 ("r", "rr"),
                 ("rl", "rll"),
                 ("rl", "rlr")],
                layout="tree", root_vertex="").flip().scale(3)

        g.suspend_updating()

        for e in g.edges:
            g.edges[e].scale(0.5)

        align_object_by_coords(expression, expression[0][6].get_center(), g.vertices[""].get_center())

        self.camera.frame.move_to(expression)

        self.play(Write(expression, run_time=0.75))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    expression[0][0].animate.fade(1),
                    expression[0][5].animate.fade(1),
                    expression[0][7].animate.fade(1),
                    expression[0][15].animate.fade(1),
                ),
                AnimationGroup(
                    expression[0][1:5].animate.set_color(RED),
                    Circumscribe(expression[0][1:5], color=RED),
                    expression[0][8:15].animate.set_color(BLUE),
                    Circumscribe(expression[0][8:15], color=BLUE),
                ),
                lag_ratio=0.5,
            )
        )

        group = VGroup(g.vertices[""], g.vertices["l"], g.vertices["r"])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    align_object_by_coords(
                        expression[0][0:6],
                        expression[0][2].get_center(),
                        g.vertices["l"].get_center(),
                        animation=True),
                    align_object_by_coords(
                        expression[0][8:],
                        expression[0][13].get_center(),
                        g.vertices["r"].get_center(),
                        animation=True),
                ),
                AnimationGroup(
                    Write(g.edges[("", "l")]),
                    Write(g.edges[("", "r")]),
                ),
                lag_ratio=0.5,
            ),
            self.camera.frame.animate.move_to(group).set_height(max(self.camera.frame.height, group.height * 2)),
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    expression[0][8].animate.fade(1),
                    expression[0][12].animate.fade(1),
                ),
                AnimationGroup(
                    expression[0][2].animate.set_color(WHITE),
                    expression[0][1:2].animate.set_color(RED),
                    Circumscribe(expression[0][1:2], color=RED),
                    expression[0][3:5].animate.set_color(BLUE),
                    Circumscribe(expression[0][3:5], color=BLUE),

                    expression[0][13].animate.set_color(WHITE),
                    expression[0][9:12].animate.set_color(RED),
                    Circumscribe(expression[0][9:12], color=RED),
                    expression[0][14:15].animate.set_color(BLUE),
                    Circumscribe(expression[0][14:15], color=BLUE),
                ),
                lag_ratio=0.5,
            )
        )

        group = VGroup(g.vertices[""], g.vertices["l"], g.vertices["r"], g.vertices["ll"], g.vertices["rr"])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    align_object_by_coords(
                        expression[0][1:2],
                        expression[0][1:2].get_center(),
                        g.vertices["ll"].get_center(),
                        animation=True),
                    align_object_by_coords(
                        expression[0][3:5],
                        expression[0][3:5].get_center(),
                        g.vertices["lr"].get_center(),
                        animation=True),
                    align_object_by_coords(
                        expression[0][9:12],
                        expression[0][10].get_center(),
                        g.vertices["rl"].get_center(),
                        animation=True),
                    align_object_by_coords(
                        expression[0][14],
                        expression[0][14].get_center(),
                        g.vertices["rr"].get_center(),
                        animation=True),
                ),
                AnimationGroup(
                    Write(g.edges[("l", "ll")]),
                    Write(g.edges[("l", "lr")]),
                    Write(g.edges[("r", "rl")]),
                    Write(g.edges[("r", "rr")]),
                ),
                lag_ratio=0.5,
            ),
            self.camera.frame.animate.move_to(group).set_height(max(self.camera.frame.height, group.height * 1.6)),
        )

        self.play(
            expression[0][1].animate.set_color(WHITE),
            expression[0][3].animate.set_color(WHITE),
            expression[0][4].animate.set_color(WHITE),
            expression[0][10].animate.set_color(WHITE),
            expression[0][14].animate.set_color(WHITE),

            expression[0][9:10].animate.set_color(RED),
            Circumscribe(expression[0][9:10], color=RED),
            expression[0][11:12].animate.set_color(BLUE),
            Circumscribe(expression[0][11:12], color=BLUE),
        )

        group = VGroup(g.vertices[""], g.vertices["l"], g.vertices["r"], g.vertices["ll"], g.vertices["rr"], g.vertices["rll"], g.vertices["rlr"])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    align_object_by_coords(
                        expression[0][9],
                        expression[0][9].get_center(),
                        g.vertices["rll"].get_center(),
                        animation=True),
                    align_object_by_coords(
                        expression[0][11],
                        expression[0][11].get_center(),
                        g.vertices["rlr"].get_center(),
                        animation=True),
                ),
                AnimationGroup(
                    Write(g.edges[("rl", "rll")]),
                    Write(g.edges[("rl", "rlr")]),
                ),
                lag_ratio=0.5,
            ),
            self.camera.frame.animate.move_to(group).set_height(max(self.camera.frame.height, group.height * 1.4)),
        )

        self.play(
            expression[0].animate.set_color(WHITE),
        )



class TriangulatedPolygonExample(Scene):
    def construct(self):
        n = 8

        polygons = LinedPolygon.generate_triangulated_polygons(n)

        p = polygons[79].scale(2.5).rotate(PI / n)
        vertices = p.polygon.get_vertices()

        all_edges = list(p.edges) + [(i, (i + 1) % n) for i in range(n)]

        triangles_brr = set()

        print(all_edges)

        for e1 in all_edges:
            for e2 in all_edges:
                for e3 in all_edges:
                    if e1 == e2 or e2 == e3 or e1 == e3:
                        continue

                    s = tuple(set(e1).union(set(e2).union(set(e3))))

                    if len(s) == 3 and s not in triangles_brr:
                        triangles_brr.add(s)

        colors = [RED, "#ffd166", "#06d6a0", BLUE]
        all_colors = color_gradient(colors, len(triangles_brr))

        triangles = VGroup(*[Polygon(vertices[a], vertices[b], vertices[c], fill_opacity=1, color=all_colors[i])
                     for i, (a, b, c) in enumerate(triangles_brr)])

        for t in triangles:
            t.round_corners(0.01)

        self.play(Write(p),
                run_time=1.5,
                )

        self.play(
                FadeIn(triangles, lag_ratio=0.05, run_time=1.5),
                FadeIn(p, run_time=0), # hack
                )

class AllTriangulatedPolygons(Scene):
    def construct(self):

        dp = [
            VGroup(*LinedPolygon.generate_triangulated_polygons(3)).arrange_in_grid(cols=1).set_width(1),
            VGroup(*LinedPolygon.generate_triangulated_polygons(4)).arrange_in_grid(cols=1).set_width(0.95),
            VGroup(*LinedPolygon.generate_triangulated_polygons(5)).arrange_in_grid(cols=1).set_width(0.8),
            VGroup(*LinedPolygon.generate_triangulated_polygons(6)).arrange_in_grid(cols=2).set_width(1.3),
        ]

        table = Table(
            [dp],
            element_to_mobject = lambda x: x,
            row_labels=[Tex("Triangulations").rotate(PI / 2)],
            col_labels=[Tex("1"), Tex("2"), Tex("5"), Tex("14")],
            v_buff=0.4, h_buff=0.65,
            top_left_entry=Tex("$C_n$"),
            include_outer_lines=True,
        )

        table.remove(*table.get_vertical_lines())

        self.play(
            FadeIn(table.get_entries()),
            AnimationGroup(
                Write(table.get_horizontal_lines()[0]),
                Write(table.get_horizontal_lines()[2]),
                Write(table.get_horizontal_lines()[1]),
                lag_ratio=0.25,
            ),
        )


class PolygonToExpressionExample(MovingCameraScene):
    def construct(self):
        polygon = LinedPolygon.generate_triangulated_polygons(6)[12].scale(2)

        self.play(Write(polygon))

        vertices = polygon.polygon.get_vertices()

        red_line = Line(start=vertices[2], end=vertices[1], color=RED, stroke_width=8)

        vertice_objects = VGroup(*[Dot().move_to(v) for v in vertices])

        self.play(
            FadeIn(red_line),
            Flash(red_line, color=RED),
            FadeIn(vertice_objects),
        )

        vertex_labels = VGroup(
            Tex("1").move_to((vertices[2] + vertices[3]) / 2 * 1.3),
            Tex("2").move_to((vertices[3] + vertices[4]) / 2 * 1.3),
            Tex("3").move_to((vertices[4] + vertices[5]) / 2 * 1.3),
            Tex("4").move_to((vertices[5] + vertices[0]) / 2 * 1.3),
            Tex("5").move_to((vertices[0] + vertices[1]) / 2 * 1.3),
        )

        self.play(
            FadeIn(vertex_labels[0], shift=(vertices[2] + vertices[3]) / 2 * 0.2),
            FadeIn(vertex_labels[1], shift=(vertices[3] + vertices[4]) / 2 * 0.2),
            FadeIn(vertex_labels[2], shift=(vertices[4] + vertices[5]) / 2 * 0.2),
            FadeIn(vertex_labels[3], shift=(vertices[5] + vertices[0]) / 2 * 0.2),
            FadeIn(vertex_labels[4], shift=(vertices[0] + vertices[1]) / 2 * 0.2),
        )

        size = vertices[5] - vertices[4]

        other_lines = Path([vertices[2], vertices[3], vertices[4], vertices[5], vertices[0], vertices[1]])

        polygon.remove(polygon.polygon)
        self.bring_to_back(other_lines)

        self.play(
            FadeOut(red_line),
        )

        new_path = Path([
            vertices[4] - size * 2,
            vertices[4] - size * 1,
            vertices[4],
            vertices[4] + size * 1,
            vertices[4] + size * 2,
            vertices[4] + size * 3,
            ])

        arcs = VGroup(
            ArcBetweenPoints(new_path[0], new_path[2], angle=-PI / 2),
            ArcBetweenPoints(new_path[0], new_path[3], angle=-PI / 1.3),
            ArcBetweenPoints(new_path[5], new_path[3], angle=PI / 2),
        )

        all_stuff = VGroup(arcs, vertice_objects)

        self.play(
            Transform(other_lines, new_path),
            Transform(list(polygon.edges.values())[1], arcs[0]),
            Transform(list(polygon.edges.values())[2], arcs[1]),
            Transform(list(polygon.edges.values())[0], arcs[2]),
            vertex_labels[0].animate.next_to((new_path[0] + new_path[1]) / 2, DOWN, buff=0.4),
            vertex_labels[1].animate.next_to((new_path[1] + new_path[2]) / 2, DOWN, buff=0.4),
            vertex_labels[2].animate.next_to((new_path[2] + new_path[3]) / 2, DOWN, buff=0.4),
            vertex_labels[3].animate.next_to((new_path[3] + new_path[4]) / 2, DOWN, buff=0.4),
            vertex_labels[4].animate.next_to((new_path[4] + new_path[5]) / 2, DOWN, buff=0.4),
            vertice_objects[2].animate.move_to(new_path[0]),
            vertice_objects[3].animate.move_to(new_path[1]),
            vertice_objects[4].animate.move_to(new_path[2]),
            vertice_objects[5].animate.move_to(new_path[3]),
            vertice_objects[0].animate.move_to(new_path[4]),
            vertice_objects[1].animate.move_to(new_path[5]),
            self.camera.frame.animate.shift(DOWN),
            run_time=2,
        )

        parentheses = VGroup(
            Tex("(").next_to(new_path[0], DOWN, buff=0.4).shift(LEFT * 0.2),
            Tex("(").next_to(new_path[0], DOWN, buff=0.4).shift(RIGHT * 0.2),
            Tex(")").next_to(new_path[2], DOWN, buff=0.4),
            Tex("(").next_to(new_path[3], DOWN, buff=0.4).shift(RIGHT * 0.2),
            Tex(")").next_to(new_path[3], DOWN, buff=0.4).shift(LEFT * 0.2),
            Tex(")").next_to(new_path[5], DOWN, buff=0.4),
        ).shift(UP * 0.05)

        expression = Tex("$((1 + 2) * 3) - (4 \div 5)$").scale(2).shift(2.5 * DOWN)

        plus = expression[0][3].copy()
        expression[0][3].fade(1)

        times = expression[0][6].copy()
        expression[0][6].fade(1)

        minus = expression[0][9].copy()
        expression[0][9].fade(1)

        div = expression[0][12].copy()
        expression[0][12].fade(1)

        self.play(
                FadeIn(parentheses, lag_ratio=0.1),
                )

        self.play(
                FadeOut(vertice_objects),
                FadeOut(VGroup(*list(polygon.edges.values()))),
                FadeOut(other_lines),
                TransformMatchingShapes(VGroup(*vertex_labels, *parentheses), expression),
                Transform(vertice_objects[3], plus),
                Transform(vertice_objects[4], times),
                Transform(vertice_objects[5], minus),
                Transform(vertice_objects[0], div),
                self.camera.frame.animate.move_to(expression),
                run_time=1.5,
        )
