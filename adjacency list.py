import matplotlib.pyplot as plt
import networkx as nx
import random
from heapq import heappop, heappush
import time


class Graph:
    def __init__(self, Nodes=None, is_directed=False, num_vertices=0): # створюємо клас Graph з заданими параметрами.
        self.nodes = self.__get_nodes(Nodes, num_vertices)
        self.adj_list = {}
        self.is_directed = is_directed

        for node in self.nodes: # створюємо список суміжності для кожної вершини
            self.adj_list[node] = []

    def __get_nodes(self, Nodes, num_vertices):#метод для генерації списку вершин графа, якщо він не заданий.
        if Nodes is not None:
            return Nodes
        return self.__generate_nodes(num_vertices)

    def __generate_nodes(self, num_vertices): #метод генерує список вершин графа.
        nodes = []
        for i in range(num_vertices):
            nodes.append(i)
        return nodes

    def add_edge(self, u, v, w): #метод додає ребро між вершинами з вагою.

        if u not in self.adj_list:
            self.adj_list[u] = []
        self.adj_list[u].append((v, w))
        if not self.is_directed:
            if v not in self.adj_list:
                self.adj_list[v] = []
            self.adj_list[v].append((u, w))

    def degree_vertex(self, node): #метод повертає ступінь вершини
        degree = len(self.adj_list[node])
        return degree

    def print_adj(self): #метод виводить список суміжності графа на екран.
        for node in self.nodes:
            print(node, ":", self.adj_list[node])

    def remove_edge(self, v, e): #метод видаляє ребро між вершинами.
        if e in self.adj_list[v]:
            self.adj_list[v].remove(e)
        if not self.is_directed:
            if v in self.adj_list[e]:
                self.adj_list[e].remove(v)

    def remove_vertex(self, node): #метод видаляє вершину з графа.
        if node in self.adj_list:
            for adjacent in list(self.adj_list[node]):
                self.adj_list[adjacent].remove(node)
            del self.adj_list[node]
            self.nodes.remove(node)

    def generate_connected_graph(self, density):
        if len(self.nodes) == 0: # перевірка, чи граф має вершини
            return
        for i in range(len(self.nodes) - 1): # створення ребер для зв'язування вершин у графі
            self.add_edge(self.nodes[i], self.nodes[i + 1], random.randint(-10, 10)) # Додаємо ребро між поточною вершиною та наступною з випадковою вагою
        for i in range(len(self.nodes)): # Додавання додаткових ребер з ймовірністю, визначеною параметром density
            for j in range(i + 2, len(self.nodes)):
                if random.random() < density:  # Генеруємо випадкове число від 0 до 1, яке визначає, чи додати ребро
                    self.add_edge(self.nodes[i], self.nodes[j], random.randint(-10, 10)) # Додаємо ребро між поточною вершиною та будь-якою вершиною пізніше за неї з випадковою вагою

    def bellman_ford(self, source):
        distance = {node: float('inf') for node in self.nodes} # Створюємо словник для зберігання відстаней від поч.вершини до кожної вершини
        distance[source] = 0 # встановлюємо відстань від поч.вершини до самої себе рівну нулю

        for i in range(len(self.nodes) - 1): # проводимо ітерації ,щоб знайти найкоротші шляхи
            for node in self.nodes: # проходимося по кожній вершині граф
                for neighbour, weight in self.adj_list[node]: # якщо шлях до сусідньої вершини коротший, то оновлюємо відстань
                    if distance[node] != float('inf') and distance[node] + weight < distance[neighbour]:
                        distance[neighbour] = distance[node] + weight

        for node in self.nodes: # Перевіряємо наявність негативних циклів
            for neighbour, weight in self.adj_list[node]:
                if distance[node] != float('inf') and distance[node] + weight < distance[neighbour]:
                    print("Граф містить негативний ваговий цикл")
                    return

        return distance

    def dijkstra(self, src, weight):
        distances = {node: float('inf') for node in self.nodes}#словник для зберігання відстаней від вершини src(початкова) до всіх інших вершин
        distances[src] = 0 # відстань від вершини src до себе дорівнює 0

        heap = [(0, src)] # ініціалізуємо чергу з відстанями та вершинами
        while heap:
            d, node = heappop(heap) # вибираємо вершину з найменшою відстанню
            if distances[node] != d: # якщо відстань у словнику відрізняється, пропускаємо цю вершину
                continue
            for neighbor, w in self.adj_list[node]: # перебираємо всі сусідні вершини
                old_cost = distances[neighbor]
                new_cost = distances[node] + w  # Обчислюємо нову відстань
                if new_cost < old_cost: # якщо нова відстань менша за попередню, оновлюємо значення
                    distances[neighbor] = new_cost
                    heappush(heap, (new_cost, neighbor)) # додаємо вершину у чергу з оновленою відстанню
        return distances

    def johnson(self):
        weight = self.bellman_ford(0)  # Обчислюємо ваги найкоротших шляхів від початкової вершини
        if any([d == float('inf') for d in weight.values()]):  # Перевіряємо, чи є в графі негативний ваговий цикл
            print("Граф містить негативний ваговий цикл")
            return None

        shortest_paths = {}# Створюємо словник для зберігання найкоротших шляхів від кожної вершини до всіх інших
        for node in self.nodes:# Обчислюємо найкоротші шляхи від кожної вершини до всіх інших за допомогою алгоритму Дейкстри
            shortest_paths[node] = self.dijkstra(node, weight)
        return shortest_paths

    def visualize_graph(self):
        G = nx.DiGraph() if self.is_directed else nx.Graph()  # створюємо граф
        edge_labels = {}  # словник для зберігання ваг на ребрах
        for node in self.nodes:  # додаємо вершини до графу
            G.add_node(node)
        for node, edges in self.adj_list.items():  # додаємо ребра до графу та заповнюємо словник edge_labels
            for edge, weight in edges:
                G.add_edge(node, edge)
                edge_labels[(node, edge)] = weight

        pos = nx.spring_layout(G)  # обчислюємо позиції вершин у малюнку графа
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=500, font_size=16,
                font_weight='bold')  # малюємо граф з властивостями вершин та ребер
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     font_color='red')  # додаємо підписи на ребрах до візуалізації графа
        plt.show()  # візуалізуємо граф


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

start_time = time.time()

distances = graph.bellman_ford(start)
shortest_paths = graph.johnson()

end_time = time.time()

print("Час виконання: {} секунд".format(end_time - start_time))

if shortest_paths is not None:
    print("Найкоротші шляхи від кожної вершини до інших: ", shortest_paths)

    if end in shortest_paths[start] and shortest_paths[start][end] != float('inf'):
        print("Найкоротший шлях від {} до {}: ".format(start, end), shortest_paths[start][end])
    else:
        print("Шлях від {} до {} не існує.".format(start, end))

    graph.visualize_graph()