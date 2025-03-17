import time
import heapq
import matplotlib.pyplot as plt
from collections import deque

class Puzzle:
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = tuple(board)
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.blank_index = board.index(0)

    def __lt__(self, other):
        return self.cost < other.cost

    def generate_children(self):
        children = []
        moves = {'U': -3, 'D': 3, 'L': -1, 'R': 1}
        for move, pos_change in moves.items():
            new_index = self.blank_index + pos_change
            if 0 <= new_index < 9 and not (self.blank_index % 3 == 0 and move == 'L') and not (self.blank_index % 3 == 2 and move == 'R'):
                new_board = list(self.board)
                new_board[self.blank_index], new_board[new_index] = new_board[new_index], new_board[self.blank_index]
                children.append(Puzzle(new_board, self, move, self.depth + 1, self.cost + 1))
        return children

    def is_goal(self):
        return self.board == (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def heuristic(self):
        goal = {val: (i // 3, i % 3) for i, val in enumerate((1, 2, 3, 4, 5, 6, 7, 8, 0))}
        return sum(abs(goal[val][0] - i // 3) + abs(goal[val][1] - i % 3) for i, val in enumerate(self.board) if val != 0)

def bfs(start):
    queue = deque([start])
    visited = set()
    nodes_explored = 0
    while queue:
        node = queue.popleft()
        nodes_explored += 1
        if node.is_goal():
            return nodes_explored, node.depth
        visited.add(node.board)
        for child in node.generate_children():
            if child.board not in visited:
                queue.append(child)
    return -1, -1

def dfs(start):
    stack = [start]
    visited = set()
    nodes_explored = 0
    while stack:
        node = stack.pop()
        nodes_explored += 1
        if node.is_goal():
            return nodes_explored, node.depth
        visited.add(node.board)
        for child in reversed(node.generate_children()):
            if child.board not in visited:
                stack.append(child)
    return -1, -1

def ucs(start):
    pq = [(0, start)]
    visited = set()
    nodes_explored = 0
    while pq:
        cost, node = heapq.heappop(pq)
        nodes_explored += 1
        if node.is_goal():
            return nodes_explored, node.depth
        visited.add(node.board)
        for child in node.generate_children():
            if child.board not in visited:
                heapq.heappush(pq, (child.cost, child))
    return -1, -1

def best_first(start):
    pq = [(start.heuristic(), start)]
    visited = set()
    nodes_explored = 0
    while pq:
        _, node = heapq.heappop(pq)
        nodes_explored += 1
        if node.is_goal():
            return nodes_explored, node.depth
        visited.add(node.board)
        for child in node.generate_children():
            if child.board not in visited:
                heapq.heappush(pq, (child.heuristic(), child))
    return -1, -1

def a_star(start):
    pq = [(start.heuristic(), start)]
    visited = set()
    nodes_explored = 0
    while pq:
        _, node = heapq.heappop(pq)
        nodes_explored += 1
        if node.is_goal():
            return nodes_explored, node.depth
        visited.add(node.board)
        for child in node.generate_children():
            if child.board not in visited:
                heapq.heappush(pq, (child.cost + child.heuristic(), child))
    return -1, -1

def run_tests():
    initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]
    start = Puzzle(initial_state)
    algorithms = {'BFS': bfs, 'DFS': dfs, 'UCS': ucs, 'Best-First': best_first, 'A*': a_star}
    results = {}
    for name, algo in algorithms.items():
        start_time = time.time()
        nodes_explored, depth = algo(start)
        end_time = time.time()
        results[name] = (nodes_explored, end_time - start_time, depth)
    return results

def plot_results(results):
    names = list(results.keys())
    nodes_explored = [results[name][0] for name in names]
    times = [results[name][1] for name in names]
    depths = [results[name][2] for name in names]
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.bar(names, nodes_explored, color='b', alpha=0.6, label='Nodes Explored')
    ax2.plot(names, times, color='r', marker='o', label='Time (s)')
    
    ax1.set_xlabel('Algorithm')
    ax1.set_ylabel('Nodes Explored', color='b')
    ax2.set_ylabel('Time (s)', color='r')
    ax1.set_title('Search Algorithm Comparison')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.show()
    
results = run_tests()
plot_results(results)
