#!/usr/bin/env python
# coding: utf-8

# In[6]:


import sys
import numpy as np

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


# In[7]:


'''
Enumerate states for a 3x3 grid ==> 81 states 
(9 choices for pacman location x 9 choices for ghost location)

y    _0_|_1_|_2_
|    _3_|_4_|_5_
v     6 | 7 | 8
    x -->

Each x,y pair represented as an integer number corresponding to the diagram above
'''

states_num = [];

for s in range(81):
    for p in range(9):
        for g in range(9):
            states_num.append( (p, g) )
                    
#for s in range(81):
#    print("state ", s, ": ", states_num[s])


# In[8]:


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

def move(x, y, action):
    if action == UP:
        y = max(0, y-1)
    elif action == RIGHT:
        x = min(2, x+1)
    elif action == DOWN:
        y = min(2, y+1)
    elif action == LEFT:
        x = max(0, x-1)
    return xy_to_grid(x, y)


# In[9]:


class PacmanEnv:
    '''
    Class to initialize and store information about the Pacman environment for program planning algorithms.

    Properties:
        P[s][a] is a list of is a list of transition tuples (prob, next_state, reward, done)
        num_states = number of states (set to default for 3x3 grid)
        num_actions = number of actions (set to 4)
        pellet_loc = location of pellet (set to 2, i.e. [2,0] by default)

    Helper Methods:
        return_state: Returns state number given location of pacman and the ghost
        move: Moves pacman given current location and action input. Returns grid location number
        calculate_reward: Returns reward for current location of pacman. Used to evaluate R(s,a,s') by 
                        first determining s' through move(s,a), then calculating the reward at s'.
        grid_to_xy: Returns corresponding (x,y) coordinate pair for valid grid location integer input
                    If number out of range, returns 'invalid entry' error message
        xy_to_grid: Returns corresponding grid location # for given (x,y) coordinate pair input
                    If number out of range, returns 'invalid entry' error message
    '''

    def __init__(self, states=states_num, num_states=81, num_actions=4, pellet_loc=2):
        self.states = states
        self.num_states = num_states
        self.num_actions = num_actions
        self.pellet_loc = pellet_loc
        
        P = {s : {a : [] for a in range(num_actions)} for s in range(num_states)}
        
        def return_state(p, g):
            return states.index( (p,g) )
        
        # parameters must be of the same type, i.e. [x,y] or int value 0-8
        # need to adjust to include reward definition for bumping into walls
        def calculate_reward(pacman_new_loc, ghost_new_loc, ghost_current_loc, pellet_location):
            if pacman_new_loc == ghost_current_loc: # pacman moved to the ghost's location
                return -1000
            elif pacman_new_loc == pellet_location:
                return 1000
            elif pacman_new_loc == ghost_new_loc: # the ghost moved to pacman's new location
                return -1000
            else:
                return 0
        
        for s in range(num_states):
            for pacman_a in range(num_actions):
                done = False # flag to signal game has ended
                temp = P[s][pacman_a]
                pacman_grid_loc = states[s][0] # for the given state, where is pacman
                ghost_grid_loc = states[s][1] # in the given state, where is the ghost
                
                # if pacman performs action a: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
                [x_p, y_p] = grid_to_xy(pacman_grid_loc)
                next_pacman_loc = move(x_p, y_p, pacman_a) # grid location he will move to
                
                for ghost_a in range(num_actions):
                    # if the ghost performs action a: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
                    [x_g, y_g] = grid_to_xy(ghost_grid_loc)
                    next_ghost_loc = move(x_g, y_g, ghost_a) # grid location he will move to
                    
                    # resulting next state, simulates pacman and the ghost moving simultaneously
                    next_state = return_state(next_pacman_loc, next_ghost_loc) 
                    reward = calculate_reward(next_pacman_loc, next_ghost_loc, ghost_grid_loc, pellet_loc) # calculate the reward at this state

                    if (pacman_grid_loc == pellet_loc or pacman_grid_loc == ghost_grid_loc):
                        done = True

                    temp.append( (0.25, next_state, reward, done) )
        
        self.P = P
        


# In[15]:


def heuristic_policy(env=PacmanEnv()):
    def calc_action_distances():
        action_distances = []

        for a in range(env.num_actions):
            [x_pellet, y_pellet] = grid_to_xy(env.pellet_loc)
            [next_x_p, next_y_p] = grid_to_xy( move(x_p, y_p, a) )
            dist_to_pellet = np.linalg.norm( np.asarray([next_x_p, next_y_p]) - np.asarray([x_pellet, y_pellet]) )
            action_distances.append(dist_to_pellet)

        return action_distances
    
    policy = np.zeros([env.num_states, env.num_actions])
    
    for s in range(env.num_states):
        pacman_grid_loc = env.states[s][0] # for the given state, where is pacman
        ghost_grid_loc = env.states[s][1] # in the given state, where is the ghost
        
        [x_p, y_p] = grid_to_xy(pacman_grid_loc)
        [x_g, y_g] = grid_to_xy(ghost_grid_loc)
            
        # check distance between pacman and ghost
        dist = np.linalg.norm( np.asarray([x_p, y_p]) - np.asarray([x_g, y_g]) )
        action_distances = calc_action_distances()
        
        # if ghost is not within euclidean distance 2 from pacman, then 
        # choose direction that brings pacman closer to pellet
        if (dist > 2):
            best_action = np.argmin(action_distances)
        
        # else, it depends on which location the ghost is in...
        # if ghost is to the right, pacman should move left
        elif(y_g == y_p):
            if (x_g > x_p):
                best_action = 3
            else:  # if ghost is to the left, pacman should move right
                best_action = 1

        # if ghost is up, pacman should move down
        elif(x_g == x_p):
            if (y_p > y_g):
                best_action = 2
            else: # if ghost is down, pacman should move up
                best_action = 0
        
        # if ghost to top-left, pacman can move down/right
        # choose direction closer to pellet
        elif( (y_p > y_g) and (x_p > x_g) ):
            best_action = np.argmin( np.array([action_distances[2], action_distances[1]]) )
            
        # if ghost to top-right, pacman can move down/left
        # choose direction closer to pellet
        elif( (y_p > y_g) and (x_p < x_g) ):
            best_action = np.argmin( np.array([action_distances[2], action_distances[3]]) )
            
        # if ghost to bottom-left, pacman can move up/right
        # choose direction closer to pellet
        elif( (y_p < y_g) and (x_p > x_g) ):
            best_action = np.argmin( np.array([action_distances[0], action_distances[1]]) )
            
        # if ghost to bottom-right, pacman can move up/left
        # choose direction closer to pellet
        elif( (y_p < y_g) and (x_p < x_g) ):
            best_action = np.argmin( np.array([action_distances[0], action_distances[3]]) )
    
        policy[s, best_action] = 1
    
    return policy




