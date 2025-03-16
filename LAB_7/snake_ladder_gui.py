import random
import tkinter as tk
from tkinter import messagebox

class SnakeLaddersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake & Ladders")
        self.root.geometry("500x600")
        self.root.configure(bg="#1E1E2E")

        self.board_size = 100
        self.position = 1
        self.wins = 0

        self.snakes = {97: 78, 95: 56, 88: 24, 62: 18, 48: 26, 36: 6, 32: 10}
        self.ladders = {3: 22, 5: 8, 15: 97, 20: 59, 57: 96, 45: 65, 60: 80}

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#333344", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.info_label = tk.Label(self.root, text=f"Position: {self.position}", font=("Arial", 14, "bold"), fg="white", bg="#4A90E2")
        self.info_label.pack()

        self.roll_button = tk.Button(self.root, text="Roll Dice 🎲", font=("Arial", 14, "bold"), command=self.roll_dice, bg="#2ECC71", fg="white", padx=10, pady=5)
        self.roll_button.pack(pady=10)

        self.wins_label = tk.Label(self.root, text=f"Wins: {self.wins}", font=("Arial", 14, "bold"), fg="white", bg="#4A90E2")
        self.wins_label.pack()

        self.draw_board()

    def roll_dice(self):
        roll = random.randint(1, 6)
        new_position = self.position + roll
        if new_position <= self.board_size:
            self.position = new_position
            self.position = self.snakes.get(self.position, self.position)
            self.position = self.ladders.get(self.position, self.position)

        self.info_label.config(text=f"Position: {self.position}")

        if self.position == self.board_size:
            self.celebrate_win()

        self.draw_board()

    def celebrate_win(self):
        self.wins += 1
        self.wins_label.config(text=f"Wins: {self.wins}")
        messagebox.showinfo("Congratulations!", "You won! 🎉🏆")
        self.position = 1
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 40
        colors = ["#2C3E50", "#34495E"]

        numbers = []
        for i in range(10):
            row = list(range(i * 10 + 1, (i + 1) * 10 + 1))
            if i % 2 == 1:
                row.reverse()
            numbers.insert(0, row)

        for i in range(10):
            for j in range(10):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = colors[(i + j) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                number = numbers[i][j]
                self.canvas.create_text(x1 + 20, y1 + 20, text=str(number), font=("Arial", 10, "bold"), fill="white")

        for start, end in self.ladders.items():
            self.draw_ladder(start, end)
        for start, end in self.snakes.items():
            self.draw_snake(start, end)

        player_x, player_y = self.get_cell_coordinates(self.position)
        self.canvas.create_oval(player_x - 10, player_y - 10, player_x + 10, player_y + 10, fill="#FFD700", outline="white", width=2)

    def draw_snake(self, start, end):
        start_x, start_y = self.get_cell_coordinates(start)
        end_x, end_y = self.get_cell_coordinates(end)

        # Draw zig-zag snake body
        num_segments = 6
        points = []
        for i in range(num_segments + 1):
            t = i / num_segments
            mid_x = start_x * (1 - t) + end_x * t
            mid_y = start_y * (1 - t) + end_y * t
            offset = 10 * ((i % 2) * 2 - 1)
            if i not in [0, num_segments]:
                mid_x += offset
            points.append((mid_x, mid_y))

        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill="#FF5733", width=4, smooth=True)

        # Snake Head
        self.canvas.create_oval(start_x - 10, start_y - 10, start_x + 10, start_y + 10, fill="green", outline="black", width=2)

        # Snake Eyes
        self.canvas.create_oval(start_x - 5, start_y - 5, start_x - 2, start_y - 2, fill="white")
        self.canvas.create_oval(start_x + 2, start_y - 5, start_x + 5, start_y - 2, fill="white")

        # Snake Tongue
        tongue_x, tongue_y = start_x + 12, start_y
        self.canvas.create_line(start_x, start_y, tongue_x, tongue_y, fill="red", width=2)
        self.canvas.create_line(tongue_x, tongue_y, tongue_x + 5, tongue_y - 5, fill="red", width=2)
        self.canvas.create_line(tongue_x, tongue_y, tongue_x + 5, tongue_y + 5, fill="red", width=2)

    def draw_ladder(self, start, end):
        start_x, start_y = self.get_cell_coordinates(start)
        end_x, end_y = self.get_cell_coordinates(end)

        # Draw side rails of ladder
        self.canvas.create_line(start_x - 10, start_y, end_x - 10, end_y, fill="#8B4513", width=5)
        self.canvas.create_line(start_x + 10, start_y, end_x + 10, end_y, fill="#8B4513", width=5)

        # Draw ladder steps
        steps = 6
        for i in range(steps):
            step_x1 = start_x - 10
            step_x2 = start_x + 10
            step_y = start_y + (end_y - start_y) * i / (steps - 1)
            self.canvas.create_line(step_x1, step_y, step_x2, step_y, fill="white", width=2)

    def get_cell_coordinates(self, position):
        cell_size = 40
        row = (position - 1) // 10
        x = ((position - 1) % 10) * cell_size + cell_size // 2
        if row % 2 == 1:
            x = 400 - x
        y = (9 - row) * cell_size + cell_size // 2
        return x, y

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLaddersGame(root)
    root.mainloop()
