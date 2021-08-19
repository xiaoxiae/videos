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

def get_blossom_path(v: Vertex, w: Vertex, parent) -> Tuple[List[Edge], List[Edge]]:
    """Return the two paths from the root of the blossom to the other end."""
    v_path = reverse_list(reverse_tuples(path_to_root(v, parent)))
    w_path = reverse_list(reverse_tuples(path_to_root(w, parent)))

    while len(v_path) != 0 and len(w_path) != 0 and v_path[0] == w_path[0]:
        v_path.pop(0)
        w_path.pop(0)

    return v_path + [(v, w)] + reverse_list(reverse_tuples(w_path))

def get_blossom_vertices(v: Vertex, w: Vertex, parent) -> List[Vertex]:
    """Get the vertices of a blossom from the forest that ends in v, w.
    It is guaranteed that the first vertex is the first common predecessor of v, w (root)."""
    combined_path_vertices = [v for e in get_blossom_path(v, w, parent) for v in e]

    return [combined_path_vertices[0]] + list(set(combined_path_vertices) - {combined_path_vertices[0]})

def get_correct_blossom_edges(v: Vertex, w: Vertex, edges: List[Edge]):
    """Get the correct blossom edges, with the root being v and exit point being w."""
    if v == w:
        return []

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
                        return reverse_list(path_to_root(v, parent)) + [(v, w)] + path_to_root(w, parent)
                    else:
                        vertices = get_blossom_vertices(v, w, parent)

                        # preserve the root as the new vertex
                        new_vertices = list(set(graph[0]) - set(vertices[1:]))

                        # transform all edges that previously went to the blossom to the new single vertex
                        new_edges = [
                            (a if a not in vertices else vertices[0], b if b not in vertices else vertices[0])
                            for a, b in graph[1]
                        ]

                        # remove loops and multi-edges
                        new_edges = [(a, b) for a, b in new_edges if a != b]
                        new_edges = [(a, b) for a, b in new_edges if (b, a) not in new_edges or b < a]

                        # remove removed edges from the matching
                        new_matching = [(a, b) for a, b in matching if a not in vertices[1:] and b not in vertices[1:]]
                        new_graph = (new_vertices, new_edges)

                        path = find_augmenting_path(new_graph, new_matching)

                        # if no path was found, no path lifting will be done
                        if path == []:
                            return []
                        else:
                            edges_in_vertices = []

                            for a, b in path:
                                if a in vertices or b in vertices:
                                    edges_in_vertices.append((a, b))

                            # if the path doesn't cross the blossom, simply return it
                            if len(edges_in_vertices) == 0:
                                return path

                            path = get_blossom_path(v, w, parent)

                            # find the other vertex that the blossom is connected to
                            # it enters through the root and must leave somewhere...
                            #for edge in edges_in_vertices:

                            # TODO: find the vertex where the path leaves
                            # they're both actually in the path

                            # improve the matching by injecting the lifted path
                            # TODO: fix the vertices on the replaced path
                            # print(get_correct_blossom_edges(11, 3, path))

                            quit()
                else:
                    pass  # do nothing!

            marked.add((v, w))

        marked.add(v)

    return []


def improve_matching(graph: Graph, matching: List[Edge]) -> List[Edge]:
    """Attempt to improve the given matching in the graph."""
    path = find_augmenting_path(graph, matching)

    # TODO: debug, remove
    if path == [-1]:
        return [-1]

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

        # TODO: debug, remove
        if improved_matching == [-1]:
            return [-1]

        if matching == improved_matching:
            return matching

        matching = improved_matching

g = ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [(1, 2), (1, 7), (2, 10), (3, 7), (3, 9), (3, 11), (5, 8), (9, 11), (10, 14)])
print(get_maximal_matching(g))
