import matplotlib.pyplot as plt
import networkx as nx
import random
from heapq import heappop, heappush


class Graph:
    def __init__(self, Nodes=None, is_directed=False, num_vertices=0):  # створюємо клас Graph з заданими параметрами.
        self.nodes = self.__get_nodes(Nodes, num_vertices)
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.is_directed = is_directed

    def __get_nodes(self, Nodes, num_vertices):  # метод для генерації списку вершин графа, якщо він не заданий
        if Nodes is not None:
            return Nodes
        return list(range(num_vertices))

    def add_edge(self, u, v, w):  # додає ребро між вершинами з вагою w.
        self.adj_matrix[u][v] = w
        if not self.is_directed:
            self.adj_matrix[v][u] = w

    def degree_vertex(self, node):  # Повертає ступінь вершини у графі
        return sum(1 for neighbor in self.adj_matrix[node] if neighbor != 0)

    def print_adj(self):  # виводить матрицю суміжності графа
        for row in self.adj_matrix:
            print(row)

    def remove_edge(self, v, e):  # Видаляє ребро між вершинами v та e.
        self.adj_matrix[v][e] = 0
        if not self.is_directed:
            self.adj_matrix[e][v] = 0

    def remove_vertex(self, node):  # Видаляє вершину та всі зв'язані з нею ребра
        self.nodes.remove(node)
        del self.adj_matrix[node]
        for row in self.adj_matrix:
            del row[node]

    def generate_connected_graph(self, density):  # Генерує зв'язний граф з випадковими ребрами.
        if len(self.nodes) == 0:
            return
        for i in range(len(self.nodes) - 1):
            self.add_edge(self.nodes[i], self.nodes[i + 1], random.randint(-10, 10))
        for i in range(len(self.nodes)):
            for j in range(i + 2, len(self.nodes)):
                if random.random() < density:
                    self.add_edge(self.nodes[i], self.nodes[j], random.randint(-10, 10))

    def bellman_ford(self, source):  # Застосовує алгоритм Беллмана-Форда для знаходження найкоротших шляхів у графі.
        distance = [float('inf')] * len(self.nodes)
        distance[source] = 0  # встановлюємо відстань від поч.вершини до самої себе рівну нулю

        for i in range(len(self.nodes) - 1):  # проводимо ітерації ,щоб знайти найкоротші шляхи
            for u in range(len(self.nodes)):  # перебираємо всі вершини графа
                for v in range(len(self.nodes)):  #
                    if self.adj_matrix[u][v] != 0 and distance[u] + self.adj_matrix[u][v] < distance[v]:
                        distance[v] = distance[u] + self.adj_matrix[u][v]

        for u in range(len(self.nodes)):  # Перевірка на наявність негативного вагового циклу
            for v in range(len(self.nodes)):
                if self.adj_matrix[u][v] != 0 and distance[u] + self.adj_matrix[u][v] < distance[v]:
                    print("Граф містить негативний ваговий цикл")
                    return

        return distance  # повертаємо список відстаней від вершини-джерела до кожної іншої вершини

    def dijkstra(self, src):  #
        distances = {node: float('inf') for node in self.nodes}
        distances[src] = 0

        heap = [(0, src)]  # створюємо чергу з вагою 0 для вершини-джерела
        while heap:
            d, u = heappop(heap)  # вибір вершини з мінімальною вагою з черги
            if distances[u] != d:  # перевірка актуальності відстані для вершини
                continue
            for v in self.nodes:
                if self.adj_matrix[u][v] != 0:  # перевірка наявності ребра між вершинами u та v
                    new_cost = distances[u] + self.adj_matrix[u][v]
                    if new_cost < distances[v]:  # оновлення відстані, якщо знайдено коротший шлях
                        distances[v] = new_cost
                        heappush(heap, (new_cost, v))  # додавання вершини з оновленою відстанню у чергу
        return distances

    def johnson(self):  #
        weight = self.bellman_ford(0)  # знаходження відстаней за допомогою алгоритму Беллмана-Форда

        if any([d == float('inf') for d in weight]):  # перевірка наявності негативного вагового циклу
            print("Граф містить негативний ваговий цикл")
            return None

        shortest_paths = {}
        for node in self.nodes:
            shortest_paths[node] = self.dijkstra(node)  # знаходження найкоротших шляхів від кожної вершини
        return shortest_paths

    def visualize_graph(self):  #
        graph = nx.DiGraph() if self.is_directed else nx.Graph()
        edge_labels = {}
        for node in self.nodes:
            graph.add_node(node)
        for u in range(len(self.nodes)):
            for v in range(len(self.nodes)):
                if self.adj_matrix[u][v] != 0:
                    graph.add_edge(u, v)
                    edge_labels[(u, v)] = self.adj_matrix[u][v]

        pos = nx.spring_layout(graph)  # обчислюємо позиції вершин у малюнку графа
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=500, font_size=16,
                font_weight='bold')  # малюємо граф з властивостями вершин та ребер
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
        plt.show() # візуалізуємо граф


def get_user_input():  #
    start = int(input("Введіть початкову точку: "))
    num_vertices = int(input("Введіть кількість вершин: "))
    end = int(input("Введіть точку виходу: "))
    density = float(input("Введіть кофіцієнт щільності:"))
    return start, num_vertices, end, density


start, num_vertices, end, density = get_user_input()

graph = Graph(None, is_directed=True, num_vertices=num_vertices)
graph.generate_connected_graph(density)
graph.print_adj()

distances = graph.bellman_ford(start)
print("Відстані від початкової точки до інших вершин: ", distances)

shortest_paths = graph.johnson()
if shortest_paths is not None:
    print("Найкоротші шляхи від кожної вершини до інших: ", shortest_paths)

    if end in shortest_paths[start] and shortest_paths[start][end] != float('inf'):
        print("Найкоротший шлях від {} до {}: ".format(start, end), shortest_paths[start][end])
    else:
        print("Шлях від {} до {} не існує..".format(start, end))

    graph.visualize_graph()
