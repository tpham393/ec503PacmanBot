import time
from random import randint as ri
from game import Game
import game_funcs as g
import math
import re
import pygame
import sys
import numpy as np

def coord2state(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY, num_ghosts, grid_len):
    '''
    Coverts pacman and ghost coordinates to state. 
    ARGS:
    pacmanLocX (int): X location of pacman
    pacmanLocY (int): Y location of pacman 
    ghostLocX (list): X locations of all ghost 
    ghostLocY (list): Y locations of all ghost 
    RETURN: 
    state: Game state, ranges 0 to numStates-1 
    '''
    # Linearize grid coordinates for all game objects
    pacmanLocLin = pacmanLocY*grid_len + pacmanLocX;
    ghostLocLin = [];
    for i in range(num_ghosts):
        ghostLocLin.append(ghostLocY[i]*grid_len + ghostLocX[i]);
    # Calculate state
    state = pacmanLocLin * math.pow(grid_len*grid_len,num_ghosts);
    for i in range(num_ghosts):
        state = state + ghostLocLin[i]*math.pow(grid_len*grid_len, num_ghosts-i-1);
    return int(state);



########## Change the following before running ################################
num_ghosts = 1;
grid_len = 5;
#f = open('heuristic_Random.txt', 'r');
#f = open("valueIter_Chase.txt",'r');
#f = open("valueIter_Random.txt",'r');
#f = open("policyIter_Chase.txt",'r');
f = open("policyIter_Random.txt",'r');
#f = open("qLearning_eps10000_Chase.txt",'r'); # change # episodes
f = open("qLearning_eps1000_Random.txt",'r'); # change # episodes
ghostType = ['Random'];


###############################################################################
# Read policy from file
policy = [];
line = f.readline();
while line:
    line = line[0:-1];
    policy.append(int(line));
    line = f.readline();


# Get ghost locations
f = open("ghostLocs.txt","r");
line = f.readline();
all_ghost_x = [];
all_ghost_y = [];
while line:
    line = line[0:-1];
    ghostx0, ghostx1, ghosty0, ghosty1 = re.split(' ',line);
    ghostLocX = [int(ghostx0),int(ghostx1)];
    ghostLocY = [int(ghosty0), int(ghosty1)];
    all_ghost_x.append(ghostLocX);
    all_ghost_y.append(ghostLocY);
    line = f.readline();

###############################################################################
############################  Game Simulation #################################
###############################################################################
game = Game();    

pacman_x,pacman_y = 1,3;
#ghost_x = [2];
#ghost_y = [2];


win_count = 0
winning_steps = []

for s in range(1): # run 100 simulations
    print(s);

    # Get random ghost location
    ghost_x = all_ghost_x[s];
    ghost_y = all_ghost_y[s];
    del ghost_x[1];
    del ghost_y[1];
    ghost_x = [2];
    ghost_y = [2];

    game = Game();    
    steps_to_win = 0
    game.updateState(pacman_x, pacman_y, ghost_x, ghost_y, num_ghosts, ghostType) # update internal grid

    ## Start game
    while not game.ended:
        game.update(); # update graphics
        time.sleep(0.5);
        # Get state (0 to numStates-1) from pacman and ghost coordinates
        state = coord2state(game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, num_ghosts, grid_len);
        # My policy[state] outputs 0 to 3, that's why I add 1, because Steven's actions go 1 to 4
        move = policy[state] + 1;
        steps_to_win += 1

        # Get game status given current state and move (action)
        pacman_x2, pacman_y2, ghost_x2, ghost_y2, game.goal_x, game.goal_y, game.ended, game.won = g.game_func(move, game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, game.goal_x, game.goal_y, game.grid, 1, ghostType);
        game.moves.append(move);
        game.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2, num_ghosts, ghostType); # update internal grid
    # Update one last time before game end
    game.update(); 

    if (game.won):
        win_count += 1
        winning_steps.append(steps_to_win) # does not add to list if game is lost

print('Total # of wins: ', win_count)
print(winning_steps)
print('Average # steps to win: ', np.mean(winning_steps))
pygame.display.quit()
pygame.quit()
sys.exit()