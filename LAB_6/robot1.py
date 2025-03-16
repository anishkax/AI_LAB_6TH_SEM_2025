import tkinter as tk
from tkinter import ttk
import math
import heapq
from collections import deque
import time
import random

class Node:
    def __init__(self, position, g_cost=float('inf'), h_cost=0):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = None

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class PathPlanningVisualizer:
    def __init__(self, root, grid_size=20, cell_size=30):
        # Initialize state variables first
        self.current_algorithm = None
        self.open_set = []
        self.closed_set = set()
        self.path = []
        self.step_delay = 100
        self.metrics = {
            'path_length': 0,
            'path_cost': 0,
            'nodes_explored': 0,
            'execution_time': 0,
            'start_time': 0
        }

        # Initialize window and grid parameters
        self.root = root
        self.root.title("Path Planning Visualizer")
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        # Start and goal positions
        self.start = (1, 1)
        self.goal = (grid_size - 2, grid_size - 2)
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.goal[0]][self.goal[1]] = 'G'

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Main control frame
        control_frame = ttk.Frame(self.root)  # Changed ttk.frame to ttk.Frame
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Algorithm selection
        ttk.Label(control_frame, text='Algorithm:').pack(side=tk.LEFT)
        self.algo_var = tk.StringVar(value='A* (Manhattan)')
        algo_menu = ttk.OptionMenu(control_frame, self.algo_var,  # Fixed usage of StringVar
                                   "A* (Manhattan)",
                                   "A* (Manhattan)",
                                   "A* (Euclidean)",
                                   "BFS",
                                   "Uniform Cost")
        algo_menu.pack(side=tk.LEFT, padx=5)

        # Control buttons
        ttk.Button(control_frame, text="Generate Random Obstacles",
                   command=self.generate_obstacles).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear Path",
                   command=self.clear_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Start Search",
                   command=self.start_search).pack(side=tk.LEFT, padx=5)

        # Speed control
        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=5)
        self.speed_scale = ttk.Scale(control_frame, from_=1, to=200,
                                     orient=tk.HORIZONTAL, length=100)

        self.speed_scale.set(100)
        self.speed_scale.pack(side=tk.LEFT)

        # Metrics frame
        metrics_frame = ttk.LabelFrame(self.root, text="Algorithm Metrics")
        metrics_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.metrics_labels = {}
        metrics_grid = [
            ("Path Length:", "path_length"),
            ("Path Cost:", "path_cost"),
            ("Nodes Explored:", "nodes_explored"),
            ("Execution Time (ms):", "execution_time")
        ]

        for i, (label_text, metric_key) in enumerate(metrics_grid):
            ttk.Label(metrics_frame, text=label_text).grid(row=i // 2, column=i % 2 * 2, padx=5, pady=2, sticky='e')
            label = ttk.Label(metrics_frame, text='0')
            label.grid(row=i // 2, column=i % 2 * 2 + 1, padx=5, pady=2, sticky='w')

        # Canvas for grid
        self.canvas = tk.Canvas(self.root,
                                width=self.grid_size * self.cell_size,
                                height=self.grid_size * self.cell_size)
        self.canvas.pack(padx=10, pady=10)

        # Bind canvas clicks
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # Fixed typo in bind method
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Colour based on cell type
                if self.grid[i][j] == 1:  # obstacle
                    color = "black"
                elif (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.goal:
                    color = "red"
                elif (i, j) in self.closed_set:
                    color = "light blue"
                elif any(node.position == (i, j) for node in self.open_set):
                    color = "yellow"
                elif (i, j) in self.path:
                    color = "blue"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="grey")

    def generate_obstacles(self):
        self.clear_path()

        # Generate random obstacles (30% of grid)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) != self.start and (i, j) != self.goal:
                    self.grid[i][j] = 1 if random.random() < 0.3 else 0

        self.draw_grid()

    def clear_path(self):
        self.open_set = []
        self.closed_set = set()
        self.path = []
        self.current_algorithm = None

        # Clear metrics
        for key in self.metrics:
            self.metrics[key] = 0
        self.update_metrics()

        # Clear everything except obstacles
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) != self.start and (i, j) != self.goal:
                    self.grid[i][j] = 0

        self.draw_grid()

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def euclidean_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def get_neighbors(self, pos, allow_diagonal=False):
        neighbors = []
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if allow_diagonal:
            moves += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in moves:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < self.grid_size and
                0 <= new_y < self.grid_size and
                self.grid[new_x][new_y] != 1):
                neighbors.append((new_x, new_y))

        return neighbors

    def reconstruct_path(self, current_node):
        path = []
        while current_node:
            path.append(current_node.position)
            current_node = current_node.parent
        return path[::-1]

    def update_metrics(self):
        for key, label in self.metrics_labels.items():
            label.config(text=str(self.metrics[key]))

    def calculate_metrics(self, path, start_time):
        self.metrics['path_length'] = len(path) if path else 0
        self.metrics['path_cost'] = self.calculate_path_cost(path)
        self.metrics['nodes_explored'] = len(self.closed_set)
        self.metrics['execution_time'] = int((time.time() - start_time) * 1000)
        self.update_metrics()

    def calculate_path_cost(self, path):
        if not path:
            return 0
        cost = 0
        for i in range(len(path) - 1):
            dx = abs(path[i + 1][0] - path[i][0])
            dy = abs(path[i + 1][1] - path[i][1])
            if dx + dy == 2:  # diagonal move
                cost += 1.4
            else:  # horizontal or vertical move
                cost += 1
        return round(cost, 2)

    def start_search(self):
        self.clear_path()
        algorithm = self.algo_var.get()
        start_time = time.time()

        if algorithm.startswith("A*"):
            self.current_algorithm = self.a_star_step
            heuristic = (self.manhattan_distance if "Manhattan" in algorithm
                         else self.euclidean_distance)
            allow_diagonal = "Euclidean" in algorithm

            start_node = Node(self.start, g_cost=0,
                              h_cost=heuristic(self.start, self.goal))
            heapq.heappush(self.open_set, start_node)

        elif algorithm == "BFS":
            self.current_algorithm = self.bfs_step
            start_node = Node(self.start, g_cost=0)
            self.open_set = deque([start_node])

        elif algorithm == "Uniform Cost":
            self.current_algorithm = self.uniform_cost_step
            start_node = Node(self.start, g_cost=0)
            heapq.heappush(self.open_set, start_node)

        self.step_delay = int(200 - self.speed_scale.get())
        self.metrics['start_time'] = start_time
        self.step_search()

    def step_search(self):
        if self.current_algorithm:
            result = self.current_algorithm()
            self.draw_grid()

            if result:  # Search finished
                self.calculate_metrics(self.path, self.metrics['start_time'])
            else:  # Search not finished
                self.root.after(self.step_delay, self.step_search)

    def a_star_step(self):
        if not self.open_set:
            print("No path found!")
            return True

        current = heapq.heappop(self.open_set)

        if current.position == self.goal:
            self.path = self.reconstruct_path(current)
            print("Path found!")
            return True

        self.closed_set.add(current.position)

        allow_diagonal = "Euclidean" in self.algo_var.get()
        for neighbor_pos in self.get_neighbors(current.position, allow_diagonal):
            if neighbor_pos in self.closed_set:
                continue

            g_cost = current.g_cost + (1.4 if allow_diagonal and
                                       abs(neighbor_pos[0] - current.position[0]) +
                                       abs(neighbor_pos[1] - current.position[1]) == 2
                                       else 1)

            heuristic = (self.manhattan_distance if "Manhattan" in self.algo_var.get()
                         else self.euclidean_distance)
            h_cost = heuristic(neighbor_pos, self.goal)

            neighbor = Node(neighbor_pos, g_cost, h_cost)
            neighbor.parent = current

            if not any(n.position == neighbor_pos and n.g_cost <= g_cost
                       for n in self.open_set):
                heapq.heappush(self.open_set, neighbor)
        return False

    def bfs_step(self):
        if not self.open_set:
            print("No path found!")
            return True

        current = self.open_set.popleft()

        if current.position == self.goal:
            self.path = self.reconstruct_path(current)
            print("Path found!")
            return True

        self.closed_set.add(current.position)

        for neighbor_pos in self.get_neighbors(current.position):
            if (neighbor_pos not in self.closed_set and
                not any(n.position == neighbor_pos for n in self.open_set)):
                neighbor = Node(neighbor_pos)
                neighbor.parent = current
                self.open_set.append(neighbor)

        return False

    def uniform_cost_step(self):
        if not self.open_set:
            print("No path found!")
            return True

        current = heapq.heappop(self.open_set)
        if current.position == self.goal:
            self.path = self.reconstruct_path(current)
            print("Path found!")
            return True

        self.closed_set.add(current.position)

        for neighbor_pos in self.get_neighbors(current.position):
            if neighbor_pos in self.closed_set:
                continue

            g_cost = current.g_cost + 1
            neighbor = Node(neighbor_pos, g_cost)
            neighbor.parent = current

            if not any(n.position == neighbor_pos and n.g_cost <= g_cost
                       for n in self.open_set):
                heapq.heappush(self.open_set, neighbor)
        return False

    def on_canvas_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if (y, x) != self.start and (y, x) != self.goal:
            self.grid[y][x] = 1 if self.grid[y][x] == 0 else 0
            self.draw_grid()

def main():
    root = tk.Tk()
    app = PathPlanningVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
