#from manim import *
from math import comb
from itertools import combinations


def edgesToVertices(edges):
    return list(set([u for u, v in edges] + [v for u, v in edges]))

def neighbours(v, E):
    """Return the neighbours of v in E."""
    t = []
    for e in E:
        if v in e:
            t.append(e)
    return [a for a in edgesToVertices(t) if a != v]


def components(V, E):
    """Calculate the number of components of the graph."""
    total = 0
    explored = set()
    for v in V:
        if v in explored:
            continue

        queue = [v]
        explored.add(v)
        total += 1
        while len(queue) != 0:
            v = queue.pop(0)

            for w in neighbours(v, E):
                if w not in explored:
                    explored.add(w)
                    queue.append(w)

    return total



def tutte(V, E):
    """Return the Tutte polynomial of the graph."""
    x_coefficients = []
    y_coefficients = []

    def _coefficients(n):
        return [(-1) ** (n - i) * comb(n, i) for i in range(n + 1)]

    def _add_to_coefficient(c, add):
        for i in range(min(len(c), len(add))):
            c[i] += add[i]

        for i in range(len(c), len(add)):
            c.append(add[i])

    c_e = components(V, E)
    for k in range(len(E)+1):

        for F in combinations(E, k):
            c_f = components(V, F)

            r_e = len(V) - c_e
            r_f = len(V) - c_f
            n_f = len(F) - r_f

            x_c = _coefficients(r_e - r_f)
            y_c = _coefficients(n_f)

            _add_to_coefficient(x_coefficients, x_c)
            _add_to_coefficient(y_coefficients, y_c)

    return x_coefficients, y_coefficients

print(tutte([0, 1, 2, 3, 4], [(0, 1), (1, 2), (1, 3), (2, 3), (3, 4)]))
quit()


class Intro(MovingCameraScene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY

        text = Tex("\Huge Intro")

        self.play(Write(text))
        self.play(FadeOut(text))
