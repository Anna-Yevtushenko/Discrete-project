import matplotlib.pyplot as plt
import networkx as nx
import random
from heapq import heappop, heappush

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

    def add_edge(self, u, v, w):
        if u not in self.adj_list:
            self.adj_list[u] = []
        self.adj_list[u].append((v, w))
        if not self.is_directed:
            if v not in self.adj_list:
                self.adj_list[v] = []
            self.adj_list[v].append((u, w))

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
            for adjacent in list(self.adj_list[node]):
                self.adj_list[adjacent].remove(node)
            del self.adj_list[node]
            self.nodes.remove(node)

    def generate_connected_graph(self, density):
        if len(self.nodes) == 0:
            return
        for i in range(len(self.nodes) - 1):
            self.add_edge(self.nodes[i], self.nodes[i + 1], random.randint(-10, 10))
        for i in range(len(self.nodes)):
            for j in range(i + 2, len(self.nodes)):
                if random.random() < density:
                    self.add_edge(self.nodes[i], self.nodes[j], random.randint(-10, 10))

    def bellman_ford(self, source):
        distance = {node: float('inf') for node in self.nodes}
        distance[source] = 0

        for _ in range(len(self.nodes) - 1):
            for node in self.nodes:
                for neighbour, weight in self.adj_list[node]:
                    if distance[node] != float('inf') and distance[node] + weight < distance[neighbour]:
                        distance[neighbour] = distance[node] + weight

        for node in self.nodes:
            for neighbour, weight in self.adj_list[node]:
                if distance[node] != float('inf') and distance[node] + weight < distance[neighbour]:
                    print("Graph contains negative weight cycle")
                    return

        return distance

    def dijkstra(self, src, weight):
        D = {node: float('inf') for node in self.nodes}
        D[src] = 0

        heap = [(0, src)]
        while heap:
            d, node = heappop(heap)
            if D[node] != d:
                continue
            for neighbor, w in self.adj_list[node]:
                old_cost = D[neighbor]
                new_cost = D[node] + w + weight[node] - weight[neighbor]
                if new_cost < old_cost:
                    D[neighbor] = new_cost
                    heappush(heap, (new_cost, neighbor))
        return D

    def johnson(self):
        weight = self.bellman_ford(0)
        if weight is None:
            return None
        shortest_paths = {}
        for node in self.nodes:
            shortest_paths[node] = self.dijkstra(node, weight)
        return shortest_paths

    def visualize_graph(self):
        G = nx.DiGraph() if self.is_directed else nx.Graph()
        edge_labels = {}
        for node in self.nodes:
            G.add_node(node)
        for node, edges in self.adj_list.items():
            for edge, weight in edges:
                G.add_edge(node, edge)
                edge_labels[(node, edge)] = weight

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=500, font_size=16, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        plt.show()

def get_user_input():
    start = int(input("Введіть точку початку: "))
    num_vertices = int(input("Введіть кількість вершин: "))
    end = int(input("Введіть точку виходу: "))
    density = float(input("Введіть кофіцієнт щільності: "))
    return start, num_vertices, end, density

start, num_vertices, end, density = get_user_input()

graph = Graph(None, is_directed=True, num_vertices=num_vertices)
graph.generate_connected_graph(density)
graph.print_adj()

distances = graph.bellman_ford(start)
print("Відстані від початкової точки до інших вершин: ", distances)

shortest_paths = graph.johnson()
print("Найкоротші шляхи від кожної вершини до інших: ", shortest_paths)

if end in shortest_paths[start] and shortest_paths[start][end] != float('inf'):
    print("Найкоротший шлях від {} до {}: ".format(start, end), shortest_paths[start][end])
else:
    print("Шлях від {} до {} не існує.".format(start, end))

graph.visualize_graph()
