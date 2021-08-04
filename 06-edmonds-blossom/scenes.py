from utilities import *
from mm import *

def visualizeBipariteBlossom(graph, pairing=[]):
    """Visualize the blossom algorithm for a bipartite graph."""


class Intro(Scene):
    def construct(self):
        g = parse_graph("""
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
                """, s=0.13, t=0.13).scale(1.2)

        self.play(Write(g))

        self.play(*[Indicate(g.vertices[v], scale_factor=1) for v in g.vertices])
        self.play(*[Indicate(g.edges[v], scale_factor=1) for v in g.edges])

        M = [(1, 2), (3, 6), (8, 13), (5, 12)]
        MV = edgesToVertices(M)

        def apply_function(mob):
            mob.set_stroke_width(9)
            mob.set_color(YELLOW)
            return mob

        def unapply_function(mob):
            mob.set_stroke_width(4)
            mob.set_color(WHITE)
            return mob

        self.play(
            *[ApplyFunction(apply_function,g.edges[e]) for e in M],
            *[g.vertices[v].animate.set_color(YELLOW) for v, _ in M],
            *[g.vertices[v].animate.set_color(YELLOW) for _, v in M],
        )

        MP = getMaximalPairing(list(g.edges))
        MPV = edgesToVertices(MP)

        self.play(
            *[ApplyFunction(apply_function,g.edges[e]) for e in MP if e not in M],
            *[g.vertices[v].animate.set_color(YELLOW) for v, _ in MP if v not in MV],
            *[g.vertices[v].animate.set_color(YELLOW) for _, v in MP if v not in MV],
            *[ApplyFunction(unapply_function,g.edges[e]) for e in M if e not in MP],
            *[g.vertices[v].animate.set_color(WHITE) for v, _ in M if v not in MPV],
            *[g.vertices[v].animate.set_color(WHITE) for _, v in M if v not in MPV],
        )
