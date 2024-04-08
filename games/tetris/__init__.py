import os
import sys

# Curr dir of the project
current_dir = os.path.dirname(os.path.realpath(__file__))

# form the path
games = os.path.join(current_dir)

# add var to PYTHONPATH
sys.path.append(games)
