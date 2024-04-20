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

