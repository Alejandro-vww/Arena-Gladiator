import tkinter as tk
from tkinter import ttk

from central_unit import playing_function  # Importing a function, assuming it's used somewhere


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arena Gladiator")
        self.geometry("380x110")

        # Create a main frame for the layout
        frame_main = tk.Frame(self)
        frame_main.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)  # Fill entire cell

        # "Number of victories" label
        self.number_label = tk.Label(frame_main, text="Number of victories:")
        self.number_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Entry for the number of wins, with half the length
        self.number_entry = tk.Entry(frame_main, width=7)
        self.number_entry.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="w")
        self.number_entry.insert(0, '15')

        # "Shut down when finished" checkbox and label
        self.shutdown_label = tk.Label(frame_main, text="Shut down when done")
        self.shutdown_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.shutdown_var = tk.BooleanVar()
        self.shutdown_check = ttk.Checkbutton(frame_main, variable=self.shutdown_var)
        self.shutdown_check.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="w")

        # "Play" button
        self.play_button = tk.Button(self, text="Play", command=self.play_action, bg="green", fg="white")
        self.play_button.config(width=15, height=2)  # Adjust button size
        self.play_button.grid(row=0, column=1, rowspan=2, sticky="ns", padx=(0, 20), pady=10)  # Stretch vertically

        # Bottom error message frame
        self.error_message = tk.Label(self, text="", fg="red", anchor="w")
        self.error_message.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 10))

        # Configure row and column weights for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def play_action(self):
        number_of_wins = self.number_entry.get()
        shutdown = self.shutdown_var.get()

        # Validate the input
        try:
            number_of_wins = int(number_of_wins)
            if number_of_wins <= 0:
                raise ValueError
        except ValueError:
            self.error_message.config(text="Please enter a valid number of victories", fg="red")
            return

        # Clear the error message if input is valid
        self.error_message.config(text="")

        # Handle the valid input
        playing_function(number_of_wins, shutdown)



if __name__ == "__main__":
    app = Application()
    app.mainloop()
