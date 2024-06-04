class Edge:
    # todo: add documentation
    def __init__(self, a_node, z_node, weight=None):
        self.beg = a_node
        self.end = z_node
        self.weight = weight


class Node:
    # todo: add documentation
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.visited = False
        self.depth = 0
        self.edges = {}
        self._ins = set()

    def add_child(self, node: 'Node', weight=None):
        edge = Edge(self, node, weight)
        self.edges[node] = edge
        node._ins.add(self)

    def add_parent(self, node: 'Node', weight=None):
        edge = Edge(node, self, weight)
        node.edges[self] = edge
        self._ins.add(edge)

    @property
    def in_deg(self):
        return len(self._ins)

    @property
    def out_deg(self):
        return len(self.edges)


class Graph:
    # todo: add documentation
    def __init__(self):
        self.nodes = []
        self.fun = lambda x: x
        self._prefix = '   '
        self.root = None

    def directed(self, from_node: Node, to_node: Node, weight=None):
        from_node.add_child(to_node, weight)

    def _refresh(self):
        for node in self.nodes:
            node._visited = False

    def print(self):
        self._refresh()
        for node in self.nodes:
            if not node.visited:
                self._print(node)

    def _print(self, node, i=0):
        if node.visited:
            return

        node.visited = True
        print(i * self._prefix + node.name)

        for next_node in node.edges:
            self._print(next_node, i + 1)

        return
