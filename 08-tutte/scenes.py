from utilities import *

GRAPH_SCALE = 3.2

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
