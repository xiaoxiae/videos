from utilities import *

GRAPH_SCALE = 3.2

HIDDEN_COLOR = DARKER_GRAY
HIGHLIGHT_COLOR = YELLOW


def yield_spanning_trees(vertices, edges):
    n = len(vertices)
    for subset in itertools.combinations(edges, n - 1):
        g = nx.Graph()
        g.add_nodes_from(vertices)
        g.add_edges_from(subset)

        if nx.algorithms.components.is_connected(g):
            yield subset

def get_random_spanning_tree(vertices, edges):
    return choice(list(yield_spanning_trees(vertices, edges)))

def strip_graph(g, edges):
    for e in list(g.edges):
        if e not in edges:
            g.remove(g.edges[e])
            del g.edges[e]

class Definitions(Scene):
    @fade
    def construct(self):
        n_min = 4
        n_max = 7 + 1

        layout_graphs = [Graph([i for i in range(n)],
            [(i, j) for i in range(n) for j in range(n) if i < j],
            layout="circular", layout_scale=0.7).scale(GRAPH_SCALE)
            for n in range(n_min, n_max)]

        layout_graph_texts = [Tex(f"$K_{n}$").shift(UP * 2.05 + RIGHT * 2.4).scale(1.3) for n in range(n_min, n_max)]

        g = Graph([i for i in range(n_max-1)],
            [(i, j) for i in range(n_max-1) for j in range(n_max-1) if i < j]).scale(GRAPH_SCALE)

        layout_graph = layout_graphs[0]
        for i, v in enumerate(g.vertices):
            rand = random() / 10000 + 1
            new_pos = layout_graph.vertices[min(i, len(layout_graph.vertices) - 1)].get_center() * rand
            g.vertices[i].move_to(new_pos)

        self.play(Write(g), Write(layout_graph_texts[0]))

        for i in range(len(layout_graphs) - 1):
            i += 1
            layout_graph = layout_graphs[i]
            new_positions = []

            for j, v in enumerate(g.vertices):

                rand = random() / 10000 + 1
                new_pos = layout_graph.vertices[min(j, len(layout_graph.vertices) - 1)].get_center() * rand

                new_positions.append(new_pos)

            self.play(
                *[g.vertices[v].animate.move_to(new_positions[v]) for v in g.vertices],
                Transform(layout_graph_texts[0], layout_graph_texts[i])
            )

        for e in layout_graphs[-1].edges:
            layout_graphs[-1].edges[e].set_color(HIDDEN_COLOR)
        for v in layout_graphs[-1].vertices:
            layout_graphs[-1].vertices[v].set_color(HIDDEN_COLOR)

        self.add(layout_graphs[-1])
        self.add(g)

        seed(0)
        st = list(yield_spanning_trees(g.vertices, g.edges))
        shuffle(st)

        i = 0
        for spanning_tree in st:
            if i == 3:
                break

            self.play(
                *[g.edges[e].animate.set_opacity(0) for e in g.edges if e not in spanning_tree],
                *[g.edges[e].animate.set_opacity(1) for e in spanning_tree],
            )

            i += 1

class Formula(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Cayley's Formula")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 1.2))

        text = Tex("\parbox{23em}{The number of ","spanning trees"," of a ","complete graph"," on ","$n$"," vertices is ","$\kappa(n) = n^{n-2}$",".}")
        highlightText(text)

        text.next_to(title, DOWN * 2)

        self.play(Write(text))

        self.play(
            title.animate.shift(UP * 1.3),
            text.animate.shift(UP * 1.3)
        )

        a = Graph([0, 1, 2], [(0, 1), (1, 2)], layout="circular", labels=True, layout_scale=0.8).scale(1.25).shift(DOWN * 1.6).shift(LEFT * 4)
        b = Graph([0, 1, 2], [(1, 2), (2, 0)], layout="circular", labels=True, layout_scale=0.8).scale(1.25).shift(DOWN * 1.6)
        c = Graph([0, 1, 2], [(2, 0), (0, 1)], layout="circular", labels=True, layout_scale=0.8).scale(1.25).shift(DOWN * 1.6).shift(RIGHT * 4)

        ne1 = Tex(r"\large$\ne$").move_to((a.get_center() + b.get_center()) / 2)
        ne2 = Tex(r"\large$\ne$").move_to((b.get_center() + c.get_center()) / 2)

        self.play(
            Write(a),
            Write(b),
            Write(c),
        )

        self.play(
            Write(ne1),
            Write(ne2),
        )


def create_oriented_edge(g, v, w):
    """Create an oriented edge from v to w."""
    v_center = g.vertices[v].get_center()
    w_center = g.vertices[w].get_center()

    center = (v_center + w_center) / 2
    delta = (v_center - w_center) / 2

    buffer = 0.23
    mag = (delta[0] ** 2 + delta[1] ** 2)**(1/2)
    c = (mag - buffer) / mag

    return Arrow(center + delta * c, center - delta * c, max_tip_length_to_length_ratio=30, buff=0)


def orient_from_root(g, root):
    queue = [root]
    explored = set([root])
    e = []

    g.clear_updaters()

    g.vertices[root].set_color(HIGHLIGHT_COLOR)

    while len(queue) != 0:
        current = queue.pop(0)

        # for each neighbour
        for v in edgesToVertices([(u, v) for u, v in g.edges if u == current or v == current]):
            if v == current:
                continue

            if v in explored:
                continue

            queue.append(v)
            explored.add(v)

            w, v = current, v

            e.append((v, w))
            a = create_oriented_edge(g, v, w)

            g.edges[(v, w) if (v, w) in g.edges else (w, v)].become(a)

    return e


def create_edge_number(g, v, w, i, scale=0.8, shift_coefficient=0.3, side=False):
    number = Tex(str(i)).scale(scale)

    v_center = g.vertices[v].get_center()
    w_center = g.vertices[w].get_center()

    center = (v_center + w_center) / 2
    delta = (v_center - w_center)
    delta /= (delta[0] ** 2 + delta[1] ** 2)**(1/2)

    # rotate 90 degrees
    if side:
        delta[0], delta[1] = -delta[1], delta[0]
    else:
        delta[0], delta[1] = delta[1], -delta[0]

    number.move_to(center).shift(delta * shift_coefficient)

    return number


def add_edge_numbering(graph, numbers=None, return_only=False):
    if not numbers:
        numbers = [i + 1 for i in range(len(graph.edges))]
        shuffle(numbers)

    if not return_only:
        graph.edge_numbers = {}
    else:
        numbers_tex = []

    for i, (v, w) in enumerate(graph.edges):
        number = create_edge_number(graph, v, w, numbers[i])

        if not return_only:
            graph.add(number)
            graph.edge_numbers[(v, w)] = number
        else:
            numbers_tex.append(number)

    if return_only:
        return numbers_tex


class Proof(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Double counting")

        self.play(Write(title))
        self.play(title.animate.shift(UP * 1.2))

        text = Tex("\parbox{23em}{The number of ","oriented trees"," on ","$n$"," vertices that have a ","root"," and some ","numbering of edges"," – ",r"$\tau(n)$",".}")
        highlightText(text)

        text.next_to(title, DOWN * 2)

        self.play(Write(text), run_time=2)

        self.play(FadeOut(title))
        self.play(text.animate.align_on_border(UP))

        l = Line(LEFT * 8, RIGHT * 8).next_to(text, DOWN).shift(DOWN * 0.15)
        self.play(Write(l))

        DOWN_C = 1.03

        n = 6
        g1 = Graph([i for i in range(n)],
                [(i, j) for i in range(n) for j in range(n) if i < j],
                layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C + RIGHT * 2.9)

        n = 7
        g2 = Graph([i for i in range(n)],
                [(i, j) for i in range(n) for j in range(n) if i < j],
                layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C + LEFT * 2.9)

        seed(5)
        strip_graph(g1, get_random_spanning_tree(g1.vertices, g1.edges)) 
        orient_from_root(g1, 2)
        add_edge_numbering(g1)

        seed(13)
        strip_graph(g2, get_random_spanning_tree(g2.vertices, g2.edges)) 
        orient_from_root(g2, 5)
        add_edge_numbering(g2)

        self.play(Write(g1), Write(g2))

        self.play(FadeOut(g1), FadeOut(g2))

        OFFSET = LEFT * 2.9
        OFFSET2 = RIGHT

        text_1 = Tex(r"$\tau(n)$").shift(DOWN * DOWN_C + OFFSET2)
        text_2 = Tex(r"$= \kappa(n)$").next_to(text_1, RIGHT)
        text_3d = Tex(r"$\cdot$").next_to(text_2, RIGHT)
        text_3 = Tex(r"$n$").next_to(text_3d, RIGHT)
        text_4d = Tex(r"$\cdot$").next_to(text_3, RIGHT)
        text_4 = Tex(r"$(n-1)!$").next_to(text_4d, RIGHT)

        n = 6
        g3 = Graph([i for i in range(n)],
                [(i, j) for i in range(n) for j in range(n) if i < j],
                layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C + OFFSET)

        g_under = Graph([i for i in range(n)],
                [(i, j) for i in range(n) for j in range(n) if i < j],
                layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C + OFFSET)
        for e in g_under.edges:
            g_under.edges[e].set_color(HIDDEN_COLOR)
        for v in g_under.vertices:
            g_under.vertices[v].set_color(HIDDEN_COLOR)

        seed(31)
        previous_edges = g3.edges
        edges = get_random_spanning_tree(g3.vertices, g3.edges)

        prev_edges = g3.edges
        self.play(Write(g3), Write(text_1))

        self.add(g_under)
        self.add(g3)

        seed(43)

        m = 5
        for i in range(m):
            if i == m - 1:
                edges = [(0, 1), (0, 5), (1, 4), (3, 4), (2, 3)]
                edges = [((a, b) if (a, b) in g3.edges else (b, a)) for a, b in edges]
            else:
                edges = get_random_spanning_tree(g3.vertices, g3.edges)

            self.play(
                *[g3.edges[e].animate.set_opacity(1) for e in edges if e not in prev_edges],
                *[g3.edges[e].animate.set_opacity(0) for e in prev_edges if e not in edges],
            )

            prev_edges = edges

        strip_graph(g3, edges)

        self.play(Write(text_2))
        self.play(FadeOut(g_under))

        g_prev = None
        prev_edges = []
        for root in range(n):
            g_curr = Graph([i for i in range(n)],
                    [(i, j) for i in range(n) for j in range(n) if i < j],
                    layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C + OFFSET)

            strip_graph(g_curr, edges)

            eee = orient_from_root(g_curr, root)

            def unfuk(v, w, g):
                return g.edges[(v, w) if (v, w) in g.edges else (w, v)]

            self.remove(g_prev)
            self.add(g_curr)

            self.play(
                *[FadeIn(unfuk(*e, g_curr)) for e in eee if e not in prev_edges],
                *[FadeOut(unfuk(*e, g_prev)) for e in prev_edges if e not in eee],
                *([] if g_prev is None else [g_prev.vertices[root - 1].animate.set_color(WHITE)]),
                g_curr.vertices[root].animate.set_color(HIGHLIGHT_COLOR),
                run_time=0.7,
            )

            if g_prev is not None:
                self.remove(g_prev.vertices[root - 1])

            prev_edges = eee
            g_prev = g_curr

        prev_numbers = add_edge_numbering(g_curr, return_only=True)

        self.play(Write(text_3), Write(text_3d))
        self.play(*[Write(n) for n in prev_numbers])

        count = len(list(permutations([i + 1 for i in range(len(g_curr.edges))])))
        for i, p in enumerate(permutations([i + 1 for i in range(len(g_curr.edges))])):
            start = [0.5, 0.5, 0.4, 0.3, 0.15, 0.08]
            waits = start + [0.004] * count * 2

            numbers = add_edge_numbering(g_curr, numbers=p, return_only=True)
            self.play(*[Transform(a, b) for a, b in zip(prev_numbers, numbers)], run_time=waits[i])

        self.play(Write(text_4), Write(text_4d))

        delta = UP * 2.4 + LEFT * 0.9
        self.play(
            *[FadeOut(n) for n in prev_numbers],
            FadeOut(g_curr),
            FadeOut(g3),
            FadeOut(text_1),
            FadeOut(text_2),
            FadeOut(text_3),
            FadeOut(text_3d),
            FadeOut(text_4),
            FadeOut(text_4d),
        )

        n = 7
        g4 = Graph([i for i in range(n)],
                [],
                layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C)

        for v in g4.vertices:
            g4.vertices[v].set_color(HIGHLIGHT_COLOR)

        self.play(Write(g4))

        edges = []
        numbers = []

        operation_list = [
            (0, 1, True),
            (4, 3, False),
            (3, 5, False),
        ]

        def _add_edge(v, w, s, i=[0]):
            edges.append(create_oriented_edge(g4, v, w))
            numbers.append(create_edge_number(g4, v, w, i[-1], side=s))

            i[-1] += 1
            self.play(
                    Write(edges[-1]),
                    Write(numbers[-1]),
                    g4.vertices[v].animate.set_color(WHITE),
                    )

        _add_edge(*operation_list[0])
        _add_edge(*operation_list[1])
        _add_edge(*operation_list[2])

        OFFSET += LEFT * 0.7
        self.play(
                g4.animate.shift(OFFSET),
                *[n.animate.shift(OFFSET) for n in numbers],
                *[e.animate.shift(OFFSET) for e in edges],
                )

        parts = [
            r"\small $1.\ $start in component's root\\ " + "\n",
            r"\small $2.\ $can't be in a single component\\ "
        ]

        l = Tex(*parts)
        l.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3.0 + DOWN * 1)

        self.play(Write(l[0]))

        edge = create_oriented_edge(g4, 3, 1)
        edge.set_color(RED)

        self.bring_to_back(edge)
        self.play(Write(edge))
        self.play(FadeOut(edge))

        self.play(Write(l[1]))

        edge = create_oriented_edge(g4, 5, 4)
        edge.set_color(RED)

        self.bring_to_back(edge)
        self.play(
                Write(edge),
                g4.vertices[5].animate.set_color(WHITE),
                )
        self.play(
                FadeOut(edge),
                g4.vertices[5].animate.set_color(HIGHLIGHT_COLOR),
                )

        self.play(
                l[0].animate.shift(UP * 1.6),
                l[1].animate.shift(UP * 1.6),
                )


        parts2 = [
            r"\small end:\\ " + "\n",
            r"\small start:\\ ",
        ]

        parts3 = [
            r"\small $n$\\ " + "\n",
            r"\small $n - k - 1$\\ ",
        ]


        l2 = Tex(*parts2)
        l2.arrange(DOWN, aligned_edge=RIGHT).shift(RIGHT * 1.8 + DOWN * 1.7)

        l3 = Tex(*parts3)
        l3.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3.5 + DOWN * 1.7)
        l3[0].set_color(YELLOW)
        l3[1].set_color(YELLOW)

        l3[0].shift(DOWN * 0.07)
        l3[1].shift(DOWN * 0.07)

        self.play(Write(l2[0]))
        self.play(Write(l3[0]))
        self.play(Write(l2[1]))
        self.play(Write(l3[1]))

        self.play(FadeOut(l2))

        lp = Tex(r"\small$($")
        rp = Tex(r"\small$)$")
        cd = Tex(r"\small$\cdot$")


        l3[0].shift(LEFT * 0.75 + DOWN * 0.3)

        delta = (l3[0].get_center() - l3[1][0].get_center())[1] * UP

        l3[1].shift(delta)

        lp.next_to(l3[1], LEFT).shift(RIGHT * 0.2)
        rp.next_to(l3[1], RIGHT).shift(LEFT * 0.2)
        cd.next_to(l3[0], RIGHT).shift(LEFT * 0.1)

        l3[1].shift(-delta)
        l3[0].shift(RIGHT * 0.75 + UP * 0.3)

        def shiftchangecolor(mob, color, delta):
            mob.set_color(WHITE)
            mob.shift(delta)

            return mob

        self.play(
            LaggedStart(
                AnimationGroup(
                    ApplyFunction(lambda x: shiftchangecolor(x, WHITE, LEFT * 0.75 + DOWN * 0.3), l3[0]),
                    ApplyFunction(lambda x: shiftchangecolor(x, WHITE, delta), l3[1]),
                ),
                AnimationGroup(
                    Write(lp),
                    Write(rp),
                    Write(cd),
                ),
                lag_ratio=0.7
            )
        )

        p = Tex(r"$$\prod_{k=0}^{n-2}$$")
        p.next_to(l3[0], LEFT).shift(UP * 0.08 + RIGHT * 0.13)
        self.play(Write(p))

        nto = Tex(r"\small $n^{n - 1}$")
        nto.move_to((-nto[0].get_center() + l3[0][0].get_center())).shift(LEFT * 0.9).shift(UP * 0.12)

        self.play(
            LaggedStart(
                AnimationGroup(
                    p.animate.shift(RIGHT * 0.65),
                    FadeOut(cd),
                    Transform(l3[0], nto)
                ),
            )
        )

        fac = Tex(r"\small $(n - 1)!$")
        fac.move_to(p).shift(RIGHT * 0.5 + DOWN * 0.072)

        combine = VMobject()
        combine.add(p)
        combine.add(l3[1])
        combine.add(lp)
        combine.add(rp)

        self.play(
            Transform(combine, fac)
        )

        combine2 = VMobject()
        combine2.add(combine)
        combine2.add(nto)

        eq = Tex(r"\small $=$").shift(DOWN * 0.8)

        self.remove(nto)
        self.remove(l3[0])

        text_2 = Tex(r"$\kappa(n)$")
        text_3d = Tex(r"$\cdot$").next_to(text_2, RIGHT)
        text_3 = Tex(r"$n$").next_to(text_3d, RIGHT)
        text_4d = Tex(r"$\cdot$").next_to(text_3, RIGHT)
        text_4 = Tex(r"$(n-1)!$").next_to(text_4d, RIGHT)

        left = VMobject()
        left.add(text_2)
        left.add(text_3d)
        left.add(text_3)
        left.add(text_4d)
        left.add(text_4)
        left.next_to(eq, LEFT)

        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(l),
                    *[FadeOut(e) for e in edges],
                    *[FadeOut(e) for e in numbers],
                    FadeOut(g4),
                ),
                AnimationGroup(
                    combine2.animate.next_to(eq, RIGHT),
                ),
                AnimationGroup(
                    Write(left),
                ),
                AnimationGroup(
                    Write(eq),
                ),
                lag_ratio=0.4,
            ),
        )

        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(combine),

                    FadeOut(text_4d),
                    FadeOut(text_4),
                ),
                AnimationGroup(
                    text_2.animate.shift(RIGHT * 2.13),
                    text_3d.animate.shift(RIGHT * 2.13),
                    text_3.animate.shift(RIGHT * 2.13),
                ),
                lag_ratio=0.3,
            ),
        )

        two = Tex("\small $^2$")
        two.move_to(nto[0][3])

        self.play(
            LaggedStart(
                AnimationGroup(
                    Transform(nto[0][3], two),

                    FadeOut(text_3d),
                    FadeOut(text_3),
                ),
                AnimationGroup(
                    text_2.animate.shift(RIGHT * 0.83),
                ),
                lag_ratio=0.3,
            ),
        )

        o = Mobject()
        o.add(text_2)
        o.add(nto)

        self.play(Circumscribe(o, color=WHITE))
