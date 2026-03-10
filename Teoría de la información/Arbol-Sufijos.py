import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False


class SuffixTree:
    def __init__(self, text):
        self.root = Node()
        self.text = text
        self.build()

    def insert(self, suffix):
        node = self.root

        for char in suffix:
            if char not in node.children:
                node.children[char] = Node()

            node = node.children[char]

        node.is_end = True

    def build(self):
        for i in range(len(self.text)):
            suffix = self.text[i:]
            self.insert(suffix)

            print("Insertando:", suffix)
            draw_tree(self)

def build_graph(node, graph, parent=None, label="root"):
    node_id = id(node)

    graph.add_node(node_id, label=label)

    if parent is not None:
        graph.add_edge(parent, node_id)

    for char, child in node.children.items():
        build_graph(child, graph, node_id, char)


def draw_tree(tree):
    G = nx.DiGraph()

    build_graph(tree.root, G)

    pos = nx.spring_layout(G)

    labels = nx.get_node_attributes(G, "label")

    nx.draw(G, pos, with_labels=False, node_size=2000)
    nx.draw_networkx_labels(G, pos, labels)

    plt.show()

    
tree = SuffixTree("BANANA")
draw_tree(tree)