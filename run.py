import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

# importing game runners
from games.snake.snake import run_snake
from games.tetris.tetris import run_tetris

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


def snake_run_handler(current_window):
    try:
        current_window.withdraw()
        run_snake()
    except Exception as e:
        print('Error occured:', str(e))

    current_window.deiconify()


def tetris_run_handler(current_window):
    try:
        current_window.withdraw()
        run_tetris()
    except Exception as e:
        print('Error occured:', str(e))

    current_window.deiconify()


# add buttons
btn1 = tk.Button(games_frame, image=snake_picture, command=partial(snake_run_handler, root))
btn1.grid(row=0, column=0, sticky='we')

btn2 = tk.Button(games_frame, image=tetris_picture, command=partial(tetris_run_handler, root))
btn2.grid(row=0, column=1, sticky='we')

btn3 = tk.Button(games_frame, image=snake_picture, command=partial(snake_run_handler, root))
btn3.grid(row=0, column=2, sticky='we')

games_frame.pack()

root.eval('tk::PlaceWindow . center') # center main window
root.mainloop()