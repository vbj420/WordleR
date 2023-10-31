import tkinter as tk
import random
class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")

        # Set window dimensions
        window_width = 600
        window_height = 560
        self.root.geometry(f"{window_width}x{window_height}")

        # Define the colors
        self.correct_color = "green"
        self.wrong_color = "yellow"
        self.default_color = "dark grey"
        self.bg_color = "white"
        self.red_color = "red"

        # Cell size
        cell_size = 40

        # Initialize the grid
        self.grid = []
        self.current_row = 0

        # Calculate the center position for the grid
        center_x = window_width // 2
        center_y = window_height // 2

        # Calculate the starting position of the grid to keep it centered
        start_x = center_x - 2.5 * cell_size
        start_y = center_y - 3 * cell_size

        # Create the grid
        for i in range(6):
            row = []
            for j in range(5):
                cell = tk.Label(root, text="", width=4, height=2, bg=self.default_color, relief="solid", borderwidth=1, fg="black")
                cell.place(x=start_x + j * cell_size, y=start_y + i * cell_size)
                row.append(cell)
            self.grid.append(row)

        # Read a random target word from "word-guess.txt" without FileNotFoundError
        self.target_word = "WASTE"
        self.max_attempts = 6
        self.attempts = 0

        # Create the input field
        self.input_entry = tk.Entry(root, width=5)
        self.input_entry.bind("<Return>", self.check_word)
        self.input_entry.place(x=center_x - 2.5 * cell_size, y=start_y + 6 * cell_size)
        self.input_entry.focus_set()

        # Create the keyboard
        keyboard_letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
        self.keyboard_buttons = []
        self.used_keyboard_buttons = []
        for i, letter in enumerate(keyboard_letters):
            button = tk.Button(root, text=letter, command=lambda l=letter: self.keyboard_letter_click(l), fg="black")
            col = i % 10
            row = i // 10
            button.place(x=start_x + col * cell_size, y=start_y + 7 * cell_size + row * cell_size)
            self.keyboard_buttons.append(button)

        # Add a clear button at the bottom center
        clear_button = tk.Button(root, text="Clear", command=self.clear_input)
        clear_button.place(x=center_x - cell_size, y=start_y + 10 * cell_size)

    def get_random_word(self):
        try:
            with open("word_guess.TXT", "r", encoding="UTF-8") as file:
                words = file.read().splitlines()
            return random.choice(words).upper()
        except FileNotFoundError:
            print("The 'word-guess.txt' file was not found.")
            return "TRAIL"  # Provide a fallback word in case the file is missing.

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

                # Highlight incorrect cell backgrounds in red on the keyboard
                for button in self.keyboard_buttons:
                    letter = button["text"]
                    if letter == guess[i]:
                        button.config(bg=self.red_color)

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

        # Highlight used letters on the keyboard
        for button in self.keyboard_buttons:
            letter = button["text"]
            if letter in used_letters:
                if letter in self.target_word:
                    button.config(bg=self.correct_color)
                else:
                    button.config(bg=self.red_color)

        # Store used buttons in a separate list
        for letter in guess:
            for button in self.keyboard_buttons:
                if letter == button["text"]:
                    self.used_keyboard_buttons.append(button)
                    break

        # Disable used keyboard buttons
        for button in self.used_keyboard_buttons:
            button.config(state=tk.DISABLED)

    def keyboard_letter_click(self, letter):
        # Add the clicked letter to the input field
        current_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, current_input + letter)

    def clear_input(self):
        self.input_entry.delete(0, tk.END)

    def game_over(self, message):
        game_over_label = tk.Label(self.root, text=message, font=("Helvetica", 16))
        game_over_label.place(x=10, y=10)  # Position it in the top-left corner
        self.input_entry.config(state=tk.DISABLED)
        # Disable the remaining keyboard buttons
        for button in self.keyboard_buttons:
            button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")
    game = WordleGame(root)
    root.mainloop()
