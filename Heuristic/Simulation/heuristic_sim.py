# simulation for value iteration algorithm

import game_funcs as gf
import game as game
import time
from random import randint as ri
import math
import Heuristic_Policy as hp

# Initial game parameters
pelletLocX = 2;
pelletLocY = 0;

row, col = (3,3);
gridSize = row*col;
numStates = gridSize*gridSize;
directions = 4;

moves = [];
ended=False

def grid_to_xy(number):
    switch = {
        0: [0,0],
        1: [1,0],
        2: [2,0],
        3: [0,1],
        4: [1,1],
        5: [2,1],
        6: [0,2],
        7: [1,2],
        8: [2,2]
    }
    return switch.get(number, "invalid entry")

def xy_to_grid(x,y):
    switch = {
        0: {0:0, 1:3, 2:6},
        1: {0:1, 1:4, 2:7},
        2: {0:2, 1:5, 2:8}
    }
    x = switch.get(x,"invalid entry")

    if x == "invalid entry":
        return x
    else:
        return x.get(y,"invalid entry")

###############################################################################
############################  Game Simulation #################################
###############################################################################
gm = game.Game(col,row);
policy = hp.heuristic_policy();
env = hp.PacmanEnv();

## Random spawn
pacman_x, pacman_y = 0,2;
while (pacman_x==gm.goal_x and pacman_y==gm.goal_y):
    pacman_x = ri(0,col-1);
    pacman_y = ri(0,row-1);

ghost_x, ghost_y = 2,0;
while (ghost_x==gm.goal_x and ghost_y==gm.goal_y) or (ghost_x==pacman_x and ghost_y==pacman_y):
    ghost_x = ri(0,col-1);
    ghost_y = ri(0,row-1);

# pacman_x, pacman_y = 0,2;
# ghost_x, ghost_y = 2,2;

gm.updateState(pacman_x, pacman_y, ghost_x, ghost_y); # update internal grid

## Start game
while not gm.ended:
    gm.update(); # update graphics
    time.sleep(0.5)
    # Get state (0 to numStates-1) from pacman and ghost coordinates
    p = xy_to_grid(gm.pacman_x, gm.pacman_y);
    g = xy_to_grid(gm.ghost_x, gm.ghost_y);
    state = env.states.index( (p,g) );

    ###########################################################################
    ########################## For Thuy to Change #############################
    # Use your policy function
    # Make sure that the that your action (1 to 4) aligns with the pacman direction of movement in game_func
    # My policy[state] outputs 0 to 3, that's why I add 1, because Steven's actions go 1 to 4
    move = policy[state].tolist().index(1) + 1;

    ###########################################################################

    # Get game status given current state and move (action)
    pacman_x2, pacman_y2, ghost_x2, ghost_y2, gm.goal_x, gm.goal_y, gm.ended, gm.won, gm.moved = gf.game_func(move, gm.pacman_x, gm.pacman_y, gm.ghost_x, gm.ghost_y, gm.goal_x,gm.goal_y,col,row);
    gm.moves.append(move);
    gm.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2); # update internal grid
# Update one last time before game end
gm.update(); 