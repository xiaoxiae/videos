from typing import Tuple, List


Vertex = int
Edge = Tuple[Vertex, Vertex]
Graph = Tuple[List[Vertex], List[Edge]]


def neighbours(v: Vertex, graph: Graph) -> List[Vertex]:
    """Return the neighbours of the vertex v in the graph."""
    return [a for a, b in graph[1] if a == v or b == v]


def get_exposed_vertices(graph: Graph, matching: List[Edge]) -> List[Vertex]:
    """Return the exposed vertices of the graph, given a matching."""
    return [v for v in graph[0] \
            if v not in list(set([v for _, v in graph[1]] + [v for v, _ in graph[1]]))]


def find_augmenting_path(graph: Graph, matching: List[Edge]) -> List[Edge]:
    """Find and return an augmenting path in the graph, or [] if there isn't one."""
    parent = {}     # parent[v]... parent of v in the forest
    root_node = {}  # root_node[v]... root node for v
    layer = {}      # layer[v]... which layer is v in

    marked = set(matching)  # marked edges
    queue = get_exposed_vertices(graph, matching)  # unmarked vertices in an even layer

    # add exposed vertices to the forest
    for v in queue:
        parent[v] = v
        root_node[v] = v
        layer[v] = 0

    # run a BFS to add the augmenting paths to the forest
    while :
        v = queue.pop(0)

        for w in neighbours(v, graph):
            # skip the one edge that is in the matching and in the forest
            if (v, w) in matching or (w, v) in matching:
                continue

            # add neighbours of w that are in the matching to the forest
            if w not in forest:
                forest[w] = v
                for x in neighbours(w, graph):
                    if x in matching:
                        forest[x] = w
            else:
                if layer(w, forest) % 2 == 0:
                    if root_node(v, forest) != root_node(w, forest):
                        pass  # TODO: report augmenting path from one forest to another
                    else:
                        pass  # TODO: recursive
                else:
                    pass  # do nothing!

    return []


def improve_matching(graph: Graph, matching: List[Edge]) -> List[Edge]:
    """Attempt to improve the given matching in the graph."""
    path = find_augmenting_path(graph, matching)

    if path != []:
        for i, e in enumerate(path):
            if i % 2 == 0:
                matching.append(e)
            else:
                matching.remove(e)

    return matching


def find_maximal_matching(graph: Graph) -> List[Edge]:
    """Find the maximal matching in a graph."""
    matching = []

    while True:
        improved_matching = improve_matching(graph, matching)

        if matching == improve_matching:
            return matching

        matching = improved_matching

    return matching
