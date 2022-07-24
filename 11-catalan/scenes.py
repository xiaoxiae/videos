from utilities import *


class ConstructStarsExample(MovingCameraScene):
    def construct(self):
        height_scale = 1.6

        star_offset=0.25

        n = 4
        tree = BinaryTree.generate_binary_trees(n)[6]
        tree_nolabels = tree.copy()

        StarUtilities.add_stars_to_graph(tree, star_offset=star_offset)
        StarUtilities.add_stars_to_graph(tree_nolabels, star_offset=star_offset, no_labels=True)

        self.camera.frame.move_to(tree).set_height(tree.height * height_scale)

        self.play(FadeIn(tree_nolabels, shift=DOWN * 0.1))

        self.play(
            AnimationGroup(
                *[Wiggle(tree_nolabels.vertices[s], scale_value=1.5) for s in StarUtilities.get_all_stars(tree_nolabels)],
                lag_ratio=0.03,
            )
        )

        self.play(
            AnimationGroup(
                *[FadeIn(tree.vertices[s][1], run_time=0.6) for s in StarUtilities.get_all_stars(tree)],
                lag_ratio=0.07,
            ),
            AnimationGroup(
                *[Circumscribe(tree.vertices[s][1],
                    color=BLACK,
                    run_time=0.6,
                    shape=Circle,
                    stroke_width=1.2,
                    buff=0.01) for s in StarUtilities.get_all_stars(tree)],
                lag_ratio=0.07,
            ),
        )

        for obj in self.mobjects:
            self.remove(obj)
        self.add(tree)

        from math import factorial

        for i in range(30):
            self.play(ChangeStars(tree, i, i + 1), run_time=0.5 if i < 3 else (1 / (i - 1)) ** (3/2))

        self.play(ChangeStars(tree, i, factorial(n + 1) - 1), run_time=0.1)

        self.wait(0.5)

        TEXT_SCALE = 0.4

        llb = Tex(r"$$\mathrm{LLB}_{2n + 1} = C_n (n + 1)!$$").scale(TEXT_SCALE).next_to(tree, LEFT, buff=1)

        llb_compute = Tex(r"$$= \left(2 \cdot 1\right) \left(2 \cdot 3\right) \ldots \left(2 \cdot (2n + 1)\right)$$").scale(TEXT_SCALE)

        self.play(
            FadeIn(llb, shift=LEFT * 0.1),
            self.camera.frame.animate.move_to(VGroup(llb, tree)),
        )

        self.play(
            AnimationGroup(
                *[Circumscribe(tree.vertices[s], shape=Circle,
                    color=WHITE if not StarUtilities.is_star_name(s) else GREEN,
                    stroke_width=1,
                    buff=0.03)
                  for s in tree.vertices],
                lag_ratio=0.05,
            )
        )

        tree.suspend_updating()

        subtree = VGroup(
            tree.vertices["r"],
            tree.vertices["rl"],
            tree.vertices["star_1"],
            tree.vertices["star_2"],
            tree.vertices["star_3"],
            tree.edges[("r", "rl")],
            tree.edges[("r", "star_1")],
            tree.edges[("rl", "star_2")],
            tree.edges[("rl", "star_3")],
        )

        ldot = Dot().move_to(StarUtilities.get_star_position(tree, "r", LEFT, star_offset=star_offset)).scale(0.5).set_color(DARK_GRAY)
        rdot = Dot().move_to(StarUtilities.get_star_position(tree, "r", RIGHT, star_offset=star_offset)).scale(0.5).set_color(DARK_GRAY)

        vpos = tree.vertices["r"].get_center()

        ldot_line = Line(vpos, ldot.get_center(), stroke_width=tree.edges[("", "r")].stroke_width * 0.75).set_color(DARK_GRAY)
        rdot_line = Line(vpos, rdot.get_center(), stroke_width=tree.edges[("", "r")].stroke_width * 0.75).set_color(DARK_GRAY)

        subtree.shift(DOWN)
        scale = self.camera.frame.height / (VGroup(tree, llb).height * height_scale)
        animation = self.camera.frame.animate.move_to(VGroup(tree, llb)).set_height(VGroup(tree, llb).height * height_scale)
        subtree.shift(UP)

        v = BinaryTree.generate_binary_trees(1)[0].move_to(vpos)
        v.set_z_index(1)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    subtree.animate.shift(DOWN),
                    animation,
                ),
                AnimationGroup(
                    FadeIn(v),
                    AnimationGroup(
                        FadeIn(ldot),
                        Flash(ldot, color=DARK_GRAY, line_stroke_width=1, flash_radius=0.1, line_length=0.05),
                        Write(ldot_line),
                    ),
                    AnimationGroup(
                        FadeIn(rdot),
                        Flash(rdot, color=DARK_GRAY, line_stroke_width=1, flash_radius=0.1, line_length=0.05),
                        Write(rdot_line),
                    ),
                    lag_ratio=0.15,
                ),
                lag_ratio=0.5,
            )
        )

        self.bring_to_back(ldot)
        self.bring_to_back(rdot)
        self.bring_to_back(ldot_line)
        self.bring_to_back(rdot_line)

        star = StarUtilities.create_star_object("6").move_to(rdot).set_z_index(1)

        l1 = Line(vpos, ldot.get_center(), stroke_width=tree.edges[("", "r")].stroke_width)
        l2 = Line(vpos, rdot.get_center(), stroke_width=tree.edges[("", "r")].stroke_width)

        subtree.shift(UP * 0.5)
        scale = self.camera.frame.height / (VGroup(tree, llb).height * height_scale)
        animation = self.camera.frame.animate.move_to(VGroup(tree, llb)).set_height(VGroup(tree, llb).height * height_scale)
        subtree.shift(DOWN * 0.5)

        self.play(
            AnimationGroup(
                align_object_by_coords(subtree, tree.vertices["r"].get_center(), ldot.get_center(), animation=True),
                AnimationGroup(
                    Write(star),
                ),
                AnimationGroup(
                    Write(l1),
                    Write(l2),
                    lag_ratio=0.1,
                ),
                lag_ratio=0.5,
            ),
            animation,
        )

        self.remove(ldot)
        self.remove(rdot)
        self.remove(ldot_line)
        self.remove(rdot_line)

        entire_tree = VGroup(tree, star, l1, l2, v)

        align_object_by_coords(llb_compute, llb_compute[0][0].get_center(), llb[0][7].get_center())
        llb_compute.shift(RIGHT * 1.23)

        shift = RIGHT * 2.6
        entire_tree.shift(shift)
        animation = self.camera.frame.animate.move_to(VGroup(entire_tree, llb[0][8:]))
        entire_tree.shift(-shift)

        self.play(
            FadeOut(llb[0][0:8]),
            AnimationGroup(
                entire_tree.animate.shift(shift),
                FadeIn(llb_compute, shift=RIGHT * 0.2),
                lag_ratio=0.5,
            ),
            animation,
        )

        next_part = Tex(r"$$C_n = \frac{\left(2 \cdot 1\right) \left(2 \cdot 3\right) \ldots \left(2 \cdot (2n + 1)\right)}{(n + 1)!}$$").scale(TEXT_SCALE)
        align_object_by_coords(next_part, next_part[0][2].get_center(), llb_compute[0][0].get_center())
        next_part.shift(LEFT * 0.5)

        def return_symbol_transforms(a, b, i, j, n):
            return [ReplacementTransform(a[0][i + k], b[0][j + k]) for k in range(n)]

        # it randomly starts updating here
        tree.remove(tree.edges[("", "r")])
        entire_tree.add(Line(tree.vertices[""].get_center(), v.get_center(), stroke_width=tree.edges[("", "r")].stroke_width))

        self.play(
            *return_symbol_transforms(llb_compute, next_part, 0, 2, 24),
            *return_symbol_transforms(llb, next_part, 10, 27, 6),
            *return_symbol_transforms(llb, next_part, 8, 0, 2),
            Succession(Wait(0.2), FadeIn(next_part[0][26])),
        )

        more_next_part = Tex(r"$$C_n = \frac{1}{n + 1} \cdot \binom{2n}{n}$$").scale(TEXT_SCALE)

        align_object_by_coords(more_next_part, more_next_part[0][2].get_center(), next_part[0][2].get_center())

        self.play(
            Transform(next_part[0][3:], more_next_part[0][3:])
        )

        for o in self.mobjects:
            self.remove(o)

        mnp = more_next_part.copy().scale(1.5)
        et = entire_tree.copy()

        g = VGroup(mnp, et).arrange(buff=1.5)

        self.play(
            Transform(more_next_part, mnp),
            Transform(entire_tree, et),
            self.camera.frame.animate.move_to(g),
        )


class DyckPathExamples(MovingCameraScene):
    def construct(self):
        good_paths = VGroup(
            DyckPath([1, -1, 1, 1, -1, 1, -1, -1]),
            DyckPath([1, 1, 1, -1, -1, -1, 1, -1]),
            DyckPath([1, -1, 1, -1, 1, -1]),
        ).arrange()

        good_paths[0].shift(UP + RIGHT * 0.5)
        good_paths[1].shift(DOWN)
        good_paths[2].shift(UP + LEFT * 0.5)

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

        cross = Tex(r"$\times$").next_to(bad_paths, UP, buff=0.7).scale(2).set_color(RED)

        self.play(
            AnimationGroup(
                AnimationGroup(*[Write(p) for p in bad_paths], lag_ratio=0.1),
                FadeIn(cross, shift=UP * 0.2),
                lag_ratio=0.1,
            )
        )

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
            lag_ratio=0.1,
            )
        )


class AllDyckPaths(Scene):
    def construct(self):
        dp = [
            VGroup(*DyckPath.generate_dyck_paths(0)).arrange_in_grid(cols=1, buff=0.8).set_width(0.15),
            VGroup(*DyckPath.generate_dyck_paths(1)).arrange_in_grid(cols=1, buff=0.8).set_width(1),
            VGroup(*DyckPath.generate_dyck_paths(2)).arrange_in_grid(cols=1, buff=0.8).set_width(1.2),
            VGroup(*DyckPath.generate_dyck_paths(3)).arrange_in_grid(cols=1, buff=0.8).set_width(1.2),
            VGroup(*DyckPath.generate_dyck_paths(4)).arrange_in_grid(cols=2, buff=0.8).set_width(2.4),
        ]

        for graph in dp[2]:
            for v in graph.path.vertices:
                graph.path.vertices[v].scale(1.1)

        for graph in dp[3]:
            for v in graph.path.vertices:
                graph.path.vertices[v].scale(1.4)

        for graph in dp[4]:
            for v in graph.path.vertices:
                graph.path.vertices[v].scale(1.8)

        table = Table(
            [dp],
            element_to_mobject = lambda x: x,
            row_labels=[Tex("Dyck Paths").rotate(PI / 2)],
            col_labels=[Tex("1"), Tex("1"), Tex("2"), Tex("5"), Tex("14")],
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
            lines = []

            for path in paths:

                if len(path.deltas) == 0:
                    continue

                l_path, r_path = path.get_left_right_subpaths(scale)

                vertices.append(l_path)
                vertices.append(r_path)

                # lines
                avg = (path.get_center() + l_path.get_center()) / 2
                avg = (path.get_center() + r_path.get_center()) / 2

                return_paths.append(l_path)
                return_paths.append(r_path)

                self.bring_to_back(l_path)
                l_pathcopy = l_path.copy().next_to(path, DOWN, buff=0.75).align_to(path, LEFT).scale(0.85)
                l_path.fade(1)

                self.bring_to_back(r_path)
                r_pathcopy = r_path.copy().next_to(path, DOWN, buff=0.75).align_to(path, RIGHT).scale(0.85)
                r_path.fade(1)

                if l_pathcopy.height > r_pathcopy.height:
                    r_pathcopy.align_to(l_pathcopy, DOWN)
                else:
                    l_pathcopy.align_to(r_pathcopy, DOWN)

                all_paths.add(l_pathcopy)
                all_paths.add(r_pathcopy)

                lines.append(Line(path.get_center() * 0.5 +  l_pathcopy.get_center() * 0.5, path.get_center() * 0.3 +  l_pathcopy.get_center() * 0.7, stroke_width=3.3 * scale).set_opacity(0.3).scale(0.9))
                edges.append((path, l_path, lines[-1]))
                lines.append(Line(path.get_center() * 0.5 +  r_pathcopy.get_center() * 0.5, path.get_center() * 0.3 +  r_pathcopy.get_center() * 0.7, stroke_width=3.3 * scale).set_opacity(0.3).scale(0.9))
                edges.append((path, r_path, lines[-1]))

                path_tuples.append((path, l_path, r_path, l_pathcopy, r_pathcopy))

            self.play(
                *[Transform(lp, lpc) for _, lp, rp, lpc, rpc in path_tuples],
                *[Transform(rp, rpc) for _, lp, rp, lpc, rpc in path_tuples],
                *[Succession(Wait(0.6), Write(line, run_time=0.5)) for line in lines],
                self.camera.frame.animate.move_to(all_paths).set_height(max(self.camera.frame.height, all_paths.height * 1.25)),
            )

            hill_anims = [lp.get_last_hill_animations() for _, lp, rp, lpc, rpc in path_tuples] + [rp.get_last_hill_animations() for _, lp, rp, lpc, rpc in path_tuples]

            self.play(
                *[a for (a, _) in hill_anims],
            )

            for _, todo in hill_anims:
                todo()

            for _, lp, rp, lpc, rpc in path_tuples:
                all_paths.remove(lpc)
                all_paths.remove(rpc)
                all_paths.add(lp)
                all_paths.add(rp)

            return return_paths

        vertices = [dpath]
        edges = []

        paths = parallel_animate_subpath_creation([dpath], all_paths, 1          , vertices, edges)
        paths = parallel_animate_subpath_creation(paths, all_paths, 1 * 0.75 ** 1, vertices, edges)
        paths = parallel_animate_subpath_creation(paths, all_paths, 1 * 0.75 ** 2, vertices, edges)
        paths = parallel_animate_subpath_creation(paths, all_paths, 1 * 0.75 ** 3, vertices, edges)

        g = Graph([id(v) for v in vertices], [(id(u), id(v)) for u, v, _ in edges])

        for path in all_paths:
            g.vertices[id(path)].move_to(path).align_to(path, DOWN).scale(1.75)

        for u, v, e in edges:
            g.edges[(id(u), id(v))].put_start_and_end_on(g.vertices[id(u)].get_center(), g.vertices[id(v)].get_center())

        self.play(
            *[FadeTransform(path, g.vertices[id(path)]) for path in all_paths],
            self.camera.frame.animate.move_to(VGroup(*list(g.vertices.values()))).set_height(VGroup(*list(g.vertices.values())).height * 1.5),
            *[Transform(e, g.edges[(id(u), id(v))]) for u, v, e in edges],
            run_time=1.5,
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

        g_copy = g.copy()

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

        for v in g.vertices:
            g.vertices[v].scale(1.5)

        self.play(
            *[Transform(g.edges[e], g_copy.edges[e]) for e in g_copy.edges],
            FadeTransform(expression[0][6], g.vertices[""]),
            FadeTransform(expression[0][2], g.vertices["l"]),
            FadeTransform(expression[0][13], g.vertices["r"]),
            FadeTransform(expression[0][1], g.vertices["ll"]),
            FadeTransform(expression[0][3:5], g.vertices["lr"]),
            FadeTransform(expression[0][10], g.vertices["rl"]),
            FadeTransform(expression[0][14], g.vertices["rr"]),
            FadeTransform(expression[0][9], g.vertices["rll"]),
            FadeTransform(expression[0][11], g.vertices["rlr"]),
        )


class TriangulatedPolygonExample(MovingCameraScene):
    """Note: this animation takes a few minutes to compute since we're creating a lot of shapes inefficiently."""

    def construct(self):
        n = 8
        count = 79

        polygons = VGroup(*LinedPolygon.generate_triangulated_polygons(n))

        for polygon in polygons:
            polygon.rotate(PI / n)

        p = polygons[count].scale(2.5)

        self.play(Write(p.polygon), run_time=1)

        self.play(Write(VGroup(*list(p.edges.values())), run_time=1.5))

        triangles = create_polygon_triangles(p)
        self.bring_to_back(triangles)

        self.play(FadeIn(triangles, lag_ratio=0.05, run_time=1.5))

        p.add_to_back(triangles)

        polygons = VGroup(*LinedPolygon.generate_triangulated_polygons(n))

        for polygon in polygons:
            polygon.rotate(PI / n)
            polygon.add_to_back(create_polygon_triangles(polygon))

        polygons.arrange_in_grid(cols=17, buff=0.3)
        polygons.scale(2.5)

        pos = polygons[count].get_center()
        polygons.remove(polygons[count])

        align_object_by_coords(polygons, pos, p.get_center())

        def dist(a, b):
            x1, y1, z1 = a.get_center()
            x2, y2, z2 = b.get_center()

            return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** (1/2)

        self.play(
            self.camera.frame.animate(run_time=2).set_width(polygons.width * 1.15).move_to(polygons),
            *[Succession(Wait(dist(p, q) / 35), Write(q)) for q in polygons]
        )


class AllBinaryTrees(Scene):
    def construct(self):

        dp = [
            VGroup(*FullBinaryTree.generate_binary_trees(0)).arrange_in_grid(cols=1, buff=0.6).set_width(0.2),
            VGroup(*FullBinaryTree.generate_binary_trees(1)).arrange_in_grid(cols=1, buff=0.6).set_width(1),
            VGroup(*FullBinaryTree.generate_binary_trees(2)).arrange_in_grid(cols=1, buff=0.6).set_width(1),
            VGroup(*FullBinaryTree.generate_binary_trees(3)).arrange_in_grid(cols=2, buff=0.6).set_width(2),
            VGroup(*FullBinaryTree.generate_binary_trees(4)).arrange_in_grid(cols=3, buff=1.2).set_width(2.2),
        ]

        for graph in dp[2]:
            for v in graph.vertices:
                graph.vertices[v].scale(1.1)

        for graph in dp[3]:
            for v in graph.vertices:
                graph.vertices[v].scale(1.2)

        for graph in dp[4]:
            for v in graph.vertices:
                graph.vertices[v].scale(1.8)


        table = Table(
            [dp],
            element_to_mobject = lambda x: x,
            row_labels=[Tex("Full Binary Trees").rotate(PI / 2)],
            col_labels=[Tex("1"), Tex("1"), Tex("2"), Tex("5"), Tex("14")],
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


class AllTriangulatedPolygons(Scene):
    def construct(self):

        dp = [
            VGroup(*LinedPolygon.generate_triangulated_polygons(3)).arrange_in_grid(cols=1, buff=0.8).set_width(1),
            VGroup(*LinedPolygon.generate_triangulated_polygons(4)).arrange_in_grid(cols=1, buff=0.3).set_width(0.90),
            VGroup(*LinedPolygon.generate_triangulated_polygons(5)).arrange_in_grid(cols=1, buff=0.5).set_width(0.75),
            VGroup(*LinedPolygon.generate_triangulated_polygons(6)).arrange_in_grid(cols=2, buff=0.6).set_width(1.3),
        ]

        table = Table(
            [dp],
            element_to_mobject = lambda x: x,
            row_labels=[Tex("Triangulations").rotate(PI / 2)],
            col_labels=[Tex("1"), Tex("1"), Tex("2"), Tex("5"), Tex("14")],
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

        expression = Tex(r"$((1 + 2) \times 3) - (4 \div 5)$").scale(2).shift(2.5 * DOWN)

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


class Intro(MovingCameraScene):
    def construct(self):
        pi = Tex(r"$$\pi$$").scale(8)

        self.play(
            AnimationGroup(
                Write(pi),
                Flash(pi, color=WHITE, flash_radius=1.5),
                lag_ratio=0.5,
                run_time=1.5
            )
        )

        expressions = VGroup(
            Tex(r"$$\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}$$"),
            Tex(r"$$n! \approx \sqrt{2 \pi n} \left(\frac{n}{e}\right)^n$$"),
            Tex(r"$$e^{i \pi} = -1$$"),
        ).scale(1.5)

        #expressions[0][0][10].set_color(BLUE)
        #expressions[1][0][6].set_color(BLUE)
        #expressions[2][0][2].set_color(BLUE)

        self.play(
            AnimationGroup(
                Transform(pi, expressions[0][0][10]),
                AnimationGroup(
                    FadeIn(expressions[0][0][:10]),
                    FadeIn(expressions[0][0][11:]),
                ),
                lag_ratio=0.25,
            )
        )

        self.remove(pi)

        self.play(
            AnimationGroup(
                FadeOut(expressions[0][0]),
                Transform(expressions[0][0][10], expressions[1][0][6]),
                AnimationGroup(
                    FadeIn(expressions[1][0][:6]),
                    FadeIn(expressions[1][0][7:]),
                ),
                lag_ratio=0.25,
            )
        )

        self.remove(expressions[0][0][10])

        self.play(
            AnimationGroup(
                FadeOut(expressions[1][0]),
                Transform(expressions[1][0][6], expressions[2][0][2]),
                AnimationGroup(
                    FadeIn(expressions[2][0][:2]),
                    FadeIn(expressions[2][0][3:]),
                ),
                lag_ratio=0.25,
            )
        )


class IntroCatalan(MovingCameraScene):
    def construct(self):
        catalan_numbers = Tex(r"Catalan numbers").scale(2)

        catalan_formula = Tex(r"$$C_n = \frac{1}{n + 1} \cdot \binom{2n}{n}$$").shift(DOWN)

        self.play(Write(catalan_numbers))

        self.play(
            catalan_numbers.animate.shift(UP),
            FadeIn(catalan_formula, shift=UP * 0.5),
        )

        catalan_sequence = Tex(r"$$= 1, 1, 2, 5, 14, 42, \ldots$$").next_to(catalan_formula, DOWN).align_to(catalan_formula[0][2], LEFT)

        self.play(
            FadeIn(catalan_sequence, shift=UP * 0.3, lag_ratio=0.05),
        )

        objects = VGroup(
            BinaryTree.generate_binary_trees(2)[0],
            DyckPath([1, -1, 1, 1, -1, 1, -1, -1]),
            LinedPolygon.generate_triangulated_polygons(7)[10],
        )

        StarUtilities.add_stars_to_graph(objects[0], no_labels=True)

        objects[2].add_to_back(create_polygon_triangles(objects[2]))

        for (u, v) in objects[1].path.edges:
            objects[1].path.edges[(u, v)].set_color(GREEN if objects[1].deltas[u] == 1 else RED)

        objects.arrange(buff=1.5).move_to(catalan_formula).shift(DOWN * 3.6)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate.shift(DOWN * 3.1),
                    catalan_numbers.animate.shift(UP * 2),
                ),
                AnimationGroup(
                    FadeIn(objects[0], shift=UP * 0.7),
                    FadeIn(objects[1], shift=UP * 0.7),
                    FadeIn(objects[2], shift=UP * 0.7),
                    lag_ratio=0.1,
                ),
                lag_ratio=0.5,
            )
        )
