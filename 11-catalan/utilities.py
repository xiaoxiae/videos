from __future__ import annotations

from manim import *
from typing import *
from random import seed
from itertools import permutations, combinations
import sympy


class StarUtilities:
    STAR_COLOR = GREEN
    STAR_N = 8
    STAR_SCALE = 0.15
    STAR_OFFSET = 0.26

    @classmethod
    def get_star_name(cls, i):
        return f"star_{i}"

    @classmethod
    def is_star_name(cls, s):
        return "star" in s

    @classmethod
    def get_star_index(cls, s):
        return int(s[len("star_"):])

    @classmethod
    def get_highest_star(cls, graph):
        max_index = 0
        max_name = None
        for v in graph.vertices:
            if cls.is_star_name(v):
                if cls.get_star_index(v) > max_index:
                    max_index = cls.get_star_index(v)
                    max_name = v
        return max_name


    @classmethod
    def create_star_object(cls, number) -> VMobject:
        # this MUST be an odd number, else the rotation won't work
        star = Star(cls.STAR_N, density=1.5, color=cls.STAR_COLOR, fill_opacity=1).scale(cls.STAR_SCALE)
        text = Tex(str(number), color=BLACK).scale(3 * cls.STAR_SCALE).move_to(star)

        return VGroup(star, text)

    @classmethod
    def get_star_position(cls, graph, v, direction):
        """Get the star position, relative to the given vertex in a graph."""
        return graph.vertices[v].get_center() + (DOWN * 1.9 + direction) * cls.STAR_OFFSET

    @classmethod
    def attach_star_to_vertex(cls, graph, v, number, direction):
        """Create star from the vertex in the given direction (LEFT/RIGHT)."""

        vertex = graph.add_vertices(
            cls.get_star_name(number),
            positions={
                cls.get_star_name(number): cls.get_star_position(graph, v, direction)
            },
            vertex_type=lambda: cls.create_star_object(number),
        )[0]

        graph.add_edges(
            ((v, cls.get_star_name(number))),
            edge_type=lambda *args, **kwargs: Line(*args, color=cls.STAR_COLOR, **kwargs),
        )


    @classmethod
    def add_stars_to_graph(cls, graph: BinaryTree):
        """Add stars to a binary tree. It is assumed that '' is the root."""

        count = 0

        # add stars sorted from left to right (so by the x, y coordinate of parent)
        for v in sorted(graph.get_non_full_vertices(), key = lambda v: (graph.vertices[v].get_center()[0], graph.vertices[v].get_center()[1])):
            descendants = [x for (w, x) in graph.edges if v == w]

            # add both stars
            if len(descendants) == 0:
                cls.attach_star_to_vertex(graph, v, count + 1, LEFT)
                cls.attach_star_to_vertex(graph, v, count + 2, RIGHT)
                count += 2

            # add one star
            else:
                d = descendants[0]

                if d[-1] == "l":
                    cls.attach_star_to_vertex(graph, v, count + 1, LEFT)
                else:
                    cls.attach_star_to_vertex(graph, v, count + 1, RIGHT)

                count += 1

        return [cls.get_star_name(i + 1) for i in range(count)]


def ChangeStars(graph, permutation: int) -> Animation:
    """Return the animation of changing the permutation on the stars."""
    n = (len(graph.vertices) + 1) // 2
    p = list(permutations(range(1, n + 1)))[permutation]  # computers are fast

    animations = []

    for vertex in graph.vertices:
        if StarUtilities.is_star_name(vertex):
            star = graph.vertices[vertex]

            new_index = p[StarUtilities.get_star_index(vertex) - 1]

            if StarUtilities.get_star_index(vertex) != new_index:
                new_star = StarUtilities.create_star_object(new_index)
                new_star[1].move_to(star[0])

                animations += [
                    star[0].animate(rate_func=there_and_back).scale(0.75),
                    star[1].animate.become(new_star[1]),
                ]

    return AnimationGroup(*animations)

def CreateStars(graph) -> Animation:
    """Return an animation of creating all of the stars of a graph."""
    animations = []

    for (u, v) in graph.edges:
        if StarUtilities.is_star_name(v):
            animations.append(
                (
                    graph.vertices[v].get_center()[0],
                    AnimationGroup(
                        FadeIn(graph.edges[(u, v)], run_time=0.4),
                        FadeIn(graph.vertices[v], run_time=0.4),
                        Flash(
                            graph.vertices[v],
                            color=graph.edges[(u, v)].color,
                            run_time=0.4,
                            line_length=0.05,
                            flash_radius=0.18,
                        ),
                        lag_ratio=0.3,
                    ),
                )
            )

    return AnimationGroup(*[a for (_, a) in sorted(animations, key=lambda x: x[0])], lag_ratio=0.1)


def RemoveHighestStar(graph) -> Animation:
    """Return an animation of removing the star with the highest number (along with its vertex) from the graph.
    We're assuming that we're not removing the very last vertex."""

    max_name = StarUtilities.get_highest_star(graph)

    max_name_parent = graph.get_parent(max_name)
    max_parent_squared = graph.get_parent(max_name_parent)
    children = graph.get_children(max_name_parent)

    # if the star's parent contains a non'star child
    if not StarUtilities.is_star_name(children[0]) or not StarUtilities.is_star_name(children[1]):
        non_star_child = children[0] if not StarUtilities.is_star_name(children[0]) else children[1]

        max_name_parent_vertex = graph.vertices[max_name_parent]
        removed = graph.remove_vertices(max_name_parent)
        removed += graph.remove_vertices(max_name)

        non_star_child_descendants = graph.get_all_descendants(non_star_child)

        animations = []

        # if the parent also has a parent
        if max_parent_squared is not None:
            edge = graph.add_edges((max_parent_squared, non_star_child))[0]
            edge.set_opacity(0)

            animations += [edge.animate.set_opacity(1)]

        return [
            *[FadeOut(r, run_time=0.5) for r in removed],
            *[graph.vertices[v].animate.shift(max_name_parent_vertex.get_center() - graph.vertices[non_star_child].get_center()) for v in non_star_child_descendants],
        ] + animations

    else:
        other_child = children[0] if max_name != children[0] else children[1]

        removed = graph.remove_vertices(max_name_parent)
        removed += graph.remove_vertices(max_name)

        edge = graph.add_edges((max_parent_squared, other_child))[0]
        edge.set_color(StarUtilities.STAR_COLOR)
        edge.set_opacity(0)

        return [
            *[FadeOut(r, run_time=0.5) for r in removed],
            graph.vertices[other_child].animate.move_to(StarUtilities.get_star_position(graph, max_parent_squared, LEFT if max_parent_squared[-1] == "l" else RIGHT)),
            edge.animate.set_opacity(1),
        ]


class LinedPolygon(VMobject):

    @classmethod
    def generate_triangulated_polygons(cls, n: int) -> List[LinedPolygon]:
        """Generate all possible triangulated polygons on n vertices.
        Runs reasonably quickly for <= 10 vertices (~a minute)."""
        # computers are fast
        edges = list(combinations(range(n), r=2))

        # remove adjacent edges
        edges = [e for e in edges if abs(e[0] - e[1]) != 1 and abs(e[0] - e[1]) != n - 1]

        def _is_subset_intesecting(subset) -> bool:
            # check for intersections
            for i in range(len(subset)):
                for j in range(i + 1, len(subset)):
                    e1 = subset[i]
                    e2 = subset[j]

                    # if they share a vertex, they don't intersect
                    if len(set(e1 + e2)) != len(e1) + len(e2):
                        continue

                    p1, p2 = e1
                    p3, p4 = e2

                    if p1 < p3 < p2 and p3 < p2 < p4:
                        return True

            return False

        polygons = []

        for subset in combinations(edges, r = n - 3):
            if not _is_subset_intesecting(subset):
                polygons.append(LinedPolygon(n, subset))

        return polygons


    def __init__(self, n, edges):
        super().__init__()

        polygon = RegularPolygon(n, color=WHITE)
        vertices = polygon.get_vertices()

        self.add(polygon)

        for u, v in edges:
            self.add(Line(start=vertices[u], end=vertices[v]))


class DyckPath(VMobject):

    def __init__(self, delta: List[int], labels=False, spacing=0.5):
        super().__init__()

        vertices = list(range(len(delta) + 1))
        edges = [(i, i + 1) for i in vertices[:-1]]

        layout = {}

        pos = ORIGIN
        min_x, max_x = 0, 0
        min_y, max_y = 0, 0
        for i, (v, d) in enumerate(zip(vertices, [0] + delta)):
            if d == 1:
                pos = np.array(pos) + (RIGHT + UP) * spacing
            elif d == -1:
                pos = np.array(pos) +(RIGHT + DOWN) * spacing

            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])

            layout[v] = np.array(pos)

        for v in layout:
            layout[v][0] -= (max_x + min_x) / 2
            layout[v][1] -= (max_y + min_y) / 2

        g = Graph(vertices, edges, layout=layout)
        self.add(g)

        bottom_line = DashedLine(
            g.vertices[0].get_center(),
            g.vertices[len(g.vertices) - 1].get_center(),
            dashed_ratio=0.25,
            color=GRAY,
        )

        self.add(bottom_line)
        bottom_line.set_z_index(-1)

        if labels:
            for v, d in zip(vertices, delta):
                color = RED if d == -1 else GREEN
                label = Tex(str(d), color=color).scale(0.5).next_to(g.vertices[v], UP, buff=0.15)
                self.add(label)





class BinaryTree(Graph):
    def get_parent(self, v) -> str:
        """Return the parent of a vertex (given that it's not the root), else return None."""
        for x, y in self.edges:
            if v == y:
                return x

    def get_children(self, v) -> List[str]:
        """Return the parent of a vertex (given that it's not the leaf), else return []."""
        children = []
        for x, y in self.edges:
            if v == x:
                children.append(y)
        return children

    def get_all_descendants(self, v) -> List[str]:
        """Return all children of a vertex, including the vertex itself."""
        stack = [v]
        children = []

        while len(stack) != 0:
            u = stack.pop(0)
            children.append(u)

            for v in self.vertices:
                if v in children:
                    continue

                if (u, v) in self.edges:
                    stack.append(v)

        return children


    def get_non_full_vertices(self) -> List[str]:
        """Return all vertices of a graph (having '0' as root) that don't have 2 children."""
        vertices = []

        for v in self.vertices:

            count = 0
            for w, _ in self.edges:
                if v == w:
                    count += 1

            if count != 2:
                vertices += [v]

        return vertices

    @classmethod
    def _generate_parentheses(cls, n: int) -> Optional[List]:
        """Generate all nested parentheses representing binary trees on n vertices.
        n = 1: [None, None]
        n = 2: [[None, None], None] and [None, [None, None]]
        n = 3: ..."""

        if n == 0:
            return None

        else:
            previous_trees = []
            trees = []

            for i in range(n):
                previous_trees.append(cls._generate_parentheses(i))

            for i in range(n):
                for l1 in (previous_trees[i] or [None]):
                    for l2 in (previous_trees[n - i - 1] or [None]):
                        trees.append([l1, l2])

            return trees

    @classmethod
    def _binary_tree_from_parentheses(cls, graph) -> VMobject:
        """Generate a binary tree from nested parentheses.
        Sample input: [None, [None, None]] (generating a 2-vertex binary tree)."""

        vertices = [""]
        edges = []

        def _populate(g, v):
            """Populate vertices and edges. Vertices to be deleted contain the 'B' symbol."""
            if g == [None, None]:
                return

            for i in range(2):
                s = "l" if i == 0 else "r"

                if g[i] != None:
                    vertices.append(v + s)
                    edges.append((v, vertices[-1]))

                    _populate(g[i], vertices[-1])
                else:
                    vertices.append(v + s + "B")
                    edges.append((v, vertices[-1]))

        _populate(graph, "")

        g = cls(
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

    @classmethod
    def generate_binary_trees(cls, n: int) -> List[BinaryTree]:
        """Generate all binary trees on n vertices."""
        return [cls._binary_tree_from_parentheses(p)
                for p in cls._generate_parentheses(n)]



def SwapChildren(graph, v, move_height=0.1, speed_ratio=0.75, **kwargs) -> List[Animation]:
    """Generates animations for swapping the children of a vertex."""

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
            points[1] + direction * move_height,
            points[2] + direction * move_height,
            points[3],
        )

        return [
            MoveAlongPath(
                graph.vertices[v],
                path.copy().shift(graph.vertices[v].get_center() - c_pos),
                **kwargs,
            )
            for v in graph.get_all_descendants(child)
        ]

    # find the children
    a, b = [x for (w, x) in graph.edges if v == w]

    # TODO: using AnimationGroup here stops updaters, I'm not sure how to prevent it
    return [
        *generate_swap_animations(v, a, UP),
        *generate_swap_animations(v, b, DOWN),
    ]
