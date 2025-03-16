import tkinter as tk
from queue import PriorityQueue, Queue
from typing import Dict, List, Set, Tuple, Optional
import random
import math


class GraphNode:
    def __init__(self, x: int, y: int, id: str):
        self.x = x
        self.y = y
        self.id = id
        self.neighbors: Dict['GraphNode', float] = {}  # neighbor -> weight

    def add_neighbor(self, neighbor: 'GraphNode', weight: float):
        self.neighbors[neighbor] = weight

    def get_position(self) -> Tuple[int, int]:
        return self.x, self.y

class Graph:
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}

    def add_node(self, node_id: str, x: int, y: int):
        self.nodes[node_id] = GraphNode(x, y, node_id)

    def add_edge(self, from_id: str, to_id: str, weight: float):
        if from_id in self.nodes and to_id in self.nodes:
            self.nodes[from_id].add_neighbor(self.nodes[to_id], weight)
            self.nodes[to_id].add_neighbor(self.nodes[from_id], weight)  # Undirected Graph


class GraphSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Search Visualization")

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Canvas for Graph Visualization
        self.canvas_size = 600
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Control Panel
        self.control_panel = tk.Frame(self.main_frame)
        self.control_panel.pack(side=tk.LEFT, padx=20, fill='y')

        # Algorithm selection
        self.algo_var = tk.StringVar(value='UCS')
        tk.Label(self.control_panel, text='Algorithm: ').pack(anchor='w')
        tk.Radiobutton(self.control_panel, text='Uniform Cost Search', variable=self.algo_var, value='UCS').pack(anchor='w')
        tk.Radiobutton(self.control_panel, text='Breadth First Search', variable=self.algo_var, value='BFS').pack(anchor='w')

        # Buttons
        tk.Button(self.control_panel, text='Generate New Graph', command=self.generate_graph).pack(fill='x', pady=5)
        tk.Button(self.control_panel, text='Start Search', command=self.start_search).pack(fill='x', pady=5)
        tk.Button(self.control_panel, text='Reset', command=self.reset_visualization).pack(fill='x', pady=5)

        # Statistics
        self.stats_frame = tk.LabelFrame(self.control_panel, text='Statistics', padx=5, pady=5)
        self.stats_frame.pack(fill='x', pady=10)

        self.nodes_explored_var = tk.StringVar(value='Nodes explored: 0')
        self.path_cost_var = tk.StringVar(value='Path Cost: 0')
        tk.Label(self.stats_frame, textvariable=self.nodes_explored_var).pack(anchor='w')
        tk.Label(self.stats_frame, textvariable=self.path_cost_var).pack(anchor='w')

        # Initialize Graph
        self.generate_graph()

    def generate_graph(self):
        self.graph = Graph()
        num_nodes = 10

        # Generate random nodes
        padding = 50
        for i in range(num_nodes):
            x = random.randint(padding, self.canvas_size - padding)
            y = random.randint(padding, self.canvas_size - padding)
            self.graph.add_node(str(i), x, y)

        # Generate edges (connect each node to 2-3 nearest neighbors)
        for node_id, node in self.graph.nodes.items():
            distances = []
            for other_id, other in self.graph.nodes.items():
                if node_id != other_id:
                    dist = math.sqrt((node.x - other.x) ** 2 + (node.y - other.y) ** 2)
                    distances.append((dist, other_id))

            distances.sort()
            for i in range(min(random.randint(2, 3), len(distances))):
                dist, other_id = distances[i]
                self.graph.add_edge(node_id, other_id, dist)

        self.start_node = '0'
        self.end_node = str(num_nodes - 1)
        self.draw_graph()

    def draw_graph(self):
        self.canvas.delete('all')

        # Draw edges
        for node_id, node in self.graph.nodes.items():
            for neighbor, weight in node.neighbors.items():
                self.canvas.create_line(node.x, node.y, neighbor.x, neighbor.y, fill='grey', width=2)

                # Draw weight
                mid_x = (node.x + neighbor.x) / 2
                mid_y = (node.y + neighbor.y) / 2
                self.canvas.create_text(mid_x, mid_y, text=f'{weight:.1f}', fill='blue', font=('Arial', 8))

        # Draw nodes
        node_radius = 20
        for node_id, node in self.graph.nodes.items():
            color = 'green' if node_id == self.start_node else 'red' if node_id == self.end_node else 'white'
            self.canvas.create_oval(node.x - node_radius, node.y - node_radius,
                                     node.x + node_radius, node.y + node_radius,
                                     fill=color, outline='black')
            self.canvas.create_text(node.x, node.y, text=node_id)

    def uniform_cost_search(self) -> Tuple[List[str], float, int]:
        frontier = PriorityQueue()
        frontier.put((0, self.start_node))
        came_from = {self.start_node: None}
        cost_so_far = {self.start_node: 0}
        nodes_explored = 0

        while not frontier.empty():
            current_cost, current_id = frontier.get()
            nodes_explored += 1

            if current_id == self.end_node:
                break

            current_node = self.graph.nodes[current_id]
            self.highlight_node(current_id, 'yellow')
            self.root.update()
            self.root.after(500)

            for next_node, weight in current_node.neighbors.items():
                new_cost = cost_so_far[current_id] + weight
                if next_node.id not in cost_so_far or new_cost < cost_so_far[next_node.id]:
                    cost_so_far[next_node.id] = new_cost
                    frontier.put((new_cost, next_node.id))
                    came_from[next_node.id] = current_id

        path = []
        current = self.end_node
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()

        return path, cost_so_far.get(self.end_node, float('inf')), nodes_explored

    def breadth_first_search(self) -> Tuple[List[str], float, int]:
        frontier = Queue()
        frontier.put(self.start_node)
        came_from = {self.start_node: None}
        nodes_explored = 0

        while not frontier.empty():
            current_id = frontier.get()
            nodes_explored += 1

            if current_id == self.end_node:
                break

            current_node = self.graph.nodes[current_id]
            self.highlight_node(current_id, 'yellow')
            self.root.update()
            self.root.after(500)

            for next_node, _ in current_node.neighbors.items():
                if next_node.id not in came_from:
                    frontier.put(next_node.id)
                    came_from[next_node.id] = current_id

        path = []
        current = self.end_node
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()

        total_cost = 0
        for i in range(len(path) - 1):
            current_node = self.graph.nodes[path[i]]
            next_node = self.graph.nodes[path[i + 1]]
            total_cost += current_node.neighbors[next_node]

        return path, total_cost, nodes_explored

    def highlight_node(self, node_id: str, color: str):
        node = self.graph.nodes[node_id]
        node_radius = 20
        self.canvas.create_oval(node.x - node_radius, node.y - node_radius,
                                 node.x + node_radius, node.y + node_radius,
                                 fill=color, outline='black')
        self.canvas.create_text(node.x, node.y, text=node_id)

    def highlight_path(self, path: List[str]):
        for i in range(len(path) - 1):
            current = self.graph.nodes[path[i]]
            next_node = self.graph.nodes[path[i + 1]]
            self.canvas.create_line(current.x, current.y, next_node.x, next_node.y, fill='green', width=3)

        for node_id in path:
            node = self.graph.nodes[node_id]
            color = 'green' if node_id == self.start_node else 'red' if node_id == self.end_node else 'light green'
            node_radius = 20
            self.canvas.create_oval(node.x - node_radius, node.y - node_radius,
                                     node.x + node_radius, node.y + node_radius,
                                     fill=color, outline='black')
            self.canvas.create_text(node.x, node.y, text=node_id)

    def start_search(self):
        self.reset_visualization()

        if self.algo_var.get() == 'UCS':
            path, cost, nodes = self.uniform_cost_search()
        else:
            path, cost, nodes = self.breadth_first_search()

        self.highlight_path(path)
        self.nodes_explored_var.set(f'Nodes explored: {nodes}')
        self.path_cost_var.set(f'Path cost: {cost:.1f}')

    def reset_visualization(self):
        self.draw_graph()
        self.nodes_explored_var.set('Nodes explored: 0')
        self.path_cost_var.set('Path cost: 0')


def main():
    root = tk.Tk()
    app = GraphSearchGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
