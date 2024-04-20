
import random

edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"),
         ("B", "E"), ("C", "D"), ("D", "E")]


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

    def generate_random_edges(self, p=0.1):
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                if random.random() < p:
                    self.add_edge(i, j)


