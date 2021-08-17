from typing import Tuple, List

Vertex = int
Edge = Tuple[Vertex, Vertex]
Graph = Tuple[List[Vertex], List[Edge]]


def neighbours(v: Vertex, graph: Graph) -> List[Vertex]:
    """Return the neighbours of the vertex v in the graph."""
    return list(set([a for a, b in graph[1] if b == v]).union(set([b for a, b in graph[1] if a == v])))


def get_exposed_vertices(graph: Graph, matching: List[Edge]) -> List[Vertex]:
    """Return the exposed vertices of the graph, given a matching."""
    return [v for v in graph[0] \
            if v not in list(set([v for _, v in matching] + [v for v, _ in matching]))]

def path_to_root(v, parent):
    path = []
    while parent[v] != v:
        path.append((v, parent[v]))
        v = parent[v]
    return path


def find_augmenting_path(graph: Graph, matching: List[Edge]) -> List[Edge]:
    """Find and return an augmenting path in the graph, or [] if there isn't one."""
    # FOREST:
    parent = {}     # parent[v]... parent of v in the forest
    root_node = {}  # root_node[v]... root node for v
    layer = {}      # layer[v]... which layer is v in

    # start with all exposed vertices as tree roots
    queue = get_exposed_vertices(graph, matching)
    marked = set(matching)

    for v in queue:
        parent[v] = v
        root_node[v] = v
        layer[v] = 0

    # run a BFS to add the augmenting paths to the forest
    while len(queue) != 0:
        v = queue.pop(0)

        # skip marked vertices
        if v in marked:
            continue

        for w in neighbours(v, graph):
            if (v, w) in marked or (w, v) in marked:
                continue

            # add neighbours of w that are in the matching to the forest
            if w not in layer:
                # w is in the forest, so it is matched
                parent[w] = v
                layer[w] = layer[v] + 1
                root_node[w] = root_node[v]

                # find the one vertex it is matched with
                for x in neighbours(w, graph):
                    if (w, x) in matching or (x, w) in matching:
                        parent[x] = w
                        layer[x] = layer[w] + 1
                        root_node[x] = root_node[w]

                        queue.append(x)
            else:
                if layer[w] % 2 == 0:
                    if root_node[v] != root_node[w]:
                        return path_to_root(v, parent) + [(v, w)] + path_to_root(w, parent)
                    else:
                        print("FUCK")
                else:
                    pass  # do nothing!

            marked.add((v, w))

        marked.add(v)

    return []


def improve_matching(graph: Graph, matching: List[Edge]) -> List[Edge]:
    """Attempt to improve the given matching in the graph."""
    path = find_augmenting_path(graph, matching)

    improved_matching = list(matching)
    if path != []:
        for i, e in enumerate(path):
            # a bit of a hack since the edges are all messed up
            if e not in graph[1]:
                e = (e[1], e[0])

            if i % 2 == 0:
                improved_matching.append(e)
            else:
                improved_matching.remove(e)


    return improved_matching


def get_maximal_matching(graph: Graph) -> List[Edge]:
    """Find the maximal matching in a graph."""
    matching = []

    while True:
        improved_matching = improve_matching(graph, matching)

        if matching == improved_matching:
            return matching

        matching = improved_matching
#
#g = ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [(0, 2), (0, 8), (0, 10), (0, 12), (1, 3), (2, 12), (5, 13), (9, 13), (10, 13), (11, 13)])
#print(get_maximal_matching(g))
