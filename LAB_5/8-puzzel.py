class Node:
    def __init__(self, data, level, fval):
        """Initialize the node with the puzzle state, level of the node, and f-value."""
        self.data = data
        self.level = level  # Depth of the node
        self.fval = fval  # f(x) = h(x) + g(x)

    def generate_child(self):
        """Generate child nodes by moving the blank space in four possible directions."""
        x, y = self.find(self.data, '_')  # Locate the blank space ('_')

        # Possible moves: left, right, up, down
        moves = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []

        for move in moves:
            child = self.shuffle(self.data, x, y, move[0], move[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)  # fval will be updated later
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """Swap the blank space with an adjacent tile to generate a new state."""
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp_puz[x1][y1], temp_puz[x2][y2] = temp_puz[x2][y2], temp_puz[x1][y1]
            return temp_puz
        return None

    def copy(self, root):
        """Create a deep copy of the given puzzle state."""
        return [row[:] for row in root]

    def find(self, puz, val):
        """Find the position (x, y) of a given value in the puzzle."""
        for i in range(len(puz)):
            for j in range(len(puz[i])):
                if puz[i][j] == val:
                    return i, j
        return None


class Puzzle:
    def __init__(self, size):
        """Initialize the puzzle with given size and empty open & closed lists."""
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """Accepts the puzzle state from the user."""
        print(f"Enter the {self.n}x{self.n} puzzle row by row (use '_' for blank space):")
        puz = [input().split() for _ in range(self.n)]
        return puz

    def f(self, start, goal):
        """Calculate the heuristic value f(x) = h(x) + g(x)."""
        return self.h(start.data, goal.data) + start.level

    def h(self, start, goal):
        """Heuristic function: Counts the number of misplaced tiles."""
        temp = sum(1 for i in range(self.n) for j in range(self.n) if start[i][j] != '_' and start[i][j] != goal[i][j])
        return temp

    def process(self):
        """Solves the puzzle using A* search algorithm."""
        # Accept start and goal states
        start_data = self.accept()
        goal_data = self.accept()

        # Create start and goal nodes
        start = Node(start_data, 0, 0)
        goal = Node(goal_data, 0, 0)

        # Set initial f-value
        start.fval = self.f(start, goal)

        # Add start node to open list
        self.open.append(start)

        print("\nSolving...\n")
        while self.open:
            # Get the node with the lowest f-value
            cur = self.open.pop(0)
            self.closed.append(cur)

            # Print current state
            print("\nStep:")
            for row in cur.data:
                print(" ".join(row))
            print("-----")

            # Check if goal is reached
            if self.h(cur.data, goal.data) == 0:
                print("Solution Found!")
                return

            # Generate child nodes
            for child in cur.generate_child():
                child.fval = self.f(child, goal)
                self.open.append(child)

            # Sort open list based on f-value (best-first search)
            self.open.sort(key=lambda x: x.fval)

        print("No solution found!")


# Run the Puzzle Solver
puzzle = Puzzle(3)
puzzle.process()