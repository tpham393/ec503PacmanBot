import time
from random import randint as ri
import game_funcs as g
from game import Game
from policyIteration import *


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



##########3 Change the following before running
col, row = (7,7); 
num_ghosts = 2;
grid_len = 7;
#f = open("valueIter.txt",'r');
#f = open("policyIter.txt",'r');
f = open("qLearning_eps100000.txt",'r');


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
game = Game();    
pacman_x,pacman_y = 5,1;
ghost_x = [2, 3];
ghost_y = [5, 1];
game.updateState(pacman_x, pacman_y, ghost_x, ghost_y, num_ghosts); # update internal grid

## Start game
while not game.ended:
    game.update(); # update graphics
    time.sleep(0.5);
    # Get state (0 to numStates-1) from pacman and ghost coordinates
    state = coord2state(game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, num_ghosts, grid_len);

    # My policy[state] outputs 0 to 3, that's why I add 1, because Steven's actions go 1 to 4
    move = policy[state] + 1;

    # Get game status given current state and move (action)
    pacman_x2, pacman_y2, ghost_x2, ghost_y2, game.goal_x, game.goal_y, game.ended, game.won = g.game_func(move, game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, game.goal_x, game.goal_y, game.grid, 2, ['Chase','Random']);
    game.moves.append(move);
    game.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2, num_ghosts); # update internal grid
# Update one last time before game end
game.update(); 