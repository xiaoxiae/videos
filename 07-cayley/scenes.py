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

def orient_from_root(g, root):
    queue = [root]
    explored = set([root])

    buffer = 0.23
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

            v_center = g.vertices[v].get_center()
            w_center = g.vertices[w].get_center()

            center = (v_center + w_center) / 2
            delta = (v_center - w_center) / 2

            mag = (delta[0] ** 2 + delta[1] ** 2)**(1/2)
            c = (mag - buffer) / mag

            a = Arrow(center + delta * c, center - delta * c, max_tip_length_to_length_ratio=30, buff=0)

            g.edges[(v, w) if (v, w) in g.edges else (w, v)].become(a)

def add_edge_numbering(graph, scale=0.8, shift_coefficient=0.3):

    numbers = [i + 1 for i in range(len(graph.edges))]
    shuffle(numbers)

    graph.edge_numbers = {}
    for i, (v, w) in enumerate(graph.edges):
        number = Tex(str(numbers[i])).scale(scale)

        v_center = graph.vertices[v].get_center()
        w_center = graph.vertices[w].get_center()

        center = (v_center + w_center) / 2
        delta = (v_center - w_center)
        delta /= (delta[0] ** 2 + delta[1] ** 2)**(1/2)

        # rotate 90 degrees
        delta[0], delta[1] = delta[1], -delta[0]

        number.move_to(center).shift(delta * shift_coefficient)
        graph.add(number)
        graph.edge_numbers[(v, w)] = number


class Proof(Scene):
    @fade
    def construct(self):
        title = Tex("\Large Double counting")

        #self.play(Write(title))
        #self.play(title.animate.shift(UP * 1.2))

        text = Tex("\parbox{23em}{The number of ","oriented trees"," on ","$n$"," vertices that have a ","root"," and some ","numbering of edges"," – ",r"$\tau(n)$",".}")
        highlightText(text)

        text.next_to(title, DOWN * 2)

        #self.play(Write(text))

        #self.play(FadeOut(title))
        #self.play(text.animate.align_on_border(UP))

        l = Line(LEFT * 8, RIGHT * 8).next_to(text, DOWN).shift(DOWN * 0.15)
        #self.play(Write(l))

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

        #self.play(Write(g1), Write(g2))
        #self.play(Circumscribe(g1.vertices[2], Circle, color=HIGHLIGHT_COLOR), Circumscribe(g2.vertices[5], Circle, color=HIGHLIGHT_COLOR))

        #self.play(FadeOut(g1), FadeOut(g2))

        n = 6
        g3 = Graph([i for i in range(n)],
                [(i, j) for i in range(n) for j in range(n) if i < j],
                layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C)

        seed(31)
        edges = get_random_spanning_tree(g3.vertices, g3.edges)
        strip_graph(g3, edges)

        self.play(Write(g3))

        g_prev = None
        for root in range(n):
            g_curr = Graph([i for i in range(n)],
                    [(i, j) for i in range(n) for j in range(n) if i < j],
                    layout="circular", layout_scale=0.6).scale(GRAPH_SCALE).shift(DOWN * DOWN_C)

            strip_graph(g_curr, edges)
            orient_from_root(g_curr, root)

            # TODO: smoother
            self.play(
                FadeIn(g_curr),
                *([] if g_prev is None else [FadeOut(g_prev)]),
                run_time=0.5,
            )

            g_prev = g_curr

