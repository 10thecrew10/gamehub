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