from utilities import *

GRAPH_SCALE = 3.6

HIDDEN_COLOR = DARKER_GRAY
HIGHLIGHT_COLOR = YELLOW


def neighbours(v, E):
    """Return the neighbours of v in E."""
    t = []
    for e in E:
        if v in e:
            t.append(e)
    return [a for a in edgesToVertices(t) if a != v]


def components(V, E):
    """Calculate the number of components of the graph."""
    total = 0
    explored = set()
    for v in V:
        if v in explored:
            continue

        queue = [v]
        explored.add(v)
        total += 1
        while len(queue) != 0:
            v = queue.pop(0)

            for w in neighbours(v, E):
                if w not in explored:
                    explored.add(w)
                    queue.append(w)

    return total


def tutte(V, E):
    """Return the Tutte polynomial of the graph."""
    sum_parts = []

    c_e = components(V, E)
    for k in range(len(E)+1):

        for F in combinations(E, k):
            c_f = components(V, F)

            r_e = len(V) - c_e
            r_f = len(V) - c_f
            n_f = len(F) - r_f

            f = (lambda r_e, r_f, n_f: (lambda x, y: (x - 1) ** (r_e - r_f) * (y - 1) ** n_f))(r_e, r_f, n_f)
            sum_parts.append(f)

    return lambda x, y: sum(v(x, y) for v in sum_parts)


class Intro(ThreeDScene):
    def construct(self):
        n = 4
        resolution = 32

        g = parse_graph(
            """
1 2 <14.955583178269885, 12.492887677476215> <16.3169159925859, 18.518980248079334>
3 2 <10.488387335146333, 16.6269826120094> <16.3169159925859, 18.518980248079334>
1 3 <14.955583178269885, 12.492887677476215> <10.488387335146333, 16.6269826120094>
1 4 <14.955583178269885, 12.492887677476215> <15.748659587666504, 6.403292853126976>
2 5 <16.3169159925859, 18.518980248079334> <15.588570469025248, 24.63764356262158>
2 6 <16.3169159925859, 18.518980248079334> <22.433423744442276, 19.229414535025658>
                """,
            s=0.12,
            t=0.12,
        ).scale(GRAPH_SCALE)

        f = tutte(g.vertices, g.edges)

        axes = ThreeDAxes(
            x_length=4.5,
            y_length=4.5,
            z_length=4.5,
        )

        x_start, x_end = -2.5, 2.5
        y_start, y_end = -2.5, 2.5

        surface = Surface(
                lambda x, y: axes.c2p(x, y, f(x, y)),
            u_range=[x_start, x_end],
            v_range=[y_start, y_end],
            resolution=resolution,
        )
        surface.set_fill_by_checkerboard(LIGHT_GRAY, DARK_GRAY, opacity=0.5)
        surface.set_style(fill_opacity=1)

        self.set_camera_orientation(theta=120 * DEGREES, phi=75 * DEGREES)

        self.renderer.camera.light_source.move_to(3*IN)

        axes.scale(1.5)
        surface.scale(1.5)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(Write(axes))
        self.play(Write(surface), run_time=1)

        self.wait(3)


def get_graph_background(g, vertex_scale=1.7, edge_scale=1.4, color=DARKER_GRAY):
    objects = []

    for u, v in g.edges:
        mid = g.vertices[u].get_center() / 2 + g.vertices[v].get_center() / 2
        x, y, _ = g.vertices[u].get_center() - g.vertices[v].get_center()
        angle = atan2(y, x)

        a = g.vertices[u].copy().scale(vertex_scale)
        b = g.vertices[v].copy().scale(vertex_scale)
        rect = Rectangle(height = a.height * edge_scale, width = 2 * (x ** 2 + y ** 2) ** (1/2)).move_to(mid).rotate(angle).scale(0.5)

        objects += [a, b, rect]

    u = Union(*objects).set_fill(color, 1).set_stroke(color)
    u.set_z_index(-2)  # TODO: hack
    return u


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


class Intro(Scene):
    def construct(self):
        g = parse_graph(
            """
12 14 <6.603275758877981, 0.22200042158063704> <10.542340602049554, 5.0486231945767255>
2 12 <6.603275758877981, 0.22200042158063704> <10.542340602049554, 5.0486231945767255>
1 2 <6.603275758877981, 0.22200042158063704> <10.542340602049554, 5.0486231945767255>
1 3 <6.603275758877981, 0.22200042158063704> <0.8751494485961517, 2.8894436903527834>
2 4 <10.542340602049554, 5.0486231945767255> <8.316429210045438, 9.49508367004807>
1 5 <6.603275758877981, 0.22200042158063704> <5.320620964273308, -6.074692063436867>
3 6 <0.8751494485961517, 2.8894436903527834> <-4.8178524679438075, 0.2426494079303798>
6 7 <-4.8178524679438075, 0.2426494079303798> <-10.765611934215096, -1.6359342354516002>
7 8 <-10.765611934215096, -1.6359342354516002> <-12.201191317109153, 3.5640128560657254>
3 9 <0.8751494485961517, 2.8894436903527834> <-0.22868399658749183, 8.989711296016043>
6 10 <-4.8178524679438075, 0.2426494079303798> <-6.36641219483813, -5.744685968682711>
1 12 <6.603275758877981, 0.22200042158063704> <11.495122080884329, -4.388454491563957>
7 10 <-10.765611934215096, -1.6359342354516002> <-6.36641219483813, -5.744685968682711>
5 12 <5.320620964273308, -6.074692063436867> <11.495122080884329, -4.388454491563957>
3 11 <0.8751494485961517, 2.8894436903527834> <0.4357598447196547, -3.4516057795938906>
2 14 <10.542340602049554, 5.0486231945767255> <16.235759844719652, 1.2483942204061114>
                """,
            s=0.09,
            t=-0.09,
            scale=GRAPH_SCALE,
        )

        self.play(Write(g))

        self.play(*[g.edges[v].animate.set_color(BLACK) for v in g.edges])
        self.play(*[g.edges[v].animate.set_color(WHITE) for v in g.edges], *[g.vertices[v].animate.set_color(BLACK) for v in g.vertices])
        self.play(*[g.vertices[v].animate.set_color(WHITE) for v in g.vertices])

        vertices = Tex(r"\small $V$... set of vertices").align_on_border(DOWN + LEFT).shift((RIGHT + UP) * 0.75 + UP * 0.65)
        edges = Tex(r"\small $E$... set of edges").next_to(vertices, DOWN).align_to(vertices, LEFT)

        self.play(g.animate.shift(RIGHT * 0.5))

        self.play(Write(vertices), run_time=1)
        self.play(Write(edges), run_time=1)

        self.play(
                FadeOut(g.edges[(1, 3)]),
                FadeOut(g.edges[(3, 6)]),
                )

        new_g = g.copy()
        del new_g.edges[(1, 3)]
        del new_g.edges[(3, 6)]
        u = get_graph_background(new_g)
        self.play(FadeIn(u))

        upshift = 0.4
        components = Tex(r"\small $c(G)$... number of components").next_to(edges, DOWN).align_to(vertices, LEFT).shift(UP * upshift * 1.2)

        def update_edges(obj, u, v):
            obj.put_start_and_end_on(g[u].get_center(), g[v].get_center())

        for e in g.edges:
            g.edges[e].add_updater((lambda arg: (lambda x: update_edges(x, *arg)))(e))

        self.play(FadeOut(u))

        self.play(
            LaggedStart(
                AnimationGroup(
                    vertices.animate.shift(UP * upshift),


                    g.vertices[8].animate.shift(UP * upshift * 1.4 + LEFT * 0.6),
                    g.vertices[7].animate.shift(UP * upshift / 1.6),
                    g.vertices[6].animate.shift(UP * upshift / 1.6),

                    g.vertices[9].animate.shift(UP * upshift * 2.3),
                    g.vertices[3].animate.shift(UP * upshift * 1.4),
                    g.vertices[11].animate.shift(UP * upshift / 2.2),
                    edges.animate.shift(UP * upshift),
                ),
                AnimationGroup(Write(components)),
                lag_ratio=0.4,
            ),
            run_time=1.9
        )

        self.play(
                FadeIn(g.edges[(1, 3)]),
                FadeIn(g.edges[(3, 6)]),
                )
        
        st = get_random_spanning_tree(g.vertices, g.edges)

        self.play(
                *[g.edges[e].animate.set_color(HIDDEN_COLOR) for e in g.edges if e not in st],
                *[Flash(g.edges[e], color=HIDDEN_COLOR) for e in g.edges if e not in st]
                )

