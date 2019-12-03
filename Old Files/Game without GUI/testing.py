# test function for the mini game
# This test code will run one iteration of the game and will print out the moves that were taken
# (You can also keep track of the positions of each item and change the initial conditions here, 
# just not grid_size which is changed in the game_funcs initial conditions)

import game_funcs as g
from random import randint as ri

pacman_x, pacman_y = 1, 3;
ghost_x, ghost_y = 3, 3;
goal_x, goal_y = 3, 1;
moves = [];
ended=False

x, y = g.ghost_move(ghost_x, ghost_y)
print(x)
print(y)
    
print(moves)