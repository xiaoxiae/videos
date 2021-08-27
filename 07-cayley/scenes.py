from utilities import *

GRAPH_SCALE = 3.2

class Definitions(Scene):
    def construct(self):
        n_min = 4
        n_max = 7 + 1

        layout_graphs = [Graph([i for i in range(n)],
            [(i, j) for i in range(n) for j in range(n) if i != j],
            layout="circular", layout_scale=0.7).scale(GRAPH_SCALE)
            for n in range(n_min, n_max)]

        layout_graph_texts = [Tex(f"$K_{n}$").shift(UP * 2.05 + RIGHT * 2.4).scale(1.3) for n in range(n_min, n_max)]

        g = Graph([i for i in range(n_max)],
            [(i, j) for i in range(n_max) for j in range(n_max) if i != j]).scale(GRAPH_SCALE)

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
