import game_funcs as g
from game import Game
from environment import *

import sys
import numpy as np
import math

UP = 2
DOWN = 0
RIGHT = 1
LEFT = 3

def heuristic_policy(env):
    def stateValid(state):
        # check whether state valid within grid bounds
        pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = env.state2coord(state);

        if (env.grid[pacmanLocY][pacmanLocX] == True):
            return False;
        for i in range(env.num_ghosts):
            if (env.grid[ghostLocY[i]][ghostLocX[i]] == True):
                return False;
        #if pacmanLocX==env.pellet_x and pacmanLocY==env.pellet_y:
            #return False;
        return True;

    def calc_action_distances():
        action_distances = []

        for a in range(4):
            [next_x_p, next_y_p] = env.move(x_p, y_p, a)
            dist_to_pellet = np.linalg.norm( np.asarray([next_x_p, next_y_p]) - np.asarray([env.pellet_x, env.pellet_y]) )
            action_distances.append(dist_to_pellet)

        return action_distances
    
    def test_best_action(currState, action, action_distances):
        nextState, _, _ = env.nextMoveOne(currState, action)
        action_to_pellet = np.argmin(action_distances)
        moveValid = stateValid(nextState)
        # if pacman can't actually move in this direction
        while (not moveValid):
            if (action_to_pellet != action):
                return action_to_pellet
            else:
                del action_distances[action]
                return np.argmin(action_distances)
        return action
    
    policy = [0]*env.num_states
    
    for s in range(env.num_states):
        x_p,y_p,x_g,y_g = env.state2coord(s);
            
        # check distance between pacman and ghost, assuming 1 ghost
        dist = np.linalg.norm( np.asarray([x_p, y_p]) - np.asarray([x_g[0], y_g[0]]) )
        action_distances = calc_action_distances()
        
        # if ghost is not within euclidean distance 2 from pacman, then 
        # choose direction that brings pacman closer to pellet
        if (dist > 2):
            best_action = np.argmin(action_distances)
        
        # else, it depends on which location the ghost is in...
        # if ghost is to the right, pacman should move left
        elif(y_g[0] == y_p):
            if (x_g[0] > x_p):
                best_action = test_best_action(s, LEFT, action_distances)
            else:  # if ghost is to the left, pacman should move right
                best_action = test_best_action(s, RIGHT, action_distances)

        # if ghost is up, pacman should move down
        elif(x_g[0] == x_p):
            if (y_p < y_g[0]):
                best_action = test_best_action(s, DOWN, action_distances)
            else: # if ghost is down, pacman should move up
                best_action = test_best_action(s, UP, action_distances)
        
        # if ghost to top-left, pacman can move down/right
        # choose direction closer to pellet
        elif( (y_p < y_g[0]) and (x_p > x_g[0]) ):
            action = np.argmin( np.array([action_distances[DOWN], action_distances[RIGHT]]) )
            best_action = test_best_action(s, action, action_distances)
            
        # if ghost to top-right, pacman can move down/left
        # choose direction closer to pellet
        elif( (y_p < y_g[0]) and (x_p < x_g[0]) ):
            action = np.argmin( np.array([action_distances[DOWN], action_distances[LEFT]]) )
            best_action = test_best_action(s, action, action_distances)
            
        # if ghost to bottom-left, pacman can move up/right
        # choose direction closer to pellet
        elif( (y_p > y_g[0]) and (x_p > x_g[0]) ):
            action = np.argmin( np.array([action_distances[UP], action_distances[RIGHT]]) )
            best_action = test_best_action(s, action, action_distances)
            
        # if ghost to bottom-right, pacman can move up/left
        # choose direction closer to pellet
        elif( (y_p > y_g[0]) and (x_p < x_g[0]) ):
            action = np.argmin( np.array([action_distances[UP], action_distances[LEFT]]) )
            best_action = test_best_action(s, action, action_distances)
    
        policy[s] = best_action
    
    return policy

if __name__ == '__main__':
    ######################### Change this #####################################
    ghostType = 'Random';
    ###########################################################################
    # Init
    game = Game();
    env = PacmanEnv(num_ghosts=1, ghost_type=[ghostType], grid_len=5, pellet_x=3, pellet_y=1, grid=game.grid, createP=False);
    policy = heuristic_policy(env)

    # Write policy to file
    f = open("heuristic_Random.txt", "w");
    for val in policy:
      f.write(str(val)+'\n');
    f.close();




