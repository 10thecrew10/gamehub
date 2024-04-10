import tkinter as tk
from tkinter import Canvas, Scrollbar
from PIL import Image, ImageTk
from functools import partial

# Importing game runners
from games.snake.snake import run_snake
from games.tetris.tetris import run_tetris
from games.flappy_bird.main import run_flappy_bird

MAX_ITEMS_IN_ROW = 3
IMAGE_SIZE = (150, 150)

# Main window
root = tk.Tk()

# Title for the main window
root.title("GameHub Menu")

# Label for output on the window
label = tk.Label(root, text="Choose the game you want to play")
label.pack()

# Creating a canvas for buttons with scrollbar
canvas = Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Creating a frame for buttons inside the canvas
games_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=games_frame, anchor="nw")

# Configuring columns in the frame
for i in range(MAX_ITEMS_IN_ROW):
    games_frame.columnconfigure(i, weight=1)

# Loading game images
snake_image = ImageTk.PhotoImage(Image.open("games/snake/snake.png").resize(IMAGE_SIZE))
tetris_image = ImageTk.PhotoImage(Image.open("games/tetris/tetris.png").resize(IMAGE_SIZE))
flappy_bird_image = ImageTk.PhotoImage(Image.open("games/flappy_bird/flappy_bird.png").resize(IMAGE_SIZE))

# Function to run games with exception handling
def game_runner_decorator(game_runner: callable, current_window):
    def wrapper_function():
        try:
            current_window.withdraw()
            game_runner()
        except Exception as e:
            print('Error occured:', str(e))
        finally:
            current_window.deiconify()

    wrapper_function()

# Creating buttons and labels containers
buttons = []
games_pack = [(snake_image, run_snake), (tetris_image, run_tetris), (flappy_bird_image, run_flappy_bird),
              (snake_image, run_snake), (tetris_image, run_tetris), (flappy_bird_image, run_flappy_bird),
              (snake_image, run_snake), (tetris_image, run_tetris), (flappy_bird_image, run_flappy_bird),
              (snake_image, run_snake), (tetris_image, run_tetris), (flappy_bird_image, run_flappy_bird)]

games_pack = games_pack + games_pack.copy()

button_container = None
for i, (game_image, game_runner) in enumerate(games_pack):
    game_name = ''
    if game_runner == run_snake:
        game_name = 'Snake'
    elif game_runner == run_tetris:
        game_name = 'Tetris'
    elif game_runner == run_flappy_bird:
        game_name = 'Flappy Bird'

    button_container = tk.Frame(games_frame)
    button_container.grid(row=i // MAX_ITEMS_IN_ROW, column=i % MAX_ITEMS_IN_ROW)

    button = tk.Button(button_container, image=game_image, command=partial(game_runner_decorator, game_runner, root))
    button.pack()

    label = tk.Label(button_container, text=game_name)
    label.pack()

    buttons.append(button)

# Adding scrollbar
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Bind scrollbar to canvas
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.update() # place widgets

container_width = button_container.winfo_reqwidth()
container_height = button_container.winfo_reqheight()
res_width = container_width * MAX_ITEMS_IN_ROW + MAX_ITEMS_IN_ROW * 10
res_height = container_height * 4 + 4 * 6
root.minsize(res_width, res_height) # set width and height for pretty view

screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - (res_width / 2)
y = (screen_height / 2) - (res_height / 2)

root.geometry('%dx%d+%d+%d' % (res_width, res_height, x, y))
root.mainloop()