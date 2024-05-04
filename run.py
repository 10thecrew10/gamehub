import tkinter as tk
from tkinter import Canvas, Frame, Label, Button, Scrollbar, messagebox, font
from PIL import Image, ImageTk
from functools import partial

# Importing game runners
from games.snake.snaky import run_snake
from games.tetris.tetris import run_tetris
from games.flappy_bird.main import run_flappy_bird
from utils import game_runner_decorator
# Importing db funcs
from user_db import *

MAX_ITEMS_IN_ROW = 3
IMAGE_SIZE = (150, 150)

class CustomTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_font = font.Font(family="Helvetica", size=10)

class LoginWindow(CustomTk):
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
        title_label = Label(main_frame, text="GameHub Login/Register", font=self.global_font)
        title_label.pack(pady=10)

        # Create frame for buttons
        buttons_frame = Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Register button
        register_button = Button(buttons_frame, text="Register", width=10, command=self.open_register_popup, font=self.global_font)
        register_button.grid(row=0, column=0, padx=5)

        # Login button
        login_button = Button(buttons_frame, text="Login", width=10, command=self.open_login_popup, font=self.global_font)
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
        username_label = Label(popup, text="Enter your username:", font=self.global_font)
        username_label.pack(pady=5)
        username_entry = tk.Entry(popup)
        username_entry.pack(pady=5, padx=10)

        # Password label and entry
        password_label = Label(popup, text="Enter your password:", font=self.global_font)
        password_label.pack(pady=5)
        password_entry = tk.Entry(popup, show='*')
        password_entry.pack(pady=5, padx=10)

        # Repeat password label and entry
        repeat_password_label = Label(popup, text="Repeat your password:", font=self.global_font)
        repeat_password_label.pack(pady=5)
        repeat_password_entry = tk.Entry(popup, show='*')
        repeat_password_entry.pack(pady=5, padx=10)

        # Submit button
        submit_button = Button(popup, text="Register",
                               command=lambda: self.register(username_entry.get(), password_entry.get(),
                                                             repeat_password_entry.get(), popup))
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
        username_label = Label(popup, text="Enter your username:", font=self.global_font)
        username_label.pack(pady=5)
        username_entry = tk.Entry(popup)
        username_entry.pack(pady=5, padx=10)

        # Password label and entry
        password_label = Label(popup, text="Enter your password:", font=self.global_font)
        password_label.pack(pady=5)
        password_entry = tk.Entry(popup, show='*')
        password_entry.pack(pady=5, padx=10)

        # Submit button
        submit_button = Button(popup, text="Login",
                               command=lambda: self.login(username_entry.get(), password_entry.get(), popup))
        submit_button.pack(pady=10)

    def open_popup(self, title, username_text, password_text, repeat_password_text, callback):
        popup = tk.Toplevel(self)
        popup.title(title)

        # Username label and entry
        username_label = Label(popup, text=username_text, font=self.global_font)
        username_label.pack(pady=5)
        username_entry = tk.Entry(popup)
        username_entry.pack(pady=5)

        # Password label and entry
        password_label = Label(popup, text=password_text, font=self.global_font)
        password_label.pack(pady=5)
        password_entry = tk.Entry(popup, show='*')
        password_entry.pack(pady=5)

        if repeat_password_text:
            # Repeat password label and entry
            repeat_password_label = Label(popup, text=repeat_password_text, font=self.global_font)
            repeat_password_label.pack(pady=5)
            repeat_password_entry = tk.Entry(popup, show='*')
            repeat_password_entry.pack(pady=5)
        else:
            repeat_password_entry = None

        # Submit button
        submit_button = Button(popup, text=title, command=lambda: callback(username_entry.get(), password_entry.get(),
                                                                           repeat_password_entry.get() if repeat_password_entry else None))
        submit_button.pack(pady=10)

    def register(self, username, password, repeat_password, toplevel_window):
        if username and password and repeat_password:
            if password == repeat_password:
                success, message = register(username, password)
                if success:
                    messagebox.showinfo("Success", message)
                    self.destroy()
                    self.open_menu(username)
                else:
                    messagebox.showerror("Error", message)
            else:
                messagebox.showerror("Error", "Passwords do not match.")
                toplevel_window.lift()

    def login(self, username, password, toplevel_window):
        if username and password:
            success, message = login(username, password)
            if success:
                messagebox.showinfo("Success", message)
                self.destroy()
                self.open_menu(username)
            else:
                messagebox.showerror("Error", message)
                toplevel_window.lift()


    def open_menu(self, username: str):
        root = MenuWindow(username)
        try:
            root.grab_set()  # Make the window appear on top of all other windows
        except tk.TclError:
            print('See you later!')
        root.mainloop()


class MenuWindow(CustomTk):
    def __init__(self, username: str):
        super().__init__()
        self.geometry("340x180")
        self.title('Menu')

        self.username = username

        self.frame = tk.Frame(self, pady=5, padx=5, borderwidth=2, relief="groove")
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_label = tk.Label(self.frame, text=f'User: {self.username}', font=self.global_font)
        self.user_label.grid(row=0, column=0, sticky=tk.W)

        self.game_selection_btn = tk.Button(self.frame, text='View games',
                                            command=self.open_game_selection_window, font=self.global_font)
        self.game_selection_btn.grid(row=1, column=0, sticky=tk.W + tk.E, columnspan=3, pady=5, padx=10)

        self.highscores = tk.Button(self.frame, text='Highscores', font=self.global_font,
                                    command=self.open_highscores_window)
        self.highscores.grid(row=2, column=0, sticky=tk.W + tk.E, columnspan=3, pady=5, padx=10)

        self.exit_button = tk.Button(self.frame, text='Logout', command=self.back_to_previous, font=self.global_font)
        self.exit_button.grid(row=3, column=0, sticky=tk.W + tk.E, columnspan=3, pady=5, padx=10)

        # Настройка ширин столбцов
        for col in range(3):
            self.frame.grid_columnconfigure(col, weight=1)

        self.update_idletasks()  # Обновляем виджеты, чтобы они появились на экране

        # Получаем размеры экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Получаем размеры окна
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Вычисляем координаты для размещения окна по центру экрана
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Устанавливаем координаты окна
        self.geometry('+{}+{}'.format(x, y))

    def open_game_selection_window(self):
        self.destroy()
        GameSelectionWindow(self.username).mainloop()

    def open_highscores_window(self):
        self.destroy()
        HighScores(self.username).mainloop()

    def back_to_previous(self):
        # Закрыть текущее окно
        self.destroy()
        # Создать предыдущее окно
        LoginWindow().mainloop()


class GameSelectionWindow(CustomTk):
    def __init__(self, username: str):
        super().__init__()

        self.username = username
        self.user_id = get_user_id_by_username(username)
        self.title("GameHub Menu")

        back_btn = tk.Button(self, text='Back', command=self.back_to_previous, font=self.global_font)
        back_btn.pack(fill='both', padx=25, pady=10)

        # Label for output on the window
        label = tk.Label(self, text=f"Welcome, {self.username}! Choose the game", font=self.global_font)
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
        self.snake_image = ImageTk.PhotoImage(Image.open("games/snake/snake.png").resize(IMAGE_SIZE), master=self)
        self.tetris_image = ImageTk.PhotoImage(Image.open("games/tetris/tetris.png").resize(IMAGE_SIZE), master=self)
        self.flappy_bird_image = ImageTk.PhotoImage(Image.open("games/flappy_bird/flappy_bird.png").resize(IMAGE_SIZE), master=self)

        # Creating buttons and labels containers
        buttons = []
        snake_id = get_game_id_by_name('Snake')
        tetris_id = get_game_id_by_name('Tetris')
        flappybird_id = get_game_id_by_name('Flappy Bird')
        games_pack = [(self.snake_image, partial(run_snake, snake_id, self.user_id)),
                      (self.tetris_image, partial(run_tetris, tetris_id, self.user_id)),
                      (self.flappy_bird_image, partial(run_flappy_bird, flappybird_id, self.user_id)),
                      (self.snake_image, partial(run_snake, snake_id, self.user_id)),
                      (self.tetris_image, partial(run_tetris, tetris_id, self.user_id)),
                      (self.flappy_bird_image, partial(run_flappy_bird, flappybird_id, self.user_id)),
                      ]

        games_pack = games_pack + games_pack.copy() + games_pack.copy()
        button_container = None

        for i, (game_image, game_runner) in enumerate(games_pack):
            game_name = ''
            if game_runner.args[0] == snake_id:
                game_name = 'Snake'
            elif game_runner.args[0] == tetris_id:
                game_name = 'Tetris'
            elif game_runner.args[0] == flappybird_id:
                game_name = 'Flappy Bird'

            button_container = tk.Frame(games_frame)
            button_container.grid(row=i // MAX_ITEMS_IN_ROW, column=i % MAX_ITEMS_IN_ROW)
            button = tk.Button(button_container, image=game_image,
                               command=partial(game_runner_decorator, game_runner, self))
            button.pack()

            label = tk.Label(button_container, text=game_name, font=self.global_font)
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

    def back_to_previous(self):
        # Закрыть текущее окно
        self.destroy()
        # Создать предыдущее окно
        MenuWindow(self.username).mainloop()


class HighScores(CustomTk):
    def __init__(self, username):
        super().__init__()
        self.title('Highscores')

        self.username = username

        frame = tk.Frame(self, pady=10, padx=50)
        frame.pack()

        name_label = tk.Button(frame, text='Back', command=self.back_to_previous, font=self.global_font)
        name_label.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.E, pady=5)

        surname_label = tk.Label(frame, text='Snake highscores', pady=5, font=self.global_font)
        surname_label.grid(row=1, column=0, sticky=tk.W + tk.E)

        # Текстовое поле для отображения добавленных студентов
        self.snake_list = tk.Listbox(frame, font=self.global_font, width=25, height=6, borderwidth=4, relief="groove")
        self.snake_list.grid(row=2, column=0, columnspan=3, pady=5, sticky=tk.W + tk.E)

        surname_label = tk.Label(frame, text='Tetris highscores', pady=5, font=self.global_font)
        surname_label.grid(row=3, column=0, sticky=tk.W + tk.E)

        self.tetris_list = tk.Listbox(frame, font=self.global_font, width=25, height=6, borderwidth=4, relief="groove")
        self.tetris_list.grid(row=4, column=0, columnspan=3, pady=5, sticky=tk.W + tk.E)

        surname_label = tk.Label(frame, text='Flappy Bird highscores', pady=5, font=self.global_font)
        surname_label.grid(row=5, column=0, sticky=tk.W + tk.E)

        self.flappy_bird_list = tk.Listbox(frame, font=self.global_font, width=25, height=6, borderwidth=4, relief="groove")
        self.flappy_bird_list.grid(row=6, column=0, columnspan=3, pady=5, sticky=tk.W + tk.E)

        self.add_highscores()

        self.eval('tk::PlaceWindow . center')

    def add_highscores(self):
        snake_id = get_game_id_by_name('snake')
        for elem in get_top_5_highscores(snake_id):
            self.snake_list.insert(tk.END, f'User - {elem[2]}, Score - {elem[1]}')

        tetris_id = get_game_id_by_name('tetris')
        for elem in get_top_5_highscores(tetris_id):
            self.tetris_list.insert(tk.END, f'User - {elem[2]}, Score - {elem[1]}')

        flappy_bird_id = get_game_id_by_name('flappy bird')
        for elem in get_top_5_highscores(flappy_bird_id):
            self.flappy_bird_list.insert(tk.END, f'User - {elem[2]}, Score - {elem[1]}')

    def back_to_previous(self):
        # Закрыть текущее окно
        self.destroy()
        # Создать предыдущее окно
        MenuWindow(self.username).mainloop()



if __name__ == "__main__":
    create_tables()  # Create users table
    login_window = LoginWindow()
    login_window.mainloop()
