import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - AI Mode")
        self.window.geometry("330x420")
        self.window.resizable(False, False)
        self.window.configure(bg="#222")
        
        self.colors = {"X": "#ff7675", "O": "#74b9ff", "bg": "#2d3436", "fg": "#dfe6e9"}
        self.player_wins = 0
        self.ai_wins = 0
        
        self.create_widgets()
        self.reset_board()
        
    def create_widgets(self):
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.window, text="", font=("Arial", 20, "bold"), height=2, width=5,
                                   bg=self.colors["bg"], fg=self.colors["fg"],
                                   command=lambda r=i, c=j: self.human_move(r, c))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)
        
        self.status_label = tk.Label(self.window, text="Your Turn (X)", font=("Arial", 13, "bold"), bg="#222", fg="#fff")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=5)
        
        self.score_label = tk.Label(self.window, text=f"Player: {self.player_wins}  AI: {self.ai_wins}",
                                    font=("Arial", 12, "bold"), bg="#222", fg="#fff")
        self.score_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        self.play_again_button = tk.Button(self.window, text="Play Again", font=("Arial", 12, "bold"),
                                           bg="#00b894", fg="white", command=self.reset_board)
        self.play_again_button.grid(row=5, column=0, columnspan=3, pady=10)

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.player_turn = "X"
        self.status_label.config(text="Your Turn (X)")
        for row in self.buttons:
            for button in row:
                button.config(text="", bg=self.colors["bg"])  

    def human_move(self, row, col):
        if self.board[row][col] == "" and self.player_turn == "X":
            self.board[row][col] = "X"
            self.buttons[row][col]["text"] = "X"
            self.buttons[row][col]["bg"] = self.colors["X"]
            if self.check_win("X"):
                self.player_wins += 1
                messagebox.showinfo("Game Over", "You Win!")
                self.update_score()
                return
            self.player_turn = "O"
            self.status_label.config(text="AI's Turn (O)")
            self.window.after(500, self.ai_move)

    def ai_move(self):
        best_score, best_move = float("-inf"), None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(0, False, float("-inf"), float("inf"))
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score, best_move = score, (i, j)

        if best_move:
            row, col = best_move
            self.board[row][col] = "O"
            self.buttons[row][col]["text"] = "O"
            self.buttons[row][col]["bg"] = self.colors["O"]
            if self.check_win("O"):
                self.ai_wins += 1
                messagebox.showinfo("Game Over", "AI Wins!")
                self.update_score()
                return
            self.player_turn = "X"
            self.status_label.config(text="Your Turn (X)")

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_win("X"): return -10 + depth
        if self.check_win("O"): return 10 - depth
        if all(self.board[i][j] != "" for i in range(3) for j in range(3)): return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False, alpha, beta)
                        self.board[i][j] = ""
                        best_score = max(best_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True, alpha, beta)
                        self.board[i][j] = ""
                        best_score = min(best_score, score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return best_score

    def check_win(self, player):
        for row in self.board:
            if all(cell == player for cell in row): return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)): return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def update_score(self):
        self.score_label.config(text=f"Player: {self.player_wins}  AI: {self.ai_wins}")
        self.reset_board()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
 