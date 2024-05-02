import tkinter as tk
from tkinter import Canvas, Frame, Label, Button, Scrollbar, simpledialog, messagebox
from PIL import Image, ImageTk
from functools import partial

# Importing game runners
from games.snake.snake import run_snake
from games.tetris.tetris import run_tetris
from games.flappy_bird.main import run_flappy_bird
from utils import game_runner_decorator
# Importing db funcs
from user_db import *

MAX_ITEMS_IN_ROW = 3
IMAGE_SIZE = (150, 150)


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login / Register")

        # Centering the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 300
        window_height = 200
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create main frame
        main_frame = Frame(self)
        main_frame.pack(expand=True)

        # Label for title
        title_label = Label(main_frame, text="GameHub Login/Register", font=("Arial", 16))
        title_label.pack(pady=10)

        # Create frame for buttons
        buttons_frame = Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Register button
        register_button = Button(buttons_frame, text="Register", width=10, command=self.open_register_popup)
        register_button.grid(row=0, column=0, padx=5)

        # Login button
        login_button = Button(buttons_frame, text="Login", width=10, command=self.open_login_popup)
        login_button.grid(row=0, column=1, padx=5)

    def open_register_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Register")

        # Centering the popup window
        popup_width = 350  # Увеличиваем ширину окна
        popup_height = 250  # Увеличиваем высоту окна
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        # Username label and entry
        username_label = Label(popup, text="Enter your username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(popup)
        username_entry.pack(pady=5, padx=10)

        # Password label and entry
        password_label = Label(popup, text="Enter your password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(popup, show='*')
        password_entry.pack(pady=5, padx=10)

        # Repeat password label and entry
        repeat_password_label = Label(popup, text="Repeat your password:")
        repeat_password_label.pack(pady=5)
        repeat_password_entry = tk.Entry(popup, show='*')
        repeat_password_entry.pack(pady=5, padx=10)

        # Submit button
        submit_button = Button(popup, text="Register",
                               command=lambda: self.register(username_entry.get(), password_entry.get(),
                                                             repeat_password_entry.get()))
        submit_button.pack(pady=10)

    def open_login_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Login")

        # Centering the popup window
        popup_width = 350  # Увеличиваем ширину окна
        popup_height = 200  # Меняем высоту окна
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        # Username label and entry
        username_label = Label(popup, text="Enter your username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(popup)
        username_entry.pack(pady=5, padx=10)

        # Password label and entry
        password_label = Label(popup, text="Enter your password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(popup, show='*')
        password_entry.pack(pady=5, padx=10)

        # Submit button
        submit_button = Button(popup, text="Login",
                               command=lambda: self.login(username_entry.get(), password_entry.get(), None))
        submit_button.pack(pady=10)

    def open_popup(self, title, username_text, password_text, repeat_password_text, callback):
        popup = tk.Toplevel(self)
        popup.title(title)

        # Username label and entry
        username_label = Label(popup, text=username_text)
        username_label.pack(pady=5)
        username_entry = tk.Entry(popup)
        username_entry.pack(pady=5)

        # Password label and entry
        password_label = Label(popup, text=password_text)
        password_label.pack(pady=5)
        password_entry = tk.Entry(popup, show='*')
        password_entry.pack(pady=5)

        if repeat_password_text:
            # Repeat password label and entry
            repeat_password_label = Label(popup, text=repeat_password_text)
            repeat_password_label.pack(pady=5)
            repeat_password_entry = tk.Entry(popup, show='*')
            repeat_password_entry.pack(pady=5)
        else:
            repeat_password_entry = None

        # Submit button
        submit_button = Button(popup, text=title, command=lambda: callback(username_entry.get(), password_entry.get(),
                                                                           repeat_password_entry.get() if repeat_password_entry else None))
        submit_button.pack(pady=10)

    def register(self, username, password, repeat_password):
        if username and password and repeat_password:
            if password == repeat_password:
                success, message = register(username, password)
                if success:
                    messagebox.showinfo("Success", message)
                    self.destroy()
                    self.open_game_selection_window(username)
                else:
                    messagebox.showerror("Error", message)
            else:
                messagebox.showerror("Error", "Passwords do not match.")

    def login(self, username, password, _):
        if username and password:
            success, message = login(username, password)
            if success:
                messagebox.showinfo("Success", message)
                self.destroy()
                self.open_game_selection_window(username)
            else:
                messagebox.showerror("Error", message)

    def open_game_selection_window(self, username: str):
        root = GameSelectionWindow(username)
        try:
            root.grab_set()  # Make the window appear on top of all other windows
        except tk.TclError:
            print('See you later!')
        root.mainloop()


class GameSelectionWindow(tk.Tk):
    def __init__(self, username: str):
        super().__init__()

        self.username = username
        self.user_id = get_user_id_by_username(username)
        self.title("GameHub Menu")

        # Label for output on the window
        label = tk.Label(self, text=f"Welcome, {self.username}! Choose the game you want to play")
        label.pack()

        # Creating a canvas for buttons with scrollbar
        canvas = Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)

        # Creating a frame for buttons inside the canvas
        games_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=games_frame, anchor="nw")

        # Configuring columns in the frame
        for i in range(MAX_ITEMS_IN_ROW):
            games_frame.columnconfigure(i, weight=1)

        # Loading game images
        self.snake_image = ImageTk.PhotoImage(Image.open("games/snake/snake.png").resize(IMAGE_SIZE))
        self.tetris_image = ImageTk.PhotoImage(Image.open("games/tetris/tetris.png").resize(IMAGE_SIZE))
        self.flappy_bird_image = ImageTk.PhotoImage(Image.open("games/flappy_bird/flappy_bird.png").resize(IMAGE_SIZE))

        # Creating buttons and labels containers
        buttons = []
        games_pack = [(self.snake_image, partial(run_snake, 1, self.user_id)),
                      (self.tetris_image, partial(run_tetris, 2, self.user_id)),
                      (self.flappy_bird_image, partial(run_flappy_bird, 3, self.user_id)),
                      (self.snake_image, partial(run_snake, 1, self.user_id)),
                      (self.tetris_image, partial(run_tetris, 2, self.user_id)),
                      (self.flappy_bird_image, partial(run_flappy_bird, 3, self.user_id)),
                      ]

        games_pack = games_pack + games_pack.copy() + games_pack.copy()
        button_container = None

        for i, (game_image, game_runner) in enumerate(games_pack):
            game_name = ''
            if game_runner.args[0] == get_game_id_by_name('Snake'):
                game_name = 'Snake'
            elif game_runner.args[0] == get_game_id_by_name('Tetris'):
                game_name = 'Tetris'
            elif game_runner.args[0] == get_game_id_by_name('Flappy Bird'):
                game_name = 'Flappy Bird'

            button_container = tk.Frame(games_frame)
            button_container.grid(row=i // MAX_ITEMS_IN_ROW, column=i % MAX_ITEMS_IN_ROW)

            button = tk.Button(button_container, image=game_image,
                               command=partial(game_runner_decorator, game_runner, self))
            button.pack()

            label = tk.Label(button_container, text=game_name)
            label.pack()

            buttons.append(button)

        # Adding scrollbar
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind scrollbar to canvas
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.update()  # place widgets

        container_width = button_container.winfo_reqwidth()
        container_height = button_container.winfo_reqheight()
        res_width = container_width * MAX_ITEMS_IN_ROW + MAX_ITEMS_IN_ROW * 10
        res_height = container_height * 4 + 4 * 6
        self.minsize(res_width, res_height)  # set width and height for pretty view

        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (res_width / 2)
        y = (screen_height / 2) - (res_height / 2)

        self.geometry('%dx%d+%d+%d' % (res_width, res_height, x, y))
        self.mainloop()


if __name__ == "__main__":
    create_tables()  # Create users table
    login_window = LoginWindow()
    login_window.mainloop()
