import mm
import mm_blossom

from networkx import generators

sizes = [5, 15, 25, 35]
iterations = 5
p = 0.1

for n in sizes:
    for _ in range(iterations):
        g = generators.random_graphs.gnp_random_graph(n, p)
        
        a = len(mm.get_maximal_matching(g.edges))
        b = len(mm_blossom.get_maximal_matching((list(g.nodes), list(g.edges))))

        if a != b:
            print(a, b, (list(g.nodes), list(g.edges)))
            quit()
