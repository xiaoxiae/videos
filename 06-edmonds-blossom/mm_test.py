import mm
import mm_blossom

from networkx import generators

sizes = [5, 15]
iterations = 5
p = 0.1

# TODO: debug, remove
from random import seed
seed(8)

def test_simple():
    while True:
        for n in sizes:
            for _ in range(iterations):
                g = generators.random_graphs.gnp_random_graph(n, p)

                try:
                    a_result = mm.get_maximal_matching(g.edges)
                    b_result = mm_blossom.get_maximal_matching((list(g.nodes), list(g.edges)))
                except Exception as e:
                    print(e)

                    for a, b in g.edges:
                        print(a, b)

                    quit()

                if len(a_result) != len(b_result):
                    if b_result == [-1]:
                        continue

                    print(len(a_result), len(b_result))
                    quit()
                    #print(a, b, (list(g.nodes), list(g.edges)))

def test_full():
    while True:
        for n in sizes:
            for _ in range(iterations):
                g = generators.random_graphs.gnp_random_graph(n, p)

                print((list(g.nodes), list(g.edges)))
                for a, b in g.edges:
                    print(a, b)

                a_result = mm.get_maximal_matching(g.edges)
                b_result = mm_blossom.get_maximal_matching((list(g.nodes), list(g.edges)))

                if len(a_result) != len(b_result):
                    print(len(a_result), len(b_result))

test_full()
