from utilities import *

import mm.mm

from typing import Tuple, List
from dataclasses import dataclass


class MyBulletedList(Tex):
    def __init__(
        self,
        *items,
        buff=0.10,
        dot_scale_factor=3,
        tex_environment=None,
        **kwargs,
    ):
        self.buff = buff
        self.dot_scale_factor = dot_scale_factor
        self.tex_environment = tex_environment
        line_separated_items = [s + "\\\\" for s in items]
        Tex.__init__(
            self, *line_separated_items, tex_environment=tex_environment, **kwargs
        )
        for part in self:
            dot = MathTex("\\cdot").scale(self.dot_scale_factor)
            dot.next_to(part[0], LEFT, MED_SMALL_BUFF)
            part.add_to_back(dot)
        self.arrange(DOWN, aligned_edge=LEFT, buff=self.buff)

        for part, item in zip(self, items):
            parts = item.split(r"$\mid$")
            if len(parts) != 2:
                continue

            a, b = parts
            text = Tex(a, r"$\mid$", b).move_to(part)
            text[2].set_color(YELLOW),

            dot = MathTex("\\cdot").scale(self.dot_scale_factor)
            dot.next_to(text[0], LEFT, MED_SMALL_BUFF)
            text.add_to_back(dot)

            part.become(text)


MATCHING_COLOR = YELLOW
EXPOSED_COLOR = ORANGE
AUGMENTING_COLOR = PURPLE
BFS_COLOR = BLUE

HIDDEN_COLOR = DARK_GRAY

MATCHED_WIDTH = 15

GRAPH_SCALE = 1.3
NODE_SCALE = 1.25

SHORT_CODE_PAUSE = 1

def match_vertex(mob, where=None, width=50):
    mob.set_stroke_width(width)
    mob.move_to(where)
    return mob

def unmatch_vertex(mob, where=None, width=4):
    mob.set_stroke_width(width)
    mob.move_to(where)
    return mob

def match_edge(mob, change_color=True, width=MATCHED_WIDTH):
    mob.set_stroke_width(width)

    if change_color:
        mob.set_color(MATCHING_COLOR)

    return mob

def unmatch_edge(mob, change_color=True):
    mob.set_stroke_width(4)

    if change_color:
        mob.set_color(WHITE)

    return mob


def animate_augment_path(self, g, path, add_animations_first=None, add_animations_between=None, add_animations_second=None, instant=False, switch=False, run_time=None):
    """If animations is lambda, do them only here I don't know that I'm doing."""
    A = path
    AV = edgesToVertices(A)

    offset = 0 if not switch else 1

    # instantly switches the path (with correct coloring)
    if instant:
        self.play(
            *([] if add_animations_second is None else add_animations_second() if type(add_animations_second) is type(lambda: None) else add_animations_second),
            *[
                ApplyFunction(lambda x: match_edge(x), g.edges[e])
                for e in A[offset::2]
            ],
            *[
                ApplyFunction(lambda x: unmatch_edge(x), g.edges[e])
                for e in A[(offset+1)%2::2]
            ],
            **(dict() if run_time is None else {"run_time": run_time})
        )
        return

    self.play(
        *([] if add_animations_first is None else add_animations_first() if type(add_animations_first) is type(lambda: None) else add_animations_first),
        *[g.edges[e].animate.set_color(AUGMENTING_COLOR) for e in A],
        *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for v, _ in A],
        *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for _, v in A],
        **(dict() if run_time is None else {"run_time": run_time})
    )

    if add_animations_between is not None:
        self.play(
                *add_animations_between,
                **(dict() if run_time is None else {"run_time": run_time})
                )

    self.play(
        *([] if add_animations_second is None else add_animations_second() if type(add_animations_second) is type(lambda: None) else add_animations_second),
        *[
            ApplyFunction(lambda x: match_edge(x, change_color=False), g.edges[e])
            for e in A[offset::2]
        ],
        *[
            ApplyFunction(lambda x: unmatch_edge(x, change_color=False), g.edges[e])
            for e in A[(offset+1)%2::2]
        ],
        **(dict() if run_time is None else {"run_time": run_time})
    )

    self.play(
        *[g.edges[e].animate.set_color(MATCHING_COLOR) for e in A[offset::2]],
        *[g.edges[e].animate.set_color(WHITE) for e in A[(offset+1)%2::2]],
        *[g.vertices[v].animate.set_color(MATCHING_COLOR) for v, _ in A[offset::2]],
        *[g.vertices[v].animate.set_color(MATCHING_COLOR) for _, v in A[offset::2]],
        **(dict() if run_time is None else {"run_time": run_time})
    )


def animate_correct_graph_color(self, g, M, set_lines=None, code=None, add_animations=None, run_time=None):
    MV = edgesToVertices(M)

    self.play(
        *([] if add_animations is None else add_animations() if type(add_animations) is type(lambda: None) else add_animations),
        *([] if set_lines is None else set_lines(self, code, [24])),
        *[g.edges[e].animate.set_color(WHITE) for e in g.edges if e not in M],
        *[g.edges[e].animate.set_color(MATCHING_COLOR) for e in g.edges if e in M],
        *[
            g.vertices[v].animate.set_color(EXPOSED_COLOR)
            for v in g.vertices
            if v not in MV
        ],
        *[
            g.vertices[v].animate.set_color(MATCHING_COLOR)
            for v in g.vertices
            if v in MV
        ],
        **(dict() if run_time is None else {"run_time": run_time})
    )


def neighbours(v, edges):
    t = []
    for e in edges:
        if v in e:
            t.append(e)
    return [a for a in edgesToVertices(t) if a != v]


class Kids(Scene):
    @fade
    def construct(self):

        n = ["Alice", "Bob", "Carl", "Dan", "Ema", "Febe"]

        kids = [SVGMobject(f"kids/{i + 1}.svg").scale(0.58) for i in range(6)]
        names = [Tex(n[i]).scale(0.8) for i in range(6)]

        seed(4)
        g = nx.generators.gnm_random_graph(6, 6)

        g = Graph(list(g.nodes), list(g.edges))

        C = 2.3
        D = 3
        for i in range(6):
            kids[i].shift(D * RIGHT * abs(sin((PI * 2 / 6) * i - PI / 6)) ** 1.3 * sgn(sin((PI * 2 / 6) * i - PI / 6)) + C * UP * cos((PI * 2 / 6) * i - PI / 6)).shift(DOWN * 0.3)
            g.vertices[i].move_to(kids[i].get_center())
            g.vertices[i].scale(3)
            g.vertices[i].set_opacity(0)
            names[i].next_to(kids[i], UP, 0.2)

        self.play(LaggedStart(*([] + [a for b in zip([Write(img) for img in kids], [Write(name) for name in names]) for a in b]), lag_ratio=0.2), run_time=1.5)

        self.bring_to_back(g)

        self.play(Write(g), run_time=2)

        from itertools import chain, combinations

        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

        good_subsets = []
        for subset in powerset(g.edges):
            bad = False
            for a, b in subset:
                for c, d in subset:
                    if (a, b) == (c, d):
                        continue

                    if a == c or a == d or b == c or b == d:
                        bad = True

            if bad:
                continue

            good_subsets.append(list(subset))

        for subset in good_subsets:
            self.play(
                *[
                    ApplyFunction(lambda x: match_edge(x), g.edges[e])
                    for e in subset
                ],
                *[
                    ApplyFunction(lambda x: unmatch_edge(x), g.edges[e])
                    for e in g.edges if e not in subset
                ],
                *[g.vertices[v].animate.set_color(MATCHING_COLOR) for v in edgesToVertices(subset)],
                *[g.vertices[v].animate.set_color(EXPOSED_COLOR) for v in g.vertices if v not in edgesToVertices(subset)],
                run_time=0.3
            )


class Edmonds(Scene):
    @fade
    def construct(self):
        text = Tex("\huge Jack Edmonds").shift(LEFT * 2.7 + UP * 1)
        image = SVGMobject("edmonds.svg").scale(4).shift(1.4 * DOWN + RIGHT * 4.25)

        self.play(
            Write(text),
            Write(image),
        )

        l = MyBulletedList(
                r"\footnotesize the blossom algorithm",
                'P vs. NP (tractable problems)',
                "linear programming, matroids")
        l.next_to(text, DOWN, 0.6)

        self.play(Write(l))

class Intro(Scene):
    @fade
    def construct(self):
        g = parse_graph(
            """
1 2 <6.603275758877981, 0.22200042158063704> <10.542340602049554, 5.0486231945767255>
1 3 <6.603275758877981, 0.22200042158063704> <0.8751494485961517, 2.8894436903527834>
2 4 <10.542340602049554, 5.0486231945767255> <8.316429210045438, 9.49508367004807>
1 5 <6.603275758877981, 0.22200042158063704> <5.320620964273308, -6.074692063436867>
3 6 <0.8751494485961517, 2.8894436903527834> <-4.8178524679438075, 0.2426494079303798>
6 7 <-4.8178524679438075, 0.2426494079303798> <-10.765611934215096, -1.6359342354516002>
7 8 <-10.765611934215096, -1.6359342354516002> <-14.201191317109153, 3.5640128560657254>
3 9 <0.8751494485961517, 2.8894436903527834> <-0.22868399658749183, 8.989711296016043>
6 10 <-4.8178524679438075, 0.2426494079303798> <-6.36641219483813, -5.744685968682711>
1 12 <6.603275758877981, 0.22200042158063704> <11.495122080884329, -4.388454491563957>
8 13 <-14.201191317109153, 3.5640128560657254> <-8.237759615621837, 6.486457369598593>
7 10 <-10.765611934215096, -1.6359342354516002> <-6.36641219483813, -5.744685968682711>
5 12 <5.320620964273308, -6.074692063436867> <11.495122080884329, -4.388454491563957>
3 11 <0.8751494485961517, 2.8894436903527834> <0.4357598447196547, -3.4516057795938906>
2 14 <10.542340602049554, 5.0486231945767255> <16.235759844719652, 1.2483942204061114>
                """,
            s=0.12 / NODE_SCALE,
            t=-0.10 / NODE_SCALE,
        ).scale(GRAPH_SCALE * NODE_SCALE).shift(DOWN * 0.5)

        text = Tex("\large definitions").next_to(g, UP * 3)

        self.play(Write(text), Write(g))

        self.play(
            *[Indicate(g.vertices[v], color=WHITE) for v in g.vertices]
        )

        self.play(
            *[ApplyFunction(partial(match_edge, change_color=False, width=10), g.edges[e]) for e in g.edges],
            run_time=0.5,
        )

        self.play(
            *[ApplyFunction(unmatch_edge, g.edges[e], change_color=False) for e in g.edges],
            run_time=0.5,
        )

        M = [(1, 2), (8, 13), (5, 12)]
        MV = edgesToVertices(M)

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in M],
            *[g.vertices[v].animate.set_color(MATCHING_COLOR) for v, _ in M],
            *[g.vertices[v].animate.set_color(MATCHING_COLOR) for _, v in M],
        )

        MP = mm.mm.get_maximum_matching(list(g.edges))
        MPV = edgesToVertices(MP)

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in MP if e not in M],
            *[
                g.vertices[v].animate.set_color(MATCHING_COLOR)
                for v, _ in MP
                if v not in MV
            ],
            *[
                g.vertices[v].animate.set_color(MATCHING_COLOR)
                for _, v in MP
                if v not in MV
            ],
            *[ApplyFunction(unmatch_edge, g.edges[e]) for e in M if e not in MP],
            *[g.vertices[v].animate.set_color(WHITE) for v, _ in M if v not in MPV],
            *[g.vertices[v].animate.set_color(WHITE) for _, v in M if v not in MPV],
        )

        self.play(
            *[
                Circumscribe(g.vertices[v], Circle, color=EXPOSED_COLOR)
                for v in g.vertices
                if v not in MPV
            ],
            *[
                g.vertices[v].animate.set_color(EXPOSED_COLOR)
                for v in g.vertices
                if v not in MPV
            ],
        )


class Core(Scene):
    @fade
    def construct(self):
        g = parse_graph(
            """
1 2 <10.402934501867037, 17.34415069651897> <16.203839106744862, 19.547491168818176>
2 3 <16.203839106744862, 19.547491168818176> <22.178420402084758, 17.787256748775246> 
3 4 <22.178420402084758, 17.787256748775246> <20.774348346247653, 23.755044257314765>
2 4 <16.203839106744862, 19.547491168818176> <20.774348346247653, 23.755044257314765>
4 5 <20.774348346247653, 23.755044257314765> <27.05817492976113, 23.859707295924565>
6 5 <28.449708119653423, 17.768804208250373> <27.05817492976113, 23.859707295924565>
4 7 <20.774348346247653, 23.755044257314765> <17.47242508549339, 29.021438342487553>
5 8 <27.05817492976113, 23.859707295924565> <31.15502907598739, 28.586235859209886>
8 9 <31.15502907598739, 28.586235859209886> <37.31660856822276, 28.245054265211092> 
6 10 <28.449708119653423, 17.768804208250373> <34.660938508332286, 16.631467003826533>
10 11 <34.660938508332286, 16.631467003826533> <40.60957109101587, 18.40703837992414>
3 6 <22.178420402084758, 17.787256748775246> <28.449708119653423, 17.768804208250373>
5 12 <27.05817492976113, 23.859707295924565> <33.0788344527837, 22.821541250821294>
2 13 <16.203839106744862, 19.547491168818176> <12.52911329849324, 24.494238155627645>
                """,
            s=0.12 / NODE_SCALE,
            t=-0.12 / NODE_SCALE,
        ).scale(GRAPH_SCALE * NODE_SCALE).shift(DOWN * 0.65)

        text = Tex("\large augmenting paths").next_to(g, UP * 3)

        self.play(
            Write(text),
            Write(g),
            )

        M = [(5, 8), (6, 10), (2, 4)]
        MV = edgesToVertices(M)

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in M],
            *[g.vertices[v].animate.set_color(MATCHING_COLOR) for v, _ in M],
            *[g.vertices[v].animate.set_color(MATCHING_COLOR) for _, v in M],
            *[
                g.vertices[v].animate.set_color(EXPOSED_COLOR)
                for v in g.vertices
                if v not in MV
            ],
        )

        animate_augment_path(self, g, [(8, 9), (5, 8), (4, 5), (2, 4), (1, 2)],
                add_animations_between=[
                    Circumscribe(g.vertices[9], Circle, color=AUGMENTING_COLOR),
                    Circumscribe(g.vertices[1], Circle, color=AUGMENTING_COLOR),
                    ])

        self.play(text.animate.shift(UP * 0.2),
                g.animate.shift(DOWN * 0.2))

        text2 = Tex(r"\scriptsize \em contains an augmenting path $\Leftrightarrow$ matching is not maximum$^{\ast}$").next_to(text, DOWN)

        box = Tex(r"$\ast$ proof in description – theorem 2.4").scale(0.5).align_on_border(UP + RIGHT)
        frame = SurroundingRectangle(box, color=WHITE, stroke_width=2)

        self.play(Write(text2))

        self.play(
            Write(box, run_time=0.7),
            Write(frame)
        )

        animate_augment_path(self, g, [(10, 11), (6, 10), (3, 6)])
        animate_augment_path(self, g, [(5, 12), (4, 5), (4, 7)])


def edgeFromVertices(v, w, e):
    if (v, w) in e:
        return (v, w)
    return (w, v)


def animate_tree_algorithm_iteration(self, g, M, set_lines, code, run_time=None, no_code=False):
    MV = edgesToVertices(M)
    exposed = [v for v in g.vertices if v not in MV]

    shuffle(exposed)
    shuffle(MV)

    explored = set()

    for v in exposed:
        self.play(
            # HACK, since cirsumscribe is animated poorly
            *([Circumscribe(g.vertices[v], Circle, color=BFS_COLOR)] if run_time is None else []),
            g.vertices[v].animate.set_color(BFS_COLOR),
            *set_lines(self, code, [14]),
            **(dict() if run_time is None else {"run_time": run_time})
        )

        if not no_code:
            self.play(*set_lines(self, code, [15]), run_time=SHORT_CODE_PAUSE)
            self.play(*set_lines(self, code, [2]), run_time=SHORT_CODE_PAUSE)
            self.play(*set_lines(self, code, [3]), run_time=SHORT_CODE_PAUSE)

        queue = [(v, False, [])]

        current_layer = []
        previous_layer_length = 0
        augmenting_path = None

        while len(queue) != 0:
            v, edge_type, path = queue.pop(0)
            explored.add(v)

            # if we've explored the current layer
            if len(path) > previous_layer_length:

                # animate it
                self.play(
                    *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(current_layer)],
                    *[g.edges[e].animate.set_color(BFS_COLOR) for e in current_layer],
                    *set_lines(self, code, [4 if previous_layer_length % 2 == 0 else 9]), **(dict() if run_time is None else {"run_time": run_time})
                )

                # if it also contains an augmenting path, then animate it
                if augmenting_path is not None:
                    # animate the augmenting path
                    animate_augment_path(self, g, augmenting_path,
                            add_animations_first=lambda: set_lines(self, code, [6, 7]),
                            add_animations_second=lambda: set_lines(self, code, [17, 18, 19]),
                            run_time=run_time)

                    # dirty hack alert!
                    set_lines(self, code, [17, 18, 19])

                    # improve M
                    for i in range(0, len(augmenting_path), 2):
                        M.append(augmenting_path[i])
                    for i in range(1, len(augmenting_path), 2):
                        M.remove(augmenting_path[i])

                    return True

                previous_layer_length = len(path)

            for neighbour in neighbours(v, g.edges):
                if neighbour in explored:
                    continue

                e = edgeFromVertices(v, neighbour, g.edges)

                new_path = path + [e]

                if neighbour not in MV and not edge_type:
                    augmenting_path = new_path
                    current_layer.append(e)

                if edge_type and e in M or not edge_type and e not in M:
                    queue.append((neighbour, not edge_type, new_path))
                    current_layer.append(e)

    if not no_code:
        self.play(*set_lines(self, code, [11]), run_time=SHORT_CODE_PAUSE)
        self.play(*set_lines(self, code, [21]), run_time=SHORT_CODE_PAUSE)
        self.play(*set_lines(self, code, [25]), run_time=SHORT_CODE_PAUSE)
    return False


class Tree(Scene):
    @fade
    def construct(self):
        g_new_positions = parse_graph(
            """
1 2 <22.112572766007876, -2.5264304107833246> <25.67796210932871, 2.697892851581728>
3 1 <28.55611115849213, -3.7428115450105133> <22.112572766007876, -2.5264304107833246>
4 1 <15.428111442950147, -2.829960372608953> <22.112572766007876, -2.5264304107833246>
4 5 <15.428111442950147, -2.829960372608953> <8.976964571929539, -3.0504356092202367>
3 6 <28.55611115849213, -3.7428115450105133> <34.04768084651785, -0.5973824149390512>
3 7 <28.55611115849213, -3.7428115450105133> <32.64776811333644, -8.460442932301625>
5 8 <8.976964571929539, -3.0504356092202367> <3.834695753774831, -6.50435350211315>
4 9 <15.428111442950147, -2.829960372608953> <14.226722555124457, -8.942190801950318>
2 10 <25.67796210932871, 2.697892851581728> <28.496351384614382, 8.224513316804416>
1 11 <22.112572766007876, -2.5264304107833246> <22.95614485199056, -8.724125830834108>
1 12 <22.112572766007876, -2.5264304107833246> <19.316663589836477, 3.048818090535028>
13 4 <11.896071360485621, 2.430059482684668> <15.428111442950147, -2.829960372608953>
14 6 <38.90070190924257, 3.2512436388123502> <34.04768084651785, -0.5973824149390512>
13 15 <11.896071360485621, 2.430059482684668> <8.433034228381587, 7.599704780509387>
5 16 <8.976964571929539, -3.0504356092202367> <3.6702917967931405, 0.23588429272754086>
17 12 <17.000076691912383, 8.77194474648056> <19.316663589836477, 3.048818090535028>
                """,
            s=0.05,
            t=0.06,
        ).scale(GRAPH_SCALE * NODE_SCALE).shift(3.7 * RIGHT)
        g_new_positions.rotate_in_place(-PI / 2)

        g = parse_graph(
            """
1 2 <22.112572766007876, -2.5264304107833246> <25.67796210932871, 2.697892851581728>
3 1 <28.55611115849213, -3.7428115450105133> <22.112572766007876, -2.5264304107833246>
4 1 <15.428111442950147, -2.829960372608953> <22.112572766007876, -2.5264304107833246>
4 5 <15.428111442950147, -2.829960372608953> <8.976964571929539, -3.0504356092202367>
3 6 <28.55611115849213, -3.7428115450105133> <34.04768084651785, -0.5973824149390512>
3 7 <28.55611115849213, -3.7428115450105133> <32.64776811333644, -8.460442932301625>
5 8 <8.976964571929539, -3.0504356092202367> <3.834695753774831, -6.50435350211315>
4 9 <15.428111442950147, -2.829960372608953> <14.226722555124457, -8.942190801950318>
2 10 <25.67796210932871, 2.697892851581728> <28.496351384614382, 8.224513316804416>
1 11 <22.112572766007876, -2.5264304107833246> <22.95614485199056, -8.724125830834108>
1 12 <22.112572766007876, -2.5264304107833246> <19.316663589836477, 3.048818090535028>
13 4 <11.896071360485621, 2.430059482684668> <15.428111442950147, -2.829960372608953>
14 6 <38.90070190924257, 3.2512436388123502> <34.04768084651785, -0.5973824149390512>
13 15 <11.896071360485621, 2.430059482684668> <8.433034228381587, 7.599704780509387>
5 16 <8.976964571929539, -3.0504356092202367> <3.6702917967931405, 0.23588429272754086>
17 12 <17.000076691912383, 8.77194474648056> <19.316663589836477, 3.048818090535028>
                """,
            s=0.09,
            t=0.09,
        ).scale(GRAPH_SCALE * NODE_SCALE)

        code_str = """def find_augmenting_path(v):
    bfs.start_from_vertex(v)
    while bfs.has_unexplored_vertices():
        bfs.add_vertices_not_in_matching()

        if bfs.found_augmenting_path():
            return bfs.augmenting_path

        bfs.add_vertices_in_matching()

    return []

def improve_matching(G):
    for v in exposed_vertices(G):
        path = find_augmenting_path(v)

        if path != []:
            switch_augmenting_path(path)
            return True

    return False

while True:
    if not improve_matching(G):
        break"""

        code = Code(code=code_str, font="Fira Mono", line_spacing=0, style="Monokai", language="python")
        code.background_mobject[0].set_opacity(0)
        code.scale(0.65).shift(2.6 * LEFT)

        c = 0.075

        for i in range(1, len(code.code)):
            code.code[i].shift(i * DOWN * c)
            code.line_numbers[i].shift(i * DOWN * c)

        code.shift(UP * len(code.code) * c / 2)

        frame = SurroundingRectangle(code, color=WHITE, stroke_width=2)
        frame.round_corners(0.2).shift(DOWN * 0.1)

        self.play(Write(g))

        self.play(
            *[g.vertices[v].animate.move_to(g_new_positions.vertices[v].get_center()) for v in g.vertices],
            run_time=1.5
        )

        self.play(Write(code), Write(frame))

        M = []

        def set_lines(self, code, lines, previous_lines=[]):
            # by default, the code has all lines highligted
            if previous_lines == []:
                for i in range(len(code.code_string.splitlines())):
                    previous_lines.append(i + 1)
                    code.code.chars[i - 1].save_state()

            # lines newly highlighted
            new_lines = [l for l in lines if l not in previous_lines]

            # lines that will disappear
            dis_lines = [l for l in previous_lines if l not in lines]

            for l in dis_lines:
                code.code.chars[l - 1].save_state()

            new_lines_animation = [code.line_numbers[i - 1].animate.set_color(WHITE) for i in new_lines] + \
                                  [code.code.chars[i - 1].animate.restore() for i in new_lines]
            dis_lines_animation = [code.line_numbers[i - 1].animate.set_color(HIDDEN_COLOR) for i in dis_lines] + \
                                  [code.code.chars[i - 1].animate.set_color(HIDDEN_COLOR) for i in dis_lines]

            while len(previous_lines) != 0:
                previous_lines.pop()

            for e in lines:
                previous_lines.append(e)

            return new_lines_animation + dis_lines_animation

        seed(3)

        self.play(*set_lines(self, code, [i + 1 for i in range(11)]))

        self.play(*set_lines(self, code, [i + 1 for i in range(12, 25)]))

        self.play(*set_lines(self, code, [i + 1 for i in range(25)]))

        while True:
            animate_correct_graph_color(self, g, M, set_lines, code)

            result = animate_tree_algorithm_iteration(self, g, M, set_lines, code)

            if not result:
                break

        animate_correct_graph_color(self, g, M, lambda x, y, z: [], None, add_animations=lambda: set_lines(self, code, [i + 1 for i in range(len(code.code))]))


class Problem(Scene):
    @fade
    def construct(self):
        g = parse_graph(
            """
1 2 <45.9217542503518, 30.268039362382353> <40.418193960422386, 27.255790801835087>
2 3 <40.418193960422386, 27.255790801835087> <40.275304608904456, 21.00876563036128>
3 4 <40.275304608904456, 21.00876563036128> <34.290257207802384, 19.319999132635935>
4 5 <34.290257207802384, 19.319999132635935> <30.320308258664582, 24.016251087986912>
5 6 <30.320308258664582, 24.016251087986912> <34.411741345002966, 28.722301776246766>
2 6 <40.418193960422386, 27.255790801835087> <34.411741345002966, 28.722301776246766>
1 7 <45.9217542503518, 30.268039362382353> <52.08682172920419, 30.518073800366004>
3 8 <40.275304608904456, 21.00876563036128> <45.88376295063149, 23.472558301422573>
3 9 <40.275304608904456, 21.00876563036128> <44.74231894798374, 16.725946411138796>
                """,
            s=0.1,
            t=-0.1,
        ).scale(GRAPH_SCALE * NODE_SCALE)

        self.play(Write(g))

        M = [(1, 2), (3, 4), (5, 6)]
        MV = edgesToVertices(M)
        exposed = [v for v in g.vertices if v not in MV]

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in M],
            *[g.vertices[v].animate.set_color(MATCHING_COLOR) for v in edgesToVertices(M)],
            *[g.vertices[v].animate.set_color(EXPOSED_COLOR) for v in exposed],
        )

        self.play(
                g.vertices[7].animate.set_color(BFS_COLOR),
                Circumscribe(g.vertices[7], Circle, color=BFS_COLOR)
                )

        layers = [[(1, 7)], [(1, 2)], [(2, 3), (2, 6)], [(3, 4), (5, 6)], [(4, 5)]]

        for current_layer in layers:
            self.play(
                *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(current_layer)],
                *[g.edges[e].animate.set_color(BFS_COLOR) for e in current_layer],
            )

        animate_correct_graph_color(self, g, M)

        self.play(
            *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for v in edgesToVertices([(1, 7), (1, 2), (2, 6), (5, 6), (4, 5), (3, 4), (3, 9)])],
            *[g.edges[v].animate.set_color(AUGMENTING_COLOR) for v in [(1, 7), (1, 2), (2, 6), (5, 6), (4, 5), (3, 4), (3, 9)]],
        )

        animate_correct_graph_color(self, g, M)

        self.play(
            g.vertices[8].animate.set_color(HIDDEN_COLOR),
            g.vertices[9].animate.set_color(HIDDEN_COLOR),
            g.edges[(3, 9)].animate.set_color(HIDDEN_COLOR),
            g.edges[(3, 8)].animate.set_color(HIDDEN_COLOR),
        )

        average = (g.vertices[2].get_center() \
                + g.vertices[3].get_center() \
                + g.vertices[4].get_center() \
                + g.vertices[5].get_center() \
                + g.vertices[6].get_center()) / 5

        blossom_text = Tex(r"blossom").move_to(average)
        stem_text = Tex(r"stem").next_to(g.vertices[1], UP).shift(RIGHT * 0.3 + UP * 0.3)

        self.play(
            g.vertices[7].animate.set_color(HIDDEN_COLOR),
            g.vertices[1].animate.set_color(HIDDEN_COLOR),
            g.edges[(1, 7)].animate.set_color(HIDDEN_COLOR),
            g.edges[(1, 2)].animate.set_color(HIDDEN_COLOR),
        )

        self.play(
            Write(blossom_text),
        )

        self.play(
            g.vertices[3].animate.set_color(HIDDEN_COLOR),
            g.vertices[4].animate.set_color(HIDDEN_COLOR),
            g.vertices[5].animate.set_color(HIDDEN_COLOR),
            g.vertices[6].animate.set_color(HIDDEN_COLOR),
            g.edges[(2, 3)].animate.set_color(HIDDEN_COLOR),
            g.edges[(2, 6)].animate.set_color(HIDDEN_COLOR),
            g.edges[(3, 4)].animate.set_color(HIDDEN_COLOR),
            g.edges[(4, 5)].animate.set_color(HIDDEN_COLOR),
            g.edges[(5, 6)].animate.set_color(HIDDEN_COLOR),
            blossom_text.animate.set_color(HIDDEN_COLOR),
            g.vertices[7].animate.set_color(EXPOSED_COLOR),
            g.vertices[1].animate.set_color(MATCHING_COLOR),
            g.edges[(1, 7)].animate.set_color(WHITE),
            g.edges[(1, 2)].animate.set_color(MATCHING_COLOR),
        )

        self.play(
            Write(stem_text),
        )

        animate_correct_graph_color(self, g, M, add_animations=[blossom_text.animate.set_color(WHITE)])

        self.play(
            FadeOut(blossom_text),
            FadeOut(stem_text),
        )

        layers = [[(1, 7)], [(1, 2)], [(2, 3), (2, 6)], [(3, 4), (5, 6)], [(4, 5)]]

        for current_layer in layers:
            self.play(
                *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(current_layer)],
                *[g.edges[e].animate.set_color(BFS_COLOR) for e in current_layer],
                run_time=0.3,
            )

        self.play(
            g.animate.shift(LEFT * 2),
        )


        parts = [
            r"\small $1.\ $contract the blossomg\\ " + "\n",
            r"\small $2.\ $find augmenting path\\ " + "\n",
            r"\small $3.\ $improve the matching\\ " + "\n",
            r"\small $4.\ $lift the path\\ "
        ]

        l = Tex(*parts)
        l.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3.5 + UP * 0.4)

        #l[0][2:10].set_color(YELLOW)
        l[0][20].set_color(BLACK)
        #l[1][2:6].set_color(YELLOW)
        #l[2][2:9].set_color(YELLOW)
        #l[3][2:6].set_color(YELLOW)

        # fml
        small_random = [1 + i / 10000 for i in range(5)]

        average = (g.vertices[2].get_center() \
                + g.vertices[3].get_center() \
                + g.vertices[4].get_center() \
                + g.vertices[5].get_center() \
                + g.vertices[6].get_center()) / 5

        original_positions = [
            g.vertices[2].get_center(),
            g.vertices[3].get_center(),
            g.vertices[4].get_center(),
            g.vertices[5].get_center(),
            g.vertices[6].get_center(),
        ]


        self.play(
            ApplyFunction(lambda x: match_vertex(x, where=average * small_random[0]), g.vertices[2]),
            ApplyFunction(lambda x: match_vertex(x, where=average * small_random[1]), g.vertices[3]),
            ApplyFunction(lambda x: match_vertex(x, where=average * small_random[2]), g.vertices[4]),
            ApplyFunction(lambda x: match_vertex(x, where=average * small_random[3]), g.vertices[5]),
            ApplyFunction(lambda x: match_vertex(x, where=average * small_random[4]), g.vertices[6]),
            Write(l[0]),
        )

        animate_correct_graph_color(self, g, M)

        animate_augment_path(self, g, [(1, 7), (1, 2), (2, 6), (5, 6), (4, 5), (3, 4), (3, 9)],
            add_animations_first=[Write(l[1])],
            add_animations_second=[Write(l[2])],
        )

        self.play(
            ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[0]), g.vertices[2]),
            ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[1]), g.vertices[3]),
            ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[2]), g.vertices[4]),
            ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[3]), g.vertices[5]),
            ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[4]), g.vertices[6]),
            Write(l[3]),
        )

        self.play(
                g.animate.shift(DOWN * 0.75),
                l.animate.shift(DOWN * 0.75),
                )

        text2 = Tex(r"\scriptsize \em has augmenting path $\Leftrightarrow$ contracted graph has augmenting path$^{\ast}$").shift(UP * 2.6)

        box = Tex(r"$\ast$ proof in description – theorem 2.9").scale(0.5).align_on_border(UP + RIGHT)
        frame = SurroundingRectangle(box, color=WHITE, stroke_width=2)

        self.play(Write(text2))

        self.play(
            Write(box, run_time=0.7),
            Write(frame),
            run_time=1,
        )

#--------------------------------
#--------------------------------
#--------------------------------
#--------------------------------
#--------------------------------

Vertex = int
Edge = Tuple[Vertex, Vertex]
MyGraph = Tuple[List[Vertex], List[Edge]]


def neighbours_(v: Vertex, graph: MyGraph) -> List[Vertex]:
    """Return the neighbours_ of the vertex v in the graph."""
    return list(
        set([a for a, b in graph[1] if b == v]).union(
            set([b for a, b in graph[1] if a == v])
        )
    )


def get_exposed_vertices(graph: MyGraph, matching: List[Edge]) -> List[Vertex]:
    """Return the exposed vertices of the graph, given a matching."""
    return [
        v
        for v in graph[0]
        if v not in list(set([v for _, v in matching] + [v for v, _ in matching]))
    ]


def path_to_root(v, parent):
    """Return the path to the root of the forest, given a vertex."""
    path = []
    while parent[v] != v:
        path.append((v, parent[v]))
        v = parent[v]
    return path


def reverse_tuples(l: List) -> List:
    """[(0, 1), (2, 3)] -> [(1, 0), (3, 2)]."""
    return list(map(lambda x: tuple(reversed(x)), l))


def reverse_list(l: List) -> List:
    """[0, 1, 2] -> [2, 1, 0]"""
    return list(reversed(l))


def get_blossom_edges(v: Vertex, w: Vertex, parent) -> List[Edge]:
    """Get the path around the blossom, starting from the root."""
    v_path = reverse_list(reverse_tuples(path_to_root(v, parent)))
    w_path = reverse_list(reverse_tuples(path_to_root(w, parent)))

    while len(v_path) != 0 and len(w_path) != 0 and v_path[0] == w_path[0]:
        v_path.pop(0)
        w_path.pop(0)

    return v_path + [(v, w)] + reverse_list(reverse_tuples(w_path))


def get_blossom_vertices(v: Vertex, w: Vertex, parent) -> List[Vertex]:
    """Get the vertices of a blossom from the forest that ends in v, w.
    It is guaranteed that the first vertex is the root."""
    combined_path_vertices = [v for e in get_blossom_edges(v, w, parent) for v in e]

    return [combined_path_vertices[0]] + list(
        set(combined_path_vertices) - {combined_path_vertices[0]}
    )


def get_augmenting_blossom_path(v: Vertex, w: Vertex, edges: List[Edge]):
    """Get the path around the blossom edges, with the root being v and exit point being w."""
    if v == w:
        return []

    # first, try to go this way
    cycle = edges + edges
    s, e = -1, -1
    path = []
    for i, (a, b) in enumerate(cycle):
        if a == v:
            s = i

        if s != -1:
            path.append((a, b))

        if b == w:
            if len(path) % 2 == 0:
                return path
            break

    # now try to go the other way
    cycle = reverse_list(reverse_tuples(cycle))
    s, e = -1, -1
    path = []
    for i, (a, b) in enumerate(cycle):
        if a == v:
            s = i

        if s != -1:
            path.append((a, b))

        if b == w:
            if len(path) % 2 == 0:
                return path
            break

    print("This should not have happened, there is a bug somewhere.")
    quit()


def unfuk_path(path, context):
    new_path = list(path)

    for i in range(len(new_path)):
        e = new_path[i]

        # a bit of a hack since the edges are all messed up
        if e not in context.graph.edges:
            e = (e[1], e[0])

        new_path[i] = e

    return new_path


def find_augmenting_path(graph: MyGraph, matching: List[Edge], context) -> List[Edge]:
    """Find and return an augmenting path in the graph, or [] if there isn't one."""
    # FOREST variables
    parent = {}  # parent[v]... parent of v in the forest
    sibling = {}  # sibling[v]... list of siblings of v in the forest
    root_node = {}  # root_node[v]... root node for v
    layer = {}  # layer[v]... which layer is v in

    # start with all exposed vertices as tree roots
    queue = get_exposed_vertices(graph, matching)
    marked = set(matching)

    for v in queue:
        parent[v] = v
        sibling[v] = []
        root_node[v] = v
        layer[v] = 0

    # run a BFS to add the augmenting paths to the forest
    while len(queue) != 0:
        v = queue.pop(0)

        # skip marked vertices
        if v in marked:
            continue

        for w in neighbours_(v, graph):
            if (v, w) in marked or (w, v) in marked:
                continue

            # add neighbours_ of w that are in the matching to the forest
            if w not in layer:
                parent[w] = v
                sibling[v] = [] if v not in sibling else sibling[v] + [w]
                layer[w] = layer[v] + 1
                root_node[w] = root_node[v]

                # find the one vertex it is matched with
                for x in neighbours_(w, graph):
                    if (w, x) in matching or (x, w) in matching:
                        sibling[w] = [] if w not in sibling else sibling[w] + [x]
                        parent[x] = w
                        layer[x] = layer[w] + 1
                        root_node[x] = root_node[w]

                        queue.append(x)
            else:
                if layer[w] % 2 == 0:
                    if root_node[v] != root_node[w]:
                        return (
                            reverse_list(path_to_root(v, parent))
                            + [(v, w)]
                            + path_to_root(w, parent)
                        )
                    else:
                        vertices = get_blossom_vertices(v, w, parent)
                        root = vertices[0]

                        # preserve the root as the new vertex
                        new_vertices = list(set(graph[0]) - set(vertices[1:]))

                        # transform all edges that previously went to the blossom to the new single vertex
                        new_edges = [
                            (
                                a if a not in vertices else vertices[0],
                                b if b not in vertices else vertices[0],
                            )
                            for a, b in graph[1]
                        ]

                        # remove loops and multi-edges
                        new_edges = [(a, b) for a, b in new_edges if a != b]
                        new_edges = [
                            (a, b)
                            for a, b in new_edges
                            if (b, a) not in new_edges or b < a
                        ]

                        # remove removed edges from the matching
                        new_matching = [
                            (a, b)
                            for a, b in matching
                            if a not in vertices[1:] and b not in vertices[1:]
                        ]
                        new_graph = (new_vertices, new_edges)

                        #---
                        small_random = [1 + i / 10000 for i in range(len(vertices))]
                        original_positions = [context.graph.vertices[v].get_center() for v in vertices]

                        avg = sum(original_positions) / len(vertices)

                        context.self.play(*[context.graph.vertices[v].animate.move_to(avg * small_random[i]) for i, v in enumerate(vertices)])
                        #---

                        # recursively find the augmenting path in the new graph
                        path = find_augmenting_path(new_graph, new_matching, context)

                        # if no path was found, no path lifting will be done
                        if path == []:
                            return []

                        # find the edges that are connected to the compressed vertex
                        edges_in_vertices = []
                        for a, b in path:
                            if a in vertices or b in vertices:
                                edges_in_vertices.append((a, b))

                        # if the path doesn't cross the blossom, simply return it
                        if len(edges_in_vertices) == 0:
                            return path

                        # find the other vertex that the blossom is connected to
                        # it enters through the root and must leave somewhere...
                        enter_edge = None
                        leave_edge = None
                        leave_edge_match = None
                        for a_orig, b_orig in edges_in_vertices:
                            vertex = a_orig if a_orig != root else b_orig

                            candidates = []

                            for b, c in graph[1]:
                                if (
                                    b == vertex
                                    and c in vertices
                                    or c == vertex
                                    and b in vertices
                                ):
                                    candidates.append((b, c))

                            for a, b in candidates:
                                if a == root or b == root and enter_edge is None:
                                    enter_edge = (a if a != root else b, root)
                                    break
                            else:
                                # doesn't matter... we can make any vertex work
                                a, b = candidates[0]

                                leave_edge_match = (a_orig, b_orig)
                                leave_edge = (
                                    a if a not in vertices else b,
                                    a if a in vertices else b,
                                )

                        if leave_edge is None:
                            return path

                        blossom_path = get_augmenting_blossom_path(
                            root, leave_edge[1], get_blossom_edges(v, w, parent)
                        )

                        i = path.index(leave_edge_match)

                        # improve the matching by injecting the lifted path
                        if i - 1 >= 0 and root in path[i]:
                            reverse_list(blossom_path)

                        new_path = path[:i] + blossom_path + [leave_edge] + path[i + 1 :] + [-1]

                        #---
                        animate_augment_path(context.self, context.graph, unfuk_path(new_path[:-1], context))
                        context.self.play(*[context.graph.vertices[v].animate.move_to(original_positions[i]) for i, v in enumerate(vertices)])
                        #---

                        return new_path
                else:
                    pass  # do nothing!

            marked.add((v, w))

        marked.add(v)

    return []


def improve_matching(graph: MyGraph, matching: List[Edge], context) -> List[Edge]:
    """Attempt to improve the given matching in the graph."""
    path = find_augmenting_path(graph, matching, context)

    improved_matching = list(matching)
    already_animated = False
    if path != []:
        # hack to not augment twice
        if path[-1] == -1:
            path.pop()
            already_animated = True

        new_path = unfuk_path(path, context)

        if not already_animated:
            animate_augment_path(context.self, context.graph, new_path)

        for i, e in enumerate(path):
            # a bit of a hack since the edges are all messed up
            if e not in graph[1]:
                e = (e[1], e[0])

            if i % 2 == 0:
                improved_matching.append(e)
            else:
                improved_matching.remove(e)

    return improved_matching



def get_maximum_matching(graph: MyGraph, context) -> List[Edge]:
    """Find the maximum matching in a graph."""
    matching = []

    animate_correct_graph_color(context.self, context.graph, [])
    while True:
        improved_matching = improve_matching(graph, matching, context)

        if matching == improved_matching:
            return matching

        matching = improved_matching

#--------------------------------
#--------------------------------
#--------------------------------
#--------------------------------
#--------------------------------



class Blossom(Scene):
    @fade
    def construct(self):
        @dataclass
        class Context:
            graph: MyGraph
            self: Blossom
            code: 'typing.Any'
            set_lines: 'typing.Any'

        g = parse_graph(
            """
5 0 <-16.05615947107685, -12.504911246689693> <-14.446419714646854, -6.866013725874188>
0 8 <-14.446419714646854, -6.866013725874188> <-16.42527207725241, -1.8140283988138854>
12 0 <-19.64155534824222, -7.330631498406216> <-14.446419714646854, -6.866013725874188>
1 3 <-4.698194206378598, 0.11011604485983129> <-10.209550409185647, -2.9552644219000106>
1 10 <-4.698194206378598, 0.11011604485983129> <0.9003340177597777, -2.5845025309871477>
3 2 <-10.209550409185647, -2.9552644219000106> <-10.670793355913192, -9.290296998392101>
5 2 <-16.05615947107685, -12.504911246689693> <-10.670793355913192, -9.290296998392101>
3 8 <-10.209550409185647, -2.9552644219000106> <-16.42527207725241, -1.8140283988138854>
4 6 <-1.0383909201343497, -12.64149137008625> <-7.062170194186263, -14.061899786709596>
4 7 <-1.0383909201343497, -12.64149137008625> <3.324971894939845, -8.293802236457113>
4 11 <-1.0383909201343497, -12.64149137008625> <-3.3577054035744847, -6.997621303069259>
12 5 <-19.64155534824222, -7.330631498406216> <-16.05615947107685, -12.504911246689693>
7 9 <3.324971894939845, -8.293802236457113> <7.465014371318295, -3.8180621675279958>
10 7 <0.9003340177597777, -2.5845025309871477> <3.324971894939845, -8.293802236457113>
12 8 <-19.64155534824222, -7.330631498406216> <-16.42527207725241, -1.8140283988138854>
8 13 <-16.42527207725241, -1.8140283988138854> <-12.470684295924984, 2.950307523065462>
10 11 <0.9003340177597777, -2.5845025309871477> <-3.3577054035744847, -6.997621303069259>
10 14 <0.9003340177597777, -2.5845025309871477> <5.227801852655065, 1.8530677198156864>
                """,
            s=0.065,
            t=-0.070,
        ).scale(GRAPH_SCALE * NODE_SCALE).rotate_in_place(-PI / 2).shift(3.3 * RIGHT)

        code_str = """def find_augmenting_path(v):
    bfs.start_from_vertex(v)
    while bfs.has_unexplored_vertices():
        bfs.add_vertices_not_in_matching()

        if bfs.found_blossom():
            bfs.contract_blossom()
            find_augmenting_path(v)
            bfs.lift_blossom()

        if bfs.found_augmenting_path():
            return bfs.augmenting_path

        bfs.add_vertices_in_matching()


    return []

def improve_matching(G):
    for v in exposed_vertices(G):
        path = find_augmenting_path(v)

        if path != []:
            switch_augmenting_path(path)
            return True

    return False

while True:
    if not improve_matching(G):
        break"""

        code = Code(code=code_str, font="Fira Mono", line_spacing=0, style="Monokai", language="python")
        code.background_mobject[0].set_opacity(0)
        code.scale(0.55).shift(2.8 * LEFT)

        c = 0.075

        for i in range(1, len(code.code)):
            code.code[i].shift(i * DOWN * c)
            code.line_numbers[i].shift(i * DOWN * c)

        code.shift(UP * len(code.code) * c / 2)

        frame = SurroundingRectangle(code, color=WHITE, stroke_width=2)
        frame.round_corners(0.2).shift(DOWN * 0.1)

        self.play(Write(code), Write(g), Write(frame))

        M = []

        def set_lines(self, code, lines, previous_lines=[]):
            # by default, the code has all lines highligted
            if previous_lines == []:
                for i in range(len(code.code_string.splitlines())):
                    previous_lines.append(i + 1)
                    code.code.chars[i - 1].save_state()

            # lines newly highlighted
            new_lines = [l for l in lines if l not in previous_lines]

            # lines that will disappear
            dis_lines = [l for l in previous_lines if l not in lines]

            for l in dis_lines:
                code.code.chars[l - 1].save_state()

            new_lines_animation = [code.line_numbers[i - 1].animate.set_color(WHITE) for i in new_lines] + \
                                  [code.code.chars[i - 1].animate.restore() for i in new_lines]
            dis_lines_animation = [code.line_numbers[i - 1].animate.set_color(HIDDEN_COLOR) for i in dis_lines] + \
                                  [code.code.chars[i - 1].animate.set_color(HIDDEN_COLOR) for i in dis_lines]

            while len(previous_lines) != 0:
                previous_lines.pop()

            for e in lines:
                previous_lines.append(e)

            return new_lines_animation + dis_lines_animation

        # I ran out of time making the algorithm general, so this is a simulated run
        # :C
        self.play(*set_lines(self, code, [6, 7, 8, 9]))

        self.play(*set_lines(self, code, [i + 1 for i in range(len(code.code))]))

        operations = [
            ("R", None),
            ("I", 8),
            ("B", [(8, 0), (8, 12), (8, 3), (8, 13)]),
            ("A", [(8, 12)]),
            ("I", 1),
            ("B", [(1, 3), (1, 10)]),
            ("A", [(1, 10)]),
            ("I", 3),
            ("B", [(3, 8), (3, 2), (3, 1)]),
            ("A", [(3, 2)]),
            ("I", 4),
            ("B", [(4, 11), (4, 6), (4, 7)]),
            ("A", [(4, 11)]),
            ("I", 5),
            ("B", [(5, 0), (5, 12), (5, 2)]),
            ("A", [(5, 0)]),
            ("I", 9),
            ("B", [(9, 7)]),
            ("A", [(9, 7)]),
            ("I", 14),
            ("B", [(14, 10)]),
            ("BO", [(1, 10)]),
            ("B", [(1, 3)]),
            ("BO", [(3, 2)]),
            ("B", [(2, 5)]),
            ("BO", [(5, 0)]),
            ("B", [(0, 8), (0, 12)]),
            ("BO", [(8, 12)]),
            ("C", [0, 8, 12]),
            ("R", None),
            ("I", 14),
            ("B", [(14, 10)]),
            ("BO", [(1, 10)]),
            ("B", [(1, 3)]),
            ("BO", [(3, 2)]),
            ("B", [(2, 5)]),
            ("BO", [(5, 0), (0, 8), (0, 12), (8, 12)]),
            ("B", [(8, 13)]),
            ("A", [(14, 10), (10, 1), (1, 3), (3, 2), (2, 5), (5, 0), (0, 12), (12, 8), (8, 13)]),
            ("U", [0, 8, 12]),
            ("I", 6),
            ("B", [(6, 4)]),
            ("BO", [(4, 11)]),
            ("B", [(11, 10)]),
            ("BO", [(14, 10)]),
            ("Q", None),
            ("RR", None),
        ]

        fk = (12, 5)
        g.add_to_back(g.edges[fk if fk in g.edges else (fk[1], fk[0])])

        for operation, argument in operations:
            if operation == "R":
                animate_correct_graph_color(self, g, M)

            if operation == "RR":
                animate_correct_graph_color(self, g, M, lambda x, y, z: [], None, add_animations=lambda: set_lines(self, code, [i + 1 for i in range(len(code.code))]))

            if operation == "I":
                self.play(
                    Circumscribe(g.vertices[argument], Circle, color=BFS_COLOR),
                    g.vertices[argument].animate.set_color(BFS_COLOR),
                    *set_lines(self, code, [20]),
                )

                self.play(*set_lines(self, code, [21]))
                self.play(*set_lines(self, code, [2]))
                self.play(*set_lines(self, code, [3]))

            if operation[0] == "B":
                self.play(
                    *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(argument)],
                    *[g.edges[e if e in g.edges else (e[1], e[0])].animate.set_color(BFS_COLOR) for e in argument],
                    *set_lines(self, code, [4 if operation == "B" else 14]),
                )

            if operation == "A":
                augmenting_path =[(e if e in g.edges else (e[1], e[0])) for e in argument]

                animate_augment_path(self, g,
                        augmenting_path,
                            add_animations_first=lambda: set_lines(self, code, [11, 12]),
                            add_animations_second=lambda: set_lines(self, code, [23, 24, 25])
                        )

                # improve M
                for i in range(0, len(augmenting_path), 2):
                    M.append(augmenting_path[i])
                for i in range(1, len(augmenting_path), 2):
                    M.remove(augmenting_path[i])

                # dirty hack alert!
                set_lines(self, code, [23, 24, 25])

                animate_correct_graph_color(self, g, M)

            if operation == "C":
                small_random = [1 + i / 10000 for i in range(len(argument))]

                average = sum(g.vertices[v].get_center() for v in argument) / len(argument)

                original_vertices = argument
                original_positions = [g.vertices[v].get_center() for v in argument]

                self.play(
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[0]), g.vertices[0]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[1]), g.vertices[8]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[2]), g.vertices[12]),
                    *set_lines(self, code, [6, 7]),
                )

                self.play(*set_lines(self, code, [8]))

            if operation == "U":
                self.play(
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[0]), g.vertices[0]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[1]), g.vertices[8]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[2]), g.vertices[12]),
                    *set_lines(self, code, [9]),
                )

            if operation == "Q":
                self.play(*set_lines(self, code, [17]), run_time=SHORT_CODE_PAUSE)
                self.play(*set_lines(self, code, [27]), run_time=SHORT_CODE_PAUSE)
                self.play(*set_lines(self, code, [31]), run_time=SHORT_CODE_PAUSE)


class Overview(Scene):
    @fade
    def construct(self):
        naive = Tex(r"Naïve").shift(UP * 1.7 + RIGHT * 3.35)
        naive_o = Tex("– $\mathcal{O}(2^{e})$")
        naive_o_combined = Tex("Naïve – $\mathcal{O}(2^{e})$").move_to(naive.get_center())

        blossom = Tex(r"Blossom").shift(UP * 1.7 + LEFT * 3.35)
        blossom_o = Tex("– $\mathcal{O}(e \cdot v^2)$")
        blossom_o_combined = Tex("Blossom – $\mathcal{O}(e \cdot v^2)$").move_to(blossom.get_center())

        g_naive = parse_graph(
            """
1 2 <5.305295407371162, -9.00109716204681> <-0.6729840226655002, -10.4461242684385>
3 2 <-0.8425669826207631, -16.51162542950073> <-0.6729840226655002, -10.4461242684385>
3 4 <-0.8425669826207631, -16.51162542950073> <-6.220565179720084, -13.23694362201735>
2 4 <-0.6729840226655002, -10.4461242684385> <-6.220565179720084, -13.23694362201735>
4 5 <-6.220565179720084, -13.23694362201735> <-11.791437508380174, -10.273211500280336>
4 6 <-6.220565179720084, -13.23694362201735> <-11.558874566262684, -16.33719898830283>
5 6 <-11.791437508380174, -10.273211500280336> <-11.558874566262684, -16.33719898830283>
4 7 <-6.220565179720084, -13.23694362201735> <-6.896308576133831, -7.119926197187177>
3 8 <-0.8425669826207631, -16.51162542950073> <5.2015048653161315, -15.125611531890883>
1 8 <5.305295407371162, -9.00109716204681> <5.2015048653161315, -15.125611531890883>
5 9 <-11.791437508380174, -10.273211500280336> <-17.56869374575382, -12.311184072704405>
5 10 <-11.791437508380174, -10.273211500280336> <-16.13459349493921, -5.841431825927536>
2 11 <-0.6729840226655002, -10.4461242684385> <-1.826409248537547, -4.402336655405>
                """,
            s=0.08 / NODE_SCALE,
            t=-0.08 / NODE_SCALE,
        ).scale(GRAPH_SCALE * NODE_SCALE).shift(DOWN)

        g_blossom = parse_graph(
            """
1 2 <5.305295407371162, -9.00109716204681> <-0.6729840226655002, -10.4461242684385>
3 2 <-0.8425669826207631, -16.51162542950073> <-0.6729840226655002, -10.4461242684385>
3 4 <-0.8425669826207631, -16.51162542950073> <-6.220565179720084, -13.23694362201735>
2 4 <-0.6729840226655002, -10.4461242684385> <-6.220565179720084, -13.23694362201735>
4 5 <-6.220565179720084, -13.23694362201735> <-11.791437508380174, -10.273211500280336>
4 6 <-6.220565179720084, -13.23694362201735> <-11.558874566262684, -16.33719898830283>
5 6 <-11.791437508380174, -10.273211500280336> <-11.558874566262684, -16.33719898830283>
4 7 <-6.220565179720084, -13.23694362201735> <-6.896308576133831, -7.119926197187177>
3 8 <-0.8425669826207631, -16.51162542950073> <5.2015048653161315, -15.125611531890883>
1 8 <5.305295407371162, -9.00109716204681> <5.2015048653161315, -15.125611531890883>
5 9 <-11.791437508380174, -10.273211500280336> <-17.56869374575382, -12.311184072704405>
5 10 <-11.791437508380174, -10.273211500280336> <-16.13459349493921, -5.841431825927536>
2 11 <-0.6729840226655002, -10.4461242684385> <-1.826409248537547, -4.402336655405>
                """,
            s=0.08 / NODE_SCALE,
            t=-0.08 / NODE_SCALE,
        ).scale(GRAPH_SCALE * NODE_SCALE).shift(DOWN)

        from itertools import chain, combinations

        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

        good_subsets = []
        for subset in powerset(g_naive.edges):
            bad = False
            for a, b in subset:
                for c, d in subset:
                    if (a, b) == (c, d):
                        continue

                    if a == c or a == d or b == c or b == d:
                        bad = True

            if bad:
                continue

            good_subsets.append(list(subset))

        g_blossom.next_to(blossom, DOWN, 0.8)
        self.play(Write(blossom), Write(g_blossom))

        g_naive.next_to(naive, DOWN, 0.8)
        self.play(Write(naive), Write(g_naive))

        animation_runtime = 0.06

        for subset in good_subsets:
            g = g_naive
            self.play(
                *[
                    ApplyFunction(lambda x: match_edge(x), g.edges[e])
                    for e in subset
                ],
                *[
                    ApplyFunction(lambda x: unmatch_edge(x), g.edges[e])
                    for e in g.edges if e not in subset
                ],
                *[g.vertices[v].animate.set_color(MATCHING_COLOR) for v in edgesToVertices(subset)],
                *[g.vertices[v].animate.set_color(EXPOSED_COLOR) for v in g.vertices if v not in edgesToVertices(subset)],
                run_time=animation_runtime
            )

        animation_runtime *= 3

        diff = (-naive[0][0].get_center() + naive_o_combined[0][0].get_center())

        self.play(naive.animate.shift(diff))
        naive_o.next_to(naive, RIGHT)
        self.play(Write(naive_o))

        diff = (-blossom[0][0].get_center() + blossom_o_combined[0][0].get_center())

        g = g_blossom
        M = []
        i = 0
        while True:
            if i == 0:
                animate_correct_graph_color(self, g, M, lambda x, y, z: [], None)
                i += 1
            else:
                animate_correct_graph_color(self, g, M, lambda x, y, z: [], None, run_time=animation_runtime)

            result = animate_tree_algorithm_iteration(self, g, M, lambda x, y, z: [], None, run_time=animation_runtime, no_code=True)

            if not result:
                break

        animate_correct_graph_color(self, g, M, lambda x, y, z: [], None, run_time=animation_runtime)

        self.play(blossom.animate.shift(diff))
        blossom_o.next_to(blossom, RIGHT)
        self.play(Write(blossom_o))

class Title(Scene):
    @fade
    def construct(self):
        text = Tex(r"\Large The Blossom algorithm").scale(1.3)
        i = 5
        text[0][i].set_color(BLACK)

        S = 1.2

        self.play(
            LaggedStart(
                Write(text.scale(S)),
                Write(SVGMobject("flower.svg").scale(0.225).move_to(text[0][i]).shift(LEFT * 0.02).scale(S), run_time=0.3),
                lag_ratio=0.2,
            )
        )

class Outro(Scene):
    @fade
    def construct(self):
        g = parse_graph(
            """
0 1 <16.41082561017643, 4.667526176613917> <10.84069307855083, 7.503968161787933>
1 15 <10.84069307855083, 7.503968161787933> <4.541887477921455, 8.254448675626461>
2 5 <-1.196230366996346, 5.4090795936312865> <-6.619254653629823, 1.7609337636785525>
2 10 <-1.196230366996346, 5.4090795936312865> <3.816531484644093, 1.7352935181536813>
15 2 <4.541887477921455, 8.254448675626461> <-1.196230366996346, 5.4090795936312865>
3 14 <15.86879364092038, -9.39849234273218> <9.939049668936683, -11.536515478495724>
4 6 <-0.6313440444305729, -6.6657958940717155> <5.039718780660546, -4.2902764515477605>
4 7 <-0.6313440444305729, -6.6657958940717155> <-6.4928860212702615, -4.787834235204335>
4 9 <-0.6313440444305729, -6.6657958940717155> <-1.7957609981445226, -0.806513806341758>
5 7 <-6.619254653629823, 1.7609337636785525> <-6.4928860212702615, -4.787834235204335>
5 8 <-6.619254653629823, 1.7609337636785525> <-10.651125829909375, 6.550841780969295>
5 16 <-6.619254653629823, 1.7609337636785525> <-11.785738650858029, -1.5835479095931102>
10 6 <3.816531484644093, 1.7352935181536813> <5.039718780660546, -4.2902764515477605>
6 12 <5.039718780660546, -4.2902764515477605> <11.059397566311196, -5.512977312597954>
7 9 <-6.4928860212702615, -4.787834235204335> <-1.7957609981445226, -0.806513806341758>
7 11 <-6.4928860212702615, -4.787834235204335> <-12.098487635168565, -7.615515657229979>
7 16 <-6.4928860212702615, -4.787834235204335> <-11.785738650858029, -1.5835479095931102>
7 19 <-6.4928860212702615, -4.787834235204335> <-2.8286604281628853, -10.234945141734263>
10 9 <3.816531484644093, 1.7352935181536813> <-1.7957609981445226, -0.806513806341758>
10 18 <3.816531484644093, 1.7352935181536813> <10.072341264393968, 1.4997616137359333>
16 11 <-11.785738650858029, -1.5835479095931102> <-12.098487635168565, -7.615515657229979>
12 17 <11.059397566311196, -5.512977312597954> <15.546018749458295, -1.4101212844618582>
14 13 <9.939049668936683, -11.536515478495724> <3.5146419854002207, -11.66621030177497>
19 13 <-2.8286604281628853, -10.234945141734263> <3.5146419854002207, -11.66621030177497>
18 17 <10.072341264393968, 1.4997616137359333> <15.546018749458295, -1.4101212844618582>
                """,
            s=0.09,
            t=-0.08,
        ).scale(GRAPH_SCALE * NODE_SCALE)

        @dataclass
        class Context:
            graph: MyGraph
            self: Outro

        self.play(Write(g))

        g_structure = ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [(0, 1), (1, 15), (2, 5), (2, 10), (2, 15), (3, 14), (4, 6), (4, 7), (4, 9), (5, 7), (5, 8), (5, 16), (6, 10), (6, 12), (7, 9), (7, 11), (7, 16), (7, 19), (9, 10), (10, 18), (11, 16), (12, 17), (13, 14), (13, 19), (17, 18)])

        operations = [
            ("R", None),
            ("I", 0),
            ("B", [(0, 1)]),
            ("A", [(0, 1)]),
            ("I", 2),
            ("B", [(2, 10), (2, 15), (2, 5)]),
            ("A", [(2, 10)]),
            ("I", 14),
            ("B", [(14, 3), (14, 13)]),
            ("A", [(14, 3)]),
            ("I", 9),
            ("B", [(9, 10), (9, 7), (9, 4)]),
            ("A", [(9, 4)]),
            ("I", 5),
            ("B", [(5, 8), (5, 16), (5, 2), (5, 7)]),
            ("A", [(5, 8)]),
            ("I", 12),
            ("B", [(12, 6), (12, 17)]),
            ("A", [(6, 12)]),
            ("I", 7),
            ("B", [(7, 4), (7, 9), (7, 11), (7, 5), (7, 16), (7, 19)]),
            ("A", [(16, 7)]),
            ("I", 11),
            ("B", [(11, 7), (11, 16), (7, 16)]),
            ("C", [11, 7, 16]),
            ("R", None),
            ("I", 11),
            ("B", [(16, 5), (7, 9), (7, 4), (7, 19)]),
            ("A", [(11, 16), (16, 7), (7, 19)]),
            ("U", [11, 7, 16]),
            ("I", 17),
            ("B", [(17, 18), (17, 12)]),
            ("A", [(17, 18)]),
            ("I", 13),
            ("B", [(13, 14), (13, 19)]),
            ("BO", [(19, 7)]),
            ("B", [(7, 4), (7, 9), (7, 5), (7, 16), (7, 11)]),
            ("BO", [(5, 8), (4, 9), (11, 16)]),
            ("CC", [7, 4, 9]),
            ("R", None),
            ("I", 15),
            ("B", [(15, 2), (15, 1)]),
            ("BO", [(2, 10), (1, 0)]),
            ("B", [(10, 9), (10, 18), (10, 6), (9, 4), (4, 7)]),
            ("BO", [(6, 12), (18, 17), (7, 19)]),
            ("B", [(12, 17), (19, 13)]),
            ("A", [(15, 2), (2, 10), (10, 9), (9, 4), (4, 7), (7, 19), (19, 13)]),
            ("UU", [7, 4, 9]),
            ("R", None),
        ]

        g.add_to_back(g.vertices[7])
        g.add_to_back(g.vertices[16])

        M = []

        for operation, argument in operations:
            if operation == "R":
                animate_correct_graph_color(self, g, M)

            if operation == "I":
                self.play(
                    Circumscribe(g.vertices[argument], Circle, color=BFS_COLOR),
                    g.vertices[argument].animate.set_color(BFS_COLOR),
                )

            if operation[0] == "B":
                self.play(
                    *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(argument)],
                    *[g.edges[e if e in g.edges else (e[1], e[0])].animate.set_color(BFS_COLOR) for e in argument],
                )

            if operation == "A":
                augmenting_path =[(e if e in g.edges else (e[1], e[0])) for e in argument]

                animate_augment_path(self, g, augmenting_path)

                # improve M
                for i in range(0, len(augmenting_path), 2):
                    M.append(augmenting_path[i])
                for i in range(1, len(augmenting_path), 2):
                    M.remove(augmenting_path[i])

                animate_correct_graph_color(self, g, M)

            if operation == "C":
                small_random = [1 + i / 10000 for i in range(len(argument))]

                average = sum(g.vertices[v].get_center() for v in argument) / len(argument)

                original_vertices = argument
                original_positions = [g.vertices[v].get_center() for v in argument]

                self.play(
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[0]), g.vertices[11]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[1]), g.vertices[7]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[2]), g.vertices[16]),
                )

            if operation == "CC":
                small_random = [1 + i / 10000 for i in range(len(argument))]

                average = sum(g.vertices[v].get_center() for v in argument) / len(argument)

                original_vertices = argument
                original_positions = [g.vertices[v].get_center() for v in argument]

                self.play(
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[0]), g.vertices[7]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[1]), g.vertices[4]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[2]), g.vertices[9]),
                )

            if operation == "U":
                self.play(
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[0]), g.vertices[11]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[1]), g.vertices[7]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[2]), g.vertices[16]),
                )

            if operation == "UU":
                self.play(
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[0]), g.vertices[7]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[1]), g.vertices[4]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[2]), g.vertices[9]),
                )
