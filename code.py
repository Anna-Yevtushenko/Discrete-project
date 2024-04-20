import matplotlib.pyplot as plt
import networkx as nx
import random

class Graph:
    def __init__(self, Nodes=None, is_directed=False, num_vertices=0):
        self.nodes = self.__get_nodes(Nodes, num_vertices)
        self.adj_list = {}
        self.is_directed = is_directed

        for node in self.nodes:
            self.adj_list[node] = []

    def __get_nodes(self, Nodes, num_vertices):
        if Nodes is not None:
            return Nodes
        return self.__generate_nodes(num_vertices)

    def __generate_nodes(self, num_vertices):
        nodes = []
        for i in range(num_vertices):
            nodes.append(i)
        return nodes

    def add_edge(self, v, e):
        self.adj_list[v].append(e)
        if not self.is_directed:
            self.adj_list[e].append(v)

    def degree_vertex(self, node):
        degree = len(self.adj_list[node])
        return degree

    def print_adj(self):
        for node in self.nodes:
            print(node, ":", self.adj_list[node])

    def remove_edge(self, v, e):
        if e in self.adj_list[v]:
            self.adj_list[v].remove(e)
        if not self.is_directed:
            if v in self.adj_list[e]:
                self.adj_list[e].remove(v)

    def remove_vertex(self, node):
        if node in self.adj_list:
            # Remove all edges from other vertices to this node
            for adjacent in list(self.adj_list[node]):
                self.adj_list[adjacent].remove(node)
            # Finally, remove the vertex itself
            del self.adj_list[node]
            self.nodes.remove(node)

    def generate_connected_graph(self):
        # Ensure the graph is not empty
        if len(self.nodes) == 0:
            return
        for i in range(len(self.nodes) - 1):
            self.add_edge(self.nodes[i], self.nodes[i + 1])
        for i in range(len(self.nodes)):
            for j in range(i + 2, len(self.nodes)):
                if random.random() < 0.1:
                    self.add_edge(self.nodes[i], self.nodes[j])

    def visualize_graph(self):
        G = nx.DiGraph() if self.is_directed else nx.Graph()
        for node in self.nodes:
            G.add_node(node)
        for node, edges in self.adj_list.items():
            for edge in edges:
                G.add_edge(node, edge)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=500, font_size=16, font_weight='bold')
        plt.show()


# graph = Graph(nodes, is_directed=False)
graph = Graph(None, is_directed=False, num_vertices=25)
graph.generate_connected_graph()
graph.print_adj()
graph.visualize_graph()
