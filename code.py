import numpy as np
import networkx as nx

class Graph:
    def __init__(self): # Конструктор класу
        self.adjacency_list = {}  #порожній словник для списку суміжності вершин

    def add_vertex(self, vertex):# еметод для додавання вершин
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, u, v, weight):# метод додавання ребра
        if u in self.adjacency_list and v in self.adjacency_list:
            self.adjacency_list[u].append((v, weight))

    def get_adjacent_vertices(self, vertex):#метод отримання списку суміжних
        # вершин для заданої вершини
        if vertex in self.adjacency_list:
            return self.adjacency_list[vertex]
        return []

    def adjacency_matrix(self):
        # метод для створення матриці суміжності
        #графа на основі списків суміжності
        vertices = sorted(self.adjacency_list.keys())
        vertex_count = len(vertices)
        matrix = [[0] * vertex_count for _ in range(vertex_count)]
        vertex_index = {vertex: i for i, vertex in enumerate(vertices)}

        for vertex, neighbors in self.adjacency_list.items():
            for neighbor, weight in neighbors:
                matrix[vertex_index[vertex]][vertex_index[neighbor]] = weight

        return matrix

    def display_adjacency_list(self):#виведення списку суміжності
        for vertex, neighbors in self.adjacency_list.items():
            print(f"Vertex {vertex}: {neighbors}")

#1)Створюємо новий об'єкт класу
#2)Додаємо вершини та ребра

graph = Graph()
graph.add_vertex(1)
graph.add_vertex(2)
graph.add_vertex(3)
graph.add_edge(1, 2, 5)
graph.add_edge(2, 3, 10)
graph.add_edge(1, 3, 7)


#graph.display_adjacency_list()#виведення списку суміжності


# Отримання та виведення матриці суміжності
adj_matrix = graph.adjacency_matrix()
print("\nAdjacency Matrix:")
for row in adj_matrix:
    print(row)


def generate_graph(num_vertices, edge_density, weight_range=(1, 10)):
    max_edges = num_vertices * (num_vertices - 1)
    num_edges = int(edge_density * max_edges)
    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_vertices))

    for _ in range(num_edges):
        u, v = np.random.randint(0, num_vertices, size=2)
        weight = np.random.randint(*weight_range)
        graph.add_edge(u, v, weight=weight)

    return graph



graph_size = 10  # Розмір графа
graph_density = 0.3  # Щільність графа
weight_range = (1, 10)  # Діапазон ваги ребер


graph = generate_graph(graph_size, graph_density, weight_range)




