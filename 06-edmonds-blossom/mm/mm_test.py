import mm
import mm_blossom

from networkx import generators, algorithms

sizes = [15]
iterations = 5
p = 0.1

from random import seed
seed(1)

while True:
    for n in sizes:
        for _ in range(iterations):
            g = generators.random_graphs.gnp_random_graph(n, p)

            if not algorithms.components.is_connected(g):
                continue

            a_result = mm.get_maximal_matching(g.edges)
            b_result = mm_blossom.get_maximal_matching((list(g.nodes), list(g.edges)))

            if len(a_result) != len(b_result):
                print(len(a_result), len(b_result))
                print(g)

                for a, b in g.edges:
                    print(a, b)
