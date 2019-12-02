# Functions:
# ghost_move is the function that chooses the next space for the ghost to move
# game_func is the function that the user controls the game with

# Inputs:
# move: the next move for the user
# pacman_x, pacman_y: the current x and y position of pacman
# ghost_x, ghost_y: the current x and y position of the ghost
# goal_x, goal_y: the x and y location of the goal
# (The above variables must be within the gridsize which is set in this function and can be changed)

# Outputs:
# pacman_x, pacman_y: the current x and y position of pacman
# t_x, t_y: the current x and y position of the ghost
# goal_x, goal_y: the x and y location of the goal
# ended: whether the game has ended or not
# won: whether or not you reached the goal
# moved: whether you made a valid move or not

import math
import random
import time

random_ghost = True; #Ghost movement random or chases you.

# Random Moving Ghost.
def ghost_move(ghost_x, ghost_y, grid): 
    t_x = ghost_x;
    t_y = ghost_y;
    ghost_m = random.randint(1,4)
    if (ghost_m == 1) and not (grid[ghost_y - 1][ghost_x] == 'True'):
        t_y = ghost_y - 1;
    elif (ghost_m == 2) and not (grid[ghost_y][ghost_x + 1] == 'True'):
        t_x = ghost_x + 1;
    elif (ghost_m == 3) and not (grid[ghost_y + 1][ghost_x] == 'True'):
        t_y = ghost_y + 1;
    elif (ghost_m == 4) and not (grid[ghost_y][ghost_x - 1] == 'True'):
        t_x = ghost_x - 1;
    else:
        t_x, t_y = ghost_move(ghost_x, ghost_y, grid)
    
    return t_x, t_y
    
# Ghost that chases you.
def ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid):
    t_x = ghost_x;
    t_y = ghost_y;
    distances = []
    r = random.randint(1,2) # If there are two optimal moves allows it to randomly choose one

    moves = [1, 2, 3, 4]
    distance = [((((pacman_x-ghost_x)**2) + ((pacman_y-(ghost_y-1))**2))**0.5), 
                ((((pacman_x-(ghost_x+1))**2) + ((pacman_y-(ghost_y))**2))**0.5),
                ((((pacman_x-ghost_x)**2) + ((pacman_y-(ghost_y+1))**2))**0.5), 
                ((((pacman_x-(ghost_x-1))**2) + ((pacman_y-(ghost_y))**2))**0.5)]
                
    if r == 1:
        ghost_m = moves[distance.index(min(distance))]
    else:
        moves.reverse() # Flipping the moves is one way that lets the script find a different equivalent minimum
        distance.reverse()
        ghost_m = moves[distance.index(min(distance))]
        
    if (ghost_m == 1) and not (grid[ghost_y - 1][ghost_x] == 'True'):
        t_y = ghost_y - 1;
    elif (ghost_m == 2) and not (grid[ghost_y][ghost_x + 1] == 'True'):
        t_x = ghost_x + 1;
    elif (ghost_m == 3) and not (grid[ghost_y + 1][ghost_x] == 'True'):
        t_y = ghost_y + 1;
    elif (ghost_m == 4) and not (grid[ghost_y][ghost_x - 1] == 'True'):
        t_x = ghost_x - 1;
    else:
        t_x, t_y = ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid)
    
    return t_x, t_y

def game_func(move, pacman_x = 1, pacman_y = 3, ghost_x = 3, ghost_y = 3, goal_x = 3, goal_y = 1, gridsize = [7, 7], grid = []):
    t_x = ghost_x;
    t_y = ghost_y;
    pacman = [['False' for x in range(gridsize[0])] for y in range(gridsize[1])]
    ghost  = [['False' for x in range(gridsize[0])] for y in range(gridsize[1])]
    goal = [['False' for x in range(gridsize[0])] for y in range(gridsize[1])]
    pacman[pacman_y][pacman_x] = 'True';
    ghost[ghost_y][ghost_x] = 'True';
    goal[goal_y][goal_x] = 'True';
    won = 'False'
    lost = 'False'
    turn_count=-1
    ended=False
    moved = False;
    
    t_x = ghost_x;
    t_y = ghost_y;
    if (move == 1) and not (grid[pacman_y - 1][pacman_x] == 'True'):
        pacman[pacman_y][pacman_x]='False'
        pacman_y = pacman_y - 1;
        pacman[pacman_y][pacman_x]='True'
        if (pacman_x != ghost_x or pacman_y != ghost_y):
            if random_ghost:
                t_x, t_y = ghost_move(ghost_x, ghost_y, grid)
            else:
                t_x, t_y = ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid)
        moved = True;
    elif  (move == 2) and not (grid[pacman_y][pacman_x + 1] == 'True'):
        pacman[pacman_y][pacman_x]='False'
        pacman_x = pacman_x + 1;
        pacman[pacman_y][pacman_x]='True'
        if (pacman_x != ghost_x or pacman_y != ghost_y):
            if random_ghost:
                t_x, t_y = ghost_move(ghost_x, ghost_y, grid)
            else:
                t_x, t_y = ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid)
        moved = True;
    elif  (move == 3) and not (grid[pacman_y + 1][pacman_x] == 'True'):
        pacman[pacman_y][pacman_x]='False'
        pacman_y = pacman_y + 1;
        pacman[pacman_y][pacman_x]='True'
        if (pacman_x != ghost_x or pacman_y != ghost_y):
            if random_ghost:
                t_x, t_y = ghost_move(ghost_x, ghost_y, grid)
            else:
                t_x, t_y = ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid)
        moved = True;
    elif  (move == 4) and not (grid[pacman_y][pacman_x - 1] == 'True'):
        pacman[pacman_y][pacman_x]='False'
        pacman_x = pacman_x - 1;
        pacman[pacman_y][pacman_x]='True'
        if (pacman_x != ghost_x or pacman_y != ghost_y):
            if random_ghost:
                t_x, t_y = ghost_move(ghost_x, ghost_y, grid)
            else:
                t_x, t_y = ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid)
        moved = True;
    else: # ghost move even if pacman can't move
        if random_ghost:
                t_x, t_y = ghost_move(ghost_x, ghost_y, grid)
        else:
                t_x, t_y = ghost_move2(pacman_x, pacman_y, ghost_x, ghost_y, grid)
        
    if (t_x == pacman_x) and (t_y == pacman_y):
        won = 'False'
        ended = True
    elif (goal_x == pacman_x) and (goal_y == pacman_y):
        won = 'True'
        ended = True

    return pacman_x, pacman_y, t_x, t_y, goal_x, goal_y, ended, won, moved