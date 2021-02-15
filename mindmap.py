class Node:
    def __init__(self, indented_line):
        self.t = 'list_item'
        self.d = indented_line.index('# ') # len(indented_line) - len(indented_line.lstrip())
        self.p = {}
        self.v = indented_line[self.d + 1:].strip()
        self.c = []

    def add_children(self, nodes):
        childlevel = nodes[0].d
        while nodes:
            node = nodes.pop(0)
            if node.d == childlevel: # add node as a child
                self.c.append(node)
            elif node.d > childlevel: # add nodes as grandchildren of the last child
                nodes.insert(0,node)
                self.c[-1].add_children(nodes)
            elif node.d <= self.d: # this node is a sibling, no more children
                nodes.insert(0,node)
                return

    def get_leaf_nodes(self):
        leafs = []
        def _get_leaf_nodes(node):
            if node is not None:
                if len(node.c) == 0:
                    leafs.append(node)
                for n in node.c:
                    _get_leaf_nodes(n)
        _get_leaf_nodes(self)
        return leafs
    
    def pruneLeafs(self):
        for node in self.get_leaf_nodes():
            delattr(node,'c')


def buildMindmapTree(content, pageTitle):
    import json
    mmTree = Node('# ' + pageTitle)
    mmTree.add_children([Node(line) for line in content.splitlines() if line.strip() and line.startswith('#')])
    mmTree.pruneLeafs()
    return mmTree

