from manim import *
from typing import *



def get_non_full_vertices(graph: Graph):
    """Return all vertices of a graph (having '0' as root) that don't have 2 children."""
    vertices = []

    for v in graph.vertices:

        count = 0
        for w, _ in graph.edges:
            if v == w:
                count += 1

        if count != 2:
            vertices += [v]

    return vertices


def generate_binary_trees(n: int):
    def _generate(n: int) -> List:
        """Generate all binary trees on n vertices.
        n = 1: [None, None]
        n = 2: [[None, None], None] and [None, [None, None]]
        n = 3: ..."""

        if n == 0:
            return None

        else:
            previous_trees = []
            trees = []

            for i in range(n):
                previous_trees.append(_generate(i))

            for i in range(n):
                for l1 in (previous_trees[i] or [None]):
                    for l2 in (previous_trees[n - i - 1] or [None]):
                        trees.append([l1, l2])

            return trees

    return [generate_binary_tree(tree) for tree in _generate(n)]


def generate_binary_tree(graph) -> VMobject:
    """Generate a binary tree from nested parentheses.
    Sample input: [None, [None, None]] (generating a 2-vertex binary tree)."""

    vertices = [""]
    edges = []

    def _generate(g, v):
        """Populate vertices and edges. Vertices to be deleted contain the 'B' symbol."""
        if g == [None, None]:
            return

        for i in range(2):
            s = "l" if i == 0 else "r"

            if g[i] != None:
                vertices.append(v + s)
                edges.append((v, vertices[-1]))

                _generate(g[i], vertices[-1])
            else:
                vertices.append(v + s + "B")
                edges.append((v, vertices[-1]))

    _generate(graph, "")

    g = Graph(
        vertices,
        edges,
        layout="tree",
        root_vertex="",
        layout_config={"vertex_spacing": (1.15, 1)},
        vertex_type=lambda: Dot().scale(3),
    )

    for v in list(g.vertices):
        if "B" in v:
            g.remove_vertices(v)

    return g


def star_name(i):
    return f"star_{i}"

def add_stars(graph) -> List[str]:
    """Add stars to the graph, returning their names. It is assumed that '' is the root."""

    def create_star(v, number, direction, direction_scale=0.26, color=BLUE):
        """Create star from the vertex in the given direction (LEFT/RIGHT)."""

        def create_star_object():
            star_scale = 0.2

            star = Star(5, density=1.5, color=color, fill_opacity=1).scale(star_scale)
            text = Tex(str(number), color=BLACK).scale(2.5 * star_scale).move_to(star).shift(DOWN * star_scale * 0.12)

            return VGroup(star, text)

        graph.add_vertices(
            star_name(number),
            positions={
                star_name(number): graph.vertices[v].get_center()
                + (DOWN * 1.9 + direction) * direction_scale
            },
            vertex_type=create_star_object,
        )[0]

        graph.add_edges(
            ((v, star_name(number))),
            edge_type=lambda *args, **kwargs: Line(*args, color=color, **kwargs),
        )

    count = 0

    # add stars sorted from left to right (so by the x, y coordinate of parent)
    for v in sorted(get_non_full_vertices(graph), key = lambda v: (graph.vertices[v].get_center()[0], graph.vertices[v].get_center()[1])):
        descendants = [x for (w, x) in graph.edges if v == w]

        # add both stars
        if len(descendants) == 0:
            create_star(v, count + 1, LEFT)
            create_star(v, count + 2, RIGHT)
            count += 2

        # add one star
        else:
            d = descendants[0]

            if d[-1] == "l":
                create_star(v, count + 1, LEFT)
            else:
                create_star(v, count + 1, RIGHT)

            count += 1

    return [star_name(i + 1) for i in range(count)]


def AnimateStars(graph, star_names) -> List[Animation]:
    """Return a list of animations of creating all of the stars of a graph."""
    animations = []

    for (u, v) in graph.edges:
        if v in star_names:
            animations.append(
                (
                    graph.vertices[v].get_center()[0],
                    AnimationGroup(
                        FadeIn(graph.edges[(u, v)], run_time=0.4),
                        FadeIn(graph.vertices[v], run_time=0.4),
                        Flash(
                            graph.vertices[v],
                            color=graph.vertices[v].color,
                            run_time=0.4,
                            line_length=0.05,
                            flash_radius=0.18,
                        ),
                        lag_ratio=0.3,
                    ),
                )
            )

    return [a for (_, a) in sorted(animations, key=lambda x: x[0])]


def SwapChildren(graph, v, move_distance=0.1, speed_ratio=0.75, **kwargs) -> List[Animation]:
    """Generates animations for swapping the children of a vertex."""

    def get_all_descendants(graph: Graph, vertex):
        """Return all children of a vertex, including the vertex itself."""
        stack = [vertex]
        children = []

        while len(stack) != 0:
            u = stack.pop(0)
            children.append(u)

            for v in graph.vertices:
                if v in children:
                    continue

                if (u, v) in graph.edges:
                    stack.append(v)

        return children

    def generate_swap_animations(parent, child, direction):
        """Generate the swap animations for a parent, given its child."""
        c_pos = graph.vertices[child].get_center()
        p_pos = graph.vertices[parent].get_center()

        mirror_c_pos = np.array([c_pos[0] + 2 * (p_pos[0] - c_pos[0]), c_pos[1], c_pos[2]])

        points = [
            c_pos,
            c_pos * speed_ratio + mirror_c_pos * (1 - speed_ratio),
            c_pos * (1 - speed_ratio) + mirror_c_pos * speed_ratio,
            mirror_c_pos,
        ]

        path = CubicBezier(
            points[0],
            points[1] + direction * move_distance,
            points[2] + direction * move_distance,
            points[3],
        )

        return [
            MoveAlongPath(
                graph.vertices[v],
                path.copy().shift(graph.vertices[v].get_center() - c_pos),
                **kwargs,
            )
            for v in get_all_descendants(graph, child)
        ]

    # find the children
    a, b = [x for (w, x) in graph.edges if v == w]

    return [
        *generate_swap_animations(v, a, UP),
        *generate_swap_animations(v, b, DOWN),
    ]
