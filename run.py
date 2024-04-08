import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

# importing game runners
from games.snake.snake import run_snake
from games.tetris.tetris import run_tetris
from games.flappy_bird.main import run_flappy_bird

# main window
root = tk.Tk()

# giving title to the main window
root.title("GameHub Menu")

# Label is what output will be
# show on the window
label = tk.Label(root, text="Choose the game you want to play").pack()

games_frame = tk.Frame(root)
games_frame.columnconfigure(0, weight=1)
games_frame.columnconfigure(1, weight=1)
games_frame.columnconfigure(2, weight=1)


image = Image.open("games/snake/snake.png")  # Read the Image
resize_image = image.resize((150, 150))  # Resize the image
snake_picture = ImageTk.PhotoImage(resize_image)

image = Image.open("games/tetris/tetris.png")  # Read the Image
resize_image = image.resize((150, 150))  # Resize the image
tetris_picture = ImageTk.PhotoImage(resize_image)

image = Image.open("games/flappy_bird/flappy_bird.png")  # Read the Image
resize_image = image.resize((150, 150))  # Resize the image
flappy_bird_picture = ImageTk.PhotoImage(resize_image)


def game_runner_decorator(game_runner: callable, current_window):
    def wrapper_function():
        print('Called')
        try:
            current_window.withdraw()
            game_runner()
        except Exception as e:
            print('Error occured:', str(e))

        current_window.deiconify()

    wrapper_function()


# add buttons
btn1 = tk.Button(games_frame, image=snake_picture, command=partial(game_runner_decorator, run_snake, root))
btn1.grid(row=0, column=0, sticky='we')

btn2 = tk.Button(games_frame, image=tetris_picture, command=partial(game_runner_decorator, run_tetris, root))
btn2.grid(row=0, column=1, sticky='we')

btn3 = tk.Button(games_frame, image=flappy_bird_picture, command=partial(game_runner_decorator, run_flappy_bird, root))
btn3.grid(row=0, column=2, sticky='we')

games_frame.pack()

root.eval('tk::PlaceWindow . center') # center main window
root.mainloop()