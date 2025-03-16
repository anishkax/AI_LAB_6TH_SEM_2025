import heapq
import matplotlib.pyplot as plt
import numpy as np

def manhattan_distance(x, y, goal):
    return abs(x - goal[0]) + abs(y - goal[1])

def best_first_search(maze, start, goal):
    if maze[start[0]][start[1]] == 1 or maze[goal[0]][goal[1]] == 1:
        return None, 0
    
    queue = [(0, start)]
    visited = set()
    parent = {start: None}
    steps = 0

    while queue:
        _, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1], steps

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                heapq.heappush(queue, (manhattan_distance(nx, ny, goal), (nx, ny)))
                parent[(nx, ny)] = current

    return None, steps

def visualize(maze, path, start, goal):
    maze = np.array(maze)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(maze, cmap="binary")

    if path:
        for x, y in path:
            ax.add_patch(plt.Rectangle((y, x), 1, 1, color='gold', alpha=0.5))
    ax.plot(start[1], start[0], 'go', markersize=10)
    ax.plot(goal[1], goal[0], 'ro', markersize=10)
    plt.show()

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]
start, goal = (0, 0), (4, 4)
path, steps = best_first_search(maze, start, goal)

if path:
    print(f"Path found: {path}")
else:
    print("No path found.")
print(f"Steps taken: {steps}")
visualize(maze, path, start, goal)