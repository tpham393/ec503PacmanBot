import time
from random import randint as ri
import math
import game_funcs_multGhosts as g
from game_multGhosts import Game
from policyIteration_multGhosts import *

##########3 Change the following before running
col, row = (4,4); 
numGhosts = 2;
f = open("policy_grid4x4_ghosts2.txt",'r');
##################################################
policy = [];
line = f.readline();
while line:
    line = line[0:-1];
    policy.append(int(line));
    line = f.readline();

###############################################################################
############################  Game Simulation #################################
###############################################################################
game = Game(col,row);

## Random spawn
pacman_x, pacman_y = 2,0;
while (pacman_x==game.goal_x and pacman_y==game.goal_y):
    pacman_x = ri(0,col-1);
    pacman_y = ri(0,row-1);

ghost_x = [];
ghost_y = [];
it = 1;
while (it <= numGhosts):
    test_x = ri(0,col-1);
    test_y = ri(0,row-1);
    if (test_x!=game.goal_x or test_y!=game.goal_y) and (test_x!=pacman_x or test_y!=pacman_y):
        valid = True;
        for i in range(len(ghost_x)):
            if (test_x == ghost_x[i] and test_y == ghost_y[i]):
                valid = False;
        if (valid):
            ghost_x.append(test_x);
            ghost_y.append(test_y);
            it+=1


game.updateState(pacman_x, pacman_y, ghost_x, ghost_y, numGhosts); # update internal grid

## Start game
while not game.ended:
    game.update(); # update graphics
    time.sleep(1.3);
    # Get state (0 to numStates-1) from pacman and ghost coordinates
    state = coord2state(game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y);

    ###########################################################################
    ########################## For Thuy to Change #############################
    # Use your policy function
    # Make sure that the that your action (1 to 4) aligns with the pacman direction of movement in game_func
    # My policy[state] outputs 0 to 3, that's why I add 1, because Steven's actions go 1 to 4
    move = policy[state] + 1;
    ###########################################################################

    # Get game status given current state and move (action)
    pacman_x2, pacman_y2, ghost_x2, ghost_y2, game.goal_x, game.goal_y, game.ended, game.won = g.game_func(move, game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, game.goal_x,game.goal_y,col,row,numGhosts);
    game.moves.append(move);
    game.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2, numGhosts); # update internal grid
# Update one last time before game end
game.update(); 
