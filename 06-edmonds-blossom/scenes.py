from utilities import *
from mm import *


def visualizeBipariteBlossom(graph, pairing=[]):
    """Visualize the blossom algorithm for a bipartite graph."""


PAIRING_COLOR = YELLOW
EXPOSED_COLOR = ORANGE
AUGMENTING_COLOR = RED
BFS_COLOR = BLUE

MATCHED_WIDTH = 15


def match_edge(mob, change_color=True):
    mob.set_stroke_width(MATCHED_WIDTH)

    if change_color:
        mob.set_color(PAIRING_COLOR)

    return mob


def unmatch_edge(mob, change_color=True):
    mob.set_stroke_width(4)

    if change_color:
        mob.set_color(WHITE)

    return mob


def animate_augment_path(self, g, path, add_animations_first=None, add_animations_second=None):
    A = path
    AV = edgesToVertices(A)

    self.play(
        *([] if add_animations_first is None else add_animations_first),
        *[g.edges[e].animate.set_color(AUGMENTING_COLOR) for e in A],
        *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for v, _ in A],
        *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for _, v in A],
    )

    self.play(
        *([] if add_animations_second is None else add_animations_second),
        *[
            ApplyFunction(lambda x: match_edge(x, change_color=False), g.edges[e])
            for e in A[::2]
        ],
        *[
            ApplyFunction(lambda x: unmatch_edge(x, change_color=False), g.edges[e])
            for e in A[1::2]
        ],
    )

    self.play(
        *[g.edges[e].animate.set_color(PAIRING_COLOR) for e in A[::2]],
        *[g.edges[e].animate.set_color(WHITE) for e in A[1::2]],
        *[g.vertices[v].animate.set_color(PAIRING_COLOR) for v, _ in A[::2]],
        *[g.vertices[v].animate.set_color(PAIRING_COLOR) for _, v in A[::2]],
    )


def animate_correct_graph_color(self, g, M, set_lines, code):
    MV = edgesToVertices(M)

    self.play(
        *set_lines(self, code, [16], len(code.code_string.splitlines())),
        *[g.edges[e].animate.set_color(WHITE) for e in g.edges if e not in M],
        *[g.edges[e].animate.set_color(PAIRING_COLOR) for e in g.edges if e in M],
        *[
            g.vertices[v].animate.set_color(EXPOSED_COLOR)
            for v in g.vertices
            if v not in MV
        ],
        *[
            g.vertices[v].animate.set_color(PAIRING_COLOR)
            for v in g.vertices
            if v in MV
        ],
    )


def neighbours(v, edges):
    t = []
    for e in edges:
        if v in e:
            t.append(e)
    return [a for a in edgesToVertices(t) if a != v]


class Intro(Scene):
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
            s=0.13,
            t=0.13,
        ).scale(1.3)

        self.play(Write(g))

        M = [(1, 2), (8, 13), (5, 12)]
        MV = edgesToVertices(M)

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in M],
            *[g.vertices[v].animate.set_color(PAIRING_COLOR) for v, _ in M],
            *[g.vertices[v].animate.set_color(PAIRING_COLOR) for _, v in M],
        )

        MP = getMaximalPairing(list(g.edges))
        MPV = edgesToVertices(MP)

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in MP if e not in M],
            *[
                g.vertices[v].animate.set_color(PAIRING_COLOR)
                for v, _ in MP
                if v not in MV
            ],
            *[
                g.vertices[v].animate.set_color(PAIRING_COLOR)
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
            s=0.13,
            t=0.13,
        ).scale(1.3)

        self.play(Write(g))

        M = [(5, 8), (6, 10), (2, 4)]
        MV = edgesToVertices(M)

        self.play(
            *[ApplyFunction(match_edge, g.edges[e]) for e in M],
            *[g.vertices[v].animate.set_color(PAIRING_COLOR) for v, _ in M],
            *[g.vertices[v].animate.set_color(PAIRING_COLOR) for _, v in M],
            *[
                g.vertices[v].animate.set_color(EXPOSED_COLOR)
                for v in g.vertices
                if v not in MV
            ],
        )

        animate_augment_path(self, g, [(8, 9), (5, 8), (4, 5), (2, 4), (1, 2)])
        animate_augment_path(self, g, [(10, 11), (6, 10), (3, 6)])
        animate_augment_path(self, g, [(5, 12), (4, 5), (4, 7)])


def edgeFromVertices(v, w, e):
    if (v, w) in e:
        return (v, w)
    return (w, v)


def animate_tree_algorithm_iteration(self, g, M, set_lines, code):
    MV = edgesToVertices(M)
    exposed = [v for v in g.vertices if v not in MV]

    shuffle(exposed)
    shuffle(MV)

    explored = set()

    for v in exposed:
        self.play(
            Circumscribe(g.vertices[v], Circle, color=BFS_COLOR),
            g.vertices[v].animate.set_color(BFS_COLOR),
            *set_lines(self, code, [3], len(code.code_string.splitlines())),
        )

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
                    *set_lines(self, code, [4, 5, 6], len(code.code_string.splitlines())),
                )

                # if it also contains an augmenting path, then animate it
                if augmenting_path is not None:
                    # animate the augmenting path
                    animate_augment_path(self, g, augmenting_path,
                            add_animations_first=set_lines(self, code, [8], len(code.code_string.splitlines())),
                            add_animations_second=set_lines(self, code, [9, 10], len(code.code_string.splitlines()), previous_lines=[8]))

                    set_lines(self, code, [9, 10], len(code.code_string.splitlines()))

                    # improve M
                    for i in range(0, len(augmenting_path), 2):
                        M.append(augmenting_path[i])
                    for i in range(1, len(augmenting_path), 2):
                        M.remove(augmenting_path[i])

                    return True

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

    self.play(*set_lines(self, code, [12], len(code.code_string.splitlines())))
    return False


class Tree(Scene):
    def construct(self):
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
            s=0.06,
            t=0.07,
        ).scale(1.3).shift(3.7 * RIGHT)

        code_str = """def improve_matching(G):
    \"\"\"Attempt to improve a matching in G.\"\"\"
    for v in exposed_vertices(G):
        # internally uses BFS to find alternating
        # layers of edges in and not in matching
        path = find_augmenting_path(v)

        if path is not None:
            switch_augmenting_path(path)
            return True

    return False


while True:
    if not improve_matching(G):
        break"""

        code = Code(code=code_str, font="Fira Mono", line_spacing=0.55, style="Monokai", language="python")
        code.background_mobject[0].set_opacity(0)
        code.scale(0.70).shift(2.6 * LEFT)

        g.rotate_in_place(PI / 2)

        self.play(Write(g), Write(code))

        M = []

        def set_lines(self, code, lines, line_count, previous_lines=[]):
            # by default, the code has all lines highligted
            if previous_lines == []:
                for i in range(line_count):
                    previous_lines.append(i + 1)

            # lines newly highlighted
            new_lines = [l for l in lines if l not in previous_lines]

            # lines that will disappear
            dis_lines = [l for l in previous_lines if l not in lines]

            new_lines_animation = [FadeIn(code.line_numbers[i - 1]) for i in new_lines]
            dis_lines_animation = [FadeOut(code.line_numbers[i - 1]) for i in dis_lines]

            while len(previous_lines) != 0:
                previous_lines.pop()

            for e in lines:
                previous_lines.append(e)

            return new_lines_animation + dis_lines_animation

        seed(2)

        while True:
            animate_correct_graph_color(self, g, M, set_lines, code)

            result = animate_tree_algorithm_iteration(self, g, M, set_lines, code)

            if not result:
                break

        animate_correct_graph_color(self, g, M, set_lines, code)
