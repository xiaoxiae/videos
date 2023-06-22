import numpy as np
from shapely import geometry
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
from manim import *
from typing import List, Tuple
from random import randint, seed, uniform, shuffle
import math
from copy import deepcopy
from pulp import *

import networkx as nx

LINE_STROKE = 7

BIG_OPACITY = 0.2
BIGGER_OPACITY = 0.1
MED_OPACITY = 0.5
LIGHT_ORANGE = "#ffb97e"
DARK_ORANGE = "#e46800"
BIG_COLOR = "#333333"

NORMAL_DOT_SCALE = 1.35
OPTIMUM_DOT_SCALE = 1.8


def CreateSR(obj, *args, **kwargs):
    return SurroundingRectangle(obj, *args, color=BLACK, stroke_width=0, fill_opacity=1, corner_radius=0.1, **kwargs)\
                    .set_z_index(obj.get_z_index() - 0.000001).set_opacity(0.8)

def GetTSPIllustration(fade=False):
    seed(0xDEADBEEF3)

    n = 20
    G = nx.complete_graph(n)

    points = []
    for i in range(n):
        max_distance = 0
        max_point = None

        for _ in range(10):
            local_min_dist = float('inf')
            point = np.array((uniform(-3, 3), uniform(-3, 3), 0))

            for other in points:
                local_min_dist = min(
                    local_min_dist,
                    np.linalg.norm(point - other),
                )

            if local_min_dist > max_distance:
                max_distance = local_min_dist
                max_point = point

        points.append(max_point)

    lt = {i: p for i, p in enumerate(points)}

    for u, v in G.edges:
        G[u][v]['weight'] = np.linalg.norm(lt[u] - lt[v])

    path = nx.approximation.traveling_salesman_problem(G)

    vertices = G.nodes
    edges = G.edges
    G = Graph(vertices, edges, layout=lt)

    for v in G.vertices:
        G.vertices[v].scale(2)

    for (u, v) in G.edges:
        for i in range(len(path) - 1):
            if (path[i] == u and path[i + 1] == v) or (path[i] == v and path[i + 1] == u):
                G.edges[(u, v)].set_z_index(10)

                if fade:
                    G.edges[(u, v)].set_color(DARKER_GRAY)
                break
        else:
            if uniform(0, 1) < 0.8:
                G.edges[(u, v)].set_opacity(0)
            else:
                G.edges[(u, v)].set_color(DARKER_GRAY)

                if fade:
                    G.edges[(u, v)].set_opacity(0.5)

    if fade:
        for v in G.vertices:
            G.vertices[v].set_color(DARKER_GRAY)


    return G


def CreateMeaning(obj, text):
    sr = SurroundingRectangle(
            obj,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.9,
            buff=0.25,
        ).set_z_index(1000)

    return VGroup(
        sr,
        Tex(text).set_z_index(1001).move_to(sr),
    )

def CreateHighlight(obj, **kwargs):
    return SurroundingRectangle(
        obj,
        color=YELLOW,
        fill_opacity=0.15,
        **kwargs,
    ).set_z_index(1000)

def solve_sack(prices, weights, M):
    n = len(prices)

    model = LpProblem(name="knapsack-problem", sense=LpMaximize)

    variables = [LpVariable(name=f"x_{i}", cat=LpBinary) for i in range(n)]

    model += lpSum([weights[i] * variables[i] for i in range(n)]) <= M
    model += lpSum([prices[i] * variables[i] for i in range(n)])

    status = model.solve(PULP_CBC_CMD(msg=False))

    return [int(variables[i].value()) for i in range(n)]


def solve_farm(of, fertilizer_constant=5000):
    seed(0xdeadbeef)
    model = LpProblem(name="farmer-problem", sense=LpMaximize)

    xp = LpVariable(name="potato", lowBound=0)
    xc = LpVariable(name="carrot", lowBound=0)

    model += xp >= 0
    model += xc >= 0
    model += xp <= 3000
    model += xc <= 4000
    model += xp + xc <= fertilizer_constant

    model += of[0] * xp + of[1] * xc

    status = model.solve(PULP_CBC_CMD(msg=False))

    if status:
        return xp.value(), xc.value()
    return None



def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def distance(v1, v2):
    return np.linalg.norm(v1 - v2)

def point_line_distance(p1, p2, p3):
    return np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)

def get_infinite_square(color=BLUE, opacity=0.25):
    return Square(fill_color=color, fill_opacity=opacity, stroke_color=WHITE).scale(100).set_z_index(1)

def MyCode(code_raw, **kwargs):
    code = Code(code=code_raw, **kwargs, font="Fira Mono", line_spacing=0.65, style="Monokai", insert_line_no=False, language="python")
    code.background_mobject[0].set(stroke_color=WHITE, stroke_width=2.5, fill_opacity=0)
    code.remove(code[1])  # idk man what the fuck is the Manim code class
    return code

def crop_line_to_screen(line_to_crop, screen, buff=0, epsilon=0.01):
    points = [
        Dot().next_to(screen, LEFT + UP, buff=buff).get_center(),
        Dot().next_to(screen, RIGHT + UP, buff=buff).get_center(),
        Dot().next_to(screen, LEFT + DOWN, buff=buff).get_center(),
        Dot().next_to(screen, RIGHT + DOWN, buff=buff).get_center(),
    ]

    min_x = min([points[0][0], points[1][0], points[2][0], points[3][0]]) - epsilon
    min_y = min([points[0][1], points[1][1], points[2][1], points[3][1]]) - epsilon
    max_x = max([points[0][0], points[1][0], points[2][0], points[3][0]]) + epsilon
    max_y = max([points[0][1], points[1][1], points[2][1], points[3][1]]) + epsilon

    lines = [
        line(points[0], points[1]),
        line(points[0], points[2]),
        line(points[1], points[3]),
        line(points[2], points[3]),
    ]

    intersections = [
        intersection(line(line_to_crop.get_start(), line_to_crop.get_end()), lines[0]),
        intersection(line(line_to_crop.get_start(), line_to_crop.get_end()), lines[1]),
        intersection(line(line_to_crop.get_start(), line_to_crop.get_end()), lines[2]),
        intersection(line(line_to_crop.get_start(), line_to_crop.get_end()), lines[3]),
    ]

    valid_points = []
    for point in intersections:
        if not point:
            continue

        x, y = point

        if min_x <= x <= max_x and min_y <= y <= max_y:
            valid_points.append((x, y))

    line_to_crop.put_start_and_end_on(
        (*valid_points[0], 0),
        (*valid_points[1], 0),
    )

class AffineLine2D(VMobject):
    def __init__(self, direction: Tuple[float], offset: Tuple[float] = (0, 0), length=100, **kwargs):
        super().__init__(**kwargs)

        self.direction = direction

        p1 = np.array([0, 0, 0])
        p2 = np.array([*direction, 0])

        self.line = Line(p1, p2, color=WHITE, stroke_width=LINE_STROKE).set_z_index(0)\
                .scale(length / distance(p1, p2))\
                .move_to((*offset, 0))

        self.add(self.line)

    def crop_to_screen(self, *args, **kwargs):
        crop_line_to_screen(self.line, *args, **kwargs)

    def get_area_border_intersection(self, area):
        possible_points = []

        for i in range(len(area.inequalities)):
            point = intersection(
                line(area.inequalities[i].line.get_start(), area.inequalities[i].line.get_end()),
                line(self.line.get_start(), self.line.get_end()),
            )

            if point:
                possible_points.append(point)

        dots = VGroup()

        for point in possible_points:
            for inequality in area.inequalities:
                if not inequality.satisfies(*point, epsilon=0.01):
                    break
            else:
                dots.add(Dot().move_to([*point, 0]).set_z_index(10000).scale(OPTIMUM_DOT_SCALE))

        return dots


class Inequality2D(VMobject):
    """A class for a*x + b*y <= c | (x1 = x, x2 = y)"""

    def __init__(self, a: float, b: float, operation = "<=", c: float = 0, length=100, **kwargs):
        super().__init__(**kwargs)

        self.a = a
        self.b = b
        self.operation = operation
        self.c = c

        def get_y(x):
            return (c - a * x) / b

        def get_x(y):
            return (c - b *y) / a

        if b == 0:
            p1 = np.array([c, 0, 0])
            p2 = np.array([c, 1, 0])
        elif b < 0.1:
            p1 = np.array([get_x(0), 0, 0])
            p2 = np.array([get_x(1), 1, 0])
        else:
            p1 = np.array([0, get_y(0), 0])
            p2 = np.array([1, get_y(1), 0])

        self.line_points = (p1, p2)
        self.line = Line(p1, p2, color=WHITE, stroke_width=LINE_STROKE).set_z_index(0).scale(length / distance(p1, p2))

        offset_p1 = p1 - self.line.get_center()
        self.angle = np.arctan2(offset_p1[1], offset_p1[0])

        self.add(self.line)

    @classmethod
    def points_to_slope(cls, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        if x1 != x2:
            a = (y2 - y1) / (x1 - x2)
            b = 1
        else:
            a = 1
            b = 0

        c = a * x1 + b * y1

        return a, b, c

    def crop_to_screen(self, *args, **kwargs):
        crop_line_to_screen(self.line, *args, **kwargs)

    def _get_function(self, epsilon=0):
        if self.operation == "<=":
            return lambda x, y: self.a * x + self.b * y <= self.c + epsilon
        else:
            return lambda x, y: self.a * x + self.b * y >= self.c - epsilon

    def satisfies(self, x, y, epsilon=0):
        """Return True if the point satisfies the inequality."""
        plane = self.get_half_plane()
        polygon = geometry.Polygon(plane.get_anchors()).buffer(epsilon)
        return polygon.contains(geometry.Point(x, y))

    def get_half_plane(self):
        half_plane = get_infinite_square()

        half_plane.set_color(self.get_color())

        half_plane.move_to(self.line)\
                .align_to(self.line.get_center(), UP)\
                .rotate(self.angle, about_point=self.line.get_center())

        f = self._get_function()

        if not f(half_plane.get_x(), half_plane.get_y()):
            half_plane.rotate(PI, about_point=self.line.get_center())

        return half_plane

    def move_off_screen(self, screen):
        """Move the half-plane to be barely off the screen."""
        normal = unit_vector(self.line.get_center() - self.get_half_plane().get_center())

        self.move_to(screen)

        min_angle = float('inf')

        for point in  [
            Dot().align_to(screen, LEFT + UP).get_center(),
            Dot().align_to(screen, RIGHT + UP).get_center(),
            Dot().align_to(screen, LEFT + DOWN).get_center(),
            Dot().align_to(screen, RIGHT + DOWN).get_center(),
        ]:
            angle = abs(angle_between(point, normal))

            if angle < min_angle:
                min_angle = angle
                self.move_to(point)

        self.shift(normal * 1)


class FeasibleArea2D(VMobject):
    def __init__(self, dots_z_index=1000, **kwargs):
        super().__init__(**kwargs)

        self.area = get_infinite_square()

        self.inequalities = []

        self.dots = VGroup()

        self.dots_z_index = dots_z_index

        self.add(self.dots)
        self.add(self.area)

    def add_inequalities(self, inequalities: List[Inequality2D]):
        self.inequalities += inequalities
        self._update_area()

    def remove_inequalities(self, inequalities: List[Inequality2D], update=True):
        for i in inequalities:
            self.inequalities.remove(i)

        if update:
            self._update_area()

    def clear_inequalities(self):
        self.inequalities = []
        self._update_area()

    def _update_area(self):
        new_area = get_infinite_square()

        for inequality in self.inequalities:
            new_area = Intersection(new_area, inequality.get_half_plane(),
                color = new_area.get_color(),
                fill_opacity = new_area.get_fill_opacity(),
                stroke_width = new_area.get_stroke_width(),
                stroke_color = new_area.get_stroke_color(),
                z_index=self.get_z_index(),
            )

        self.area.become(new_area).set_z_index(self.get_z_index())

        possible_points = []

        for i in range(len(self.inequalities)):
            for j in range(i + 1, len(self.inequalities)):
                point = intersection(
                    line(self.inequalities[i].line.get_start(), self.inequalities[i].line.get_end()),
                    line(self.inequalities[j].line.get_start(), self.inequalities[j].line.get_end()),
                )

                if point:
                    possible_points.append(point)

        new_dots = VGroup()

        for point in possible_points:
            for inequality in self.inequalities:
                if not inequality.satisfies(*point, epsilon=0.01):
                    break
            else:
                new_dots.add(Dot().move_to([*point, 0]).scale(NORMAL_DOT_SCALE))

        self.dots.become(new_dots).set_z_index(self.dots_z_index)


class Inequality3D:
    """A class for a*x + b*y + c*z <= d. Not an object, just for creating 3D polygons."""
    def __init__(self, a: float, b: float, c: float, operation = "<=", d: float = 0, **kwargs):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.operation = operation

    def _get_function(self, epsilon=0):
        if self.operation == "<=":
            return lambda x, y, z: self.a * x + self.b * y + self.c * z <= self.d + epsilon
        else:
            return lambda x, y, z: self.a * x + self.b * y + self.c >= self.d - epsilon

    def satisfies(self, x, y, z, epsilon=0.005):
        """Return True if the point satisfies the inequality."""
        return self._get_function(epsilon=epsilon)(x, y, z)

    def tight(self, x, y, z, epsilon=0.005):
        return self._get_function(epsilon=+epsilon)(x, y, z) \
                and not self._get_function(epsilon=-epsilon)(x, y, z)

def fibonacci_sphere(samples=5000):
    # https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
    phi = math.pi * (math.sqrt(5.) - 1.)  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        yield np.array((x, y, z))


class Addd(Animation):

    def __init__(self, mobject: Mobject, pos, introducer=True, lor = RIGHT, **kwargs):
        self.original = mobject.copy()
        self.pos = pos
        self.lor = lor

        super().__init__(mobject, introducer=introducer, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """A function that gets called every frame, for the animation to... animate."""
        a = self.rate_func(alpha)

        destination = self.original.copy().move_to(self.pos).align_to(self.pos, self.lor).get_center()

        pos = self.original.get_center() * (1 - a) + destination * a

        fade = 0 if a < 0.5 else (a - 0.5) * 2

        new_mobject = self.original.copy().move_to(pos).fade(fade)

        self.mobject.become(new_mobject)


class FeasibleArea3D(VGroup, metaclass=ConvertToOpenGL):
    """Yeah no this implementation is an act of terrorism holy shit.

    As an explanation: I was way too lazy to create a general class, so this assumes
    that the polytope is bounded, at which point it creates many vectors, solves the
    problem in each direction via pulp and records the distinct vertices.

    For what I'm doing, I think this is fine.
    """

    def __init__(self, test=False, **kwargs):
        super().__init__(**kwargs)

        self.test = test

        self.dots = VGroup()
        self.edges = VGroup()

        self.inequalities = []

        self.add(self.dots)
        self.add(self.edges)

    def add_inequalities(self, inequalities: List[Inequality3D], vertices=None, edges=None):
        self.inequalities += inequalities

        self._update_area((vertices, edges))

    def remove_inequalities(self, inequalities: List[Inequality3D], update=True):
        for i in inequalities:
            self.inequalities.remove(i)

        if update:
            self._update_area()

    def clear_inequalities(self):
        self.inequalities = []
        self._update_area()

    def _update_area(self, vae=None, shift=np.array([0, 0, 0])):
        if self.test:
            dot_res = (2, 2)
        else:
            dot_res = (8, 8)
            line_res = (8, 8)

        for dot in self.dots:
            self.dots.remove(dot)

        for edge in self.edges:
            self.edges.remove(edge)

        if vae:
            vertices, edges = vae
        else:
            vertices = []
            edges = []

        if vertices:
            for vertex in vertices:
                self.dots.add(Dot3D(resolution=dot_res).shift(vertex + shift).scale(NORMAL_DOT_SCALE))
        else:
            vertices = set()

            for of in fibonacci_sphere(5000 if not self.test else 100):
                model = LpProblem(sense=LpMaximize)

                x = LpVariable(name="x")
                y = LpVariable(name="y")
                z = LpVariable(name="z")

                for iq in self.inequalities:
                    if iq.operation == "<=":
                        model += iq.a * x + iq.b * y + iq.c * z <= iq.d
                    else:
                        model += iq.a * x + iq.b * y + iq.c * z >= iq.d

                model += of[0] * x + of[1] * y + of[2] * z

                try:
                    status = model.solve(PULP_CBC_CMD(msg=False))

                    if x.value() is not None and y.value() is not None and z.value() is not None:
                        vertices.add((x.value(), y.value(), z.value()))

                except Exception as e:
                    print(e)

            vertices = list(vertices)

            for i, vertex in enumerate(vertices):
                self.dots.add(Dot3D(resolution=dot_res).shift(vertex + shift).scale(NORMAL_DOT_SCALE))

        if self.test:
            return

        if edges:
            for u, v in edges:
                self.edges.add(Line3D(u, v, color=WHITE, resolution=line_res).shift(shift))
        else:
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    u = vertices[i]
                    v = vertices[j]

                    # if two vertices satisfy two inequalities tightly, it's an edge
                    tight_satisfactions = 0

                    for iq in self.inequalities:
                        if iq.tight(*u) and iq.tight(*v):
                            tight_satisfactions += 1

                    if tight_satisfactions >= 2:
                        self.edges.add(Line3D(u, v, color=WHITE, resolution=line_res).shift(shift))


def align_object_by_coords(obj, current, desired, animation=False):
    """Align an object such that it's current coordinate coordinate will be the desired."""
    if isinstance(current, Mobject):
        current = current.get_center()

    if isinstance(desired, Mobject):
        desired = desired.get_center()

    if animation:
        return obj.animate.shift(desired - current)
    else:
        obj.shift(desired - current)

def get_fade_rect(*args, opacity=1 - BIG_OPACITY):
    if len(args) == 0:
        return Square(fill_opacity=opacity, color=BLACK).scale(1000).set_z_index(1000000)
    else:
        return SurroundingRectangle(VGroup(*args), fill_opacity=opacity, color=BLACK).set_z_index(1000000)

def orient_edge(g, v, w):
    """Create an oriented edge from v to w."""
    v_center = g.vertices[v].get_center()
    w_center = g.vertices[w].get_center()

    g.vertices[v].set_z_index(1)
    g.vertices[w].set_z_index(1)

    center = (v_center + w_center) / 2
    delta = (v_center - w_center) / 2

    buffer = 0.23  # hack
    mag = (delta[0] ** 2 + delta[1] ** 2)**(1/2)
    c = (mag - buffer) / mag

    arrow = Arrow(center + delta * c, center - delta * c, tip_length=0.22, stroke_width=4, buff=0)
    arrow.tip.scale(1.1)
    g.edges[(v, w)].become(arrow)

def parse_graph(graph, s=0.13, t=0.13, scale=2):
    """Parse a graph in a format like this:
    ---
    1 2 <9.118072543948081, 4.650124351556167> <15.236742443226104, 4.832736111387815>
    3 2 <20.843227140026464, 7.251324476362457> <15.236742443226104, 4.832736111387815>
    3 4 <20.843227140026464, 7.251324476362457> <20.151957872799326, 1.2158150606935652>
    4 2 <20.151957872799326, 1.2158150606935652> <15.236742443226104, 4.832736111387815>
    """

    lt = {}
    edges = []
    vertices = set()

    for line in graph.strip().splitlines():
        line = line.strip()
        edge, p1, p2 = line.split("<")
        u, v = list(map(int, edge.strip().split()))
        u_x, u_y = list(map(float, p1[:-2].strip().split(", ")))
        v_x, v_y = list(map(float, p2[:-2].strip().split(", ")))

        lt[u] = [u_x, u_y, 0]
        lt[v] = [v_x, v_y, 0]

        edges.append((u, v))
        vertices.add(u)
        vertices.add(v)

    lt_avg_x = 0
    lt_avg_y = 0

    for i in lt:
        lt_avg_x += lt[i][0]
        lt_avg_y += lt[i][1]

    lt_avg_x /= len(lt)
    lt_avg_y /= len(lt)

    for i in lt:
        lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

    g = Graph(sorted(list(vertices)), edges, layout=lt).scale(scale)
    g.clear_updaters()

    for v, w in g.edges:
        orient_edge(g, v, w)

    return g


def ComplexTex(*args, **kwargs):
    t = Tex(*args, **kwargs)
    if config.quality and config.quality.startswith("medium"):
        t.add(index_labels(t[0]))
    return t


def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)

        if config.quality and not config.quality.startswith("medium"):
            self.play(*map(FadeOut, self.mobjects))

    return inner


def MyCode(path, lang="python", **kwargs):
    with open(path) as f:
        code = Code(code=f.read(), **kwargs, font="Fira Mono", line_spacing=0.65, style="Monokai", insert_line_no=False, language=lang)
        code.background_mobject[0].set(color=BLACK, stroke_color=WHITE, stroke_width=5)
        code.remove(code[1])  # idk man what the fuck is the Manim code class
        return code

def MyFlash(*args, num_lines=13, **kwargs):
    return Flash(*args, num_lines=13, **kwargs)
    
