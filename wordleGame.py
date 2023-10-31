import tkinter as tk
import random

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")

        # Set window dimensions
        window_width = 400  # Adjust to your desired width
        window_height = 400  # Adjust to your desired height
        self.root.geometry(f"{window_width}x{window_height}")

        # Define the colors
        self.correct_color = "green"
        self.wrong_color = "yellow"
        self.default_color = "dark grey"
        self.bg_color = "white"
        
        # Cell size (adjust as needed)
        cell_size = 40

        # Initialize the grid
        self.grid = []
        self.current_row = 0

        # Calculate the center position for the grid
        center_x = window_width // 2
        center_y = window_height // 2
                
        # Calculate the starting position of the grid to keep it centered
        start_x = center_x - 2.5 * cell_size  # Adjust for grid size and cell_size
        start_y = center_y - 3 * cell_size  # Adjust for grid size and cell_size

        # Create the grid
        for i in range(6):
            row = []
            for j in range(5):
                cell = tk.Label(root, text="", width=4, height=2, bg=self.default_color, relief="solid", borderwidth=1)
                cell.place(x=start_x + j * cell_size, y=start_y + i * cell_size)
                row.append(cell)
            self.grid.append(row)

        # Load target word from a text file
        self.target_word = self.load_target_word('words-guess.txt')
        
        self.max_attempts = 6
        self.attempts = 0

        # Create the input field
        self.input_entry = tk.Entry(root, width=5)
        self.input_entry.bind("<Return>", self.check_word)
        self.input_entry.place(x=center_x - 2.5 * cell_size, y=start_y + 6 * cell_size)
        self.input_entry.focus_set()

    def load_target_word(self, file_path):
        try:
            with open(file_path, 'r') as file:
                words = file.read().split()
                return random.choice(words).upper()
        except Exception as e:
            print(f"Error loading target word: {e}")
            return "APPLE"  # Use a default word if loading fails

    def check_word(self, event):
        guess = self.input_entry.get().upper()  # Convert the input to uppercase
        self.input_entry.delete(0, tk.END)
        if len(guess) != 5:
            return

        used_indices = set()  # To track used indices in the target word
        used_letters = set()  # To track used letters in the target word

        for i in range(5):
            if guess[i] == self.target_word[i]:
                self.grid[self.current_row][i].config(text=guess[i], bg=self.correct_color)
                used_indices.add(i)
                used_letters.add(guess[i])
            else:
                self.grid[self.current_row][i].config(text=guess[i], bg=self.default_color)

        for i in range(5):
            if i not in used_indices and guess[i] in self.target_word:
                if guess[i] not in used_letters:
                    self.grid[self.current_row][i].config(bg=self.wrong_color)
                    used_letters.add(guess[i])

        self.current_row += 1

        if guess == self.target_word:
            self.game_over("You won!")
        elif self.current_row >= self.max_attempts:
            self.game_over(f"You lost! The word was {self.target_word}")

    def game_over(self, message):
        game_over_label = tk.Label(self.root, text=message, font=("Helvetica", 16))
        game_over_label.place(x=10, y=10)  # Position it in the top-left corner
        self.input_entry.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")
    game = WordleGame(root)
    root.mainloop()
