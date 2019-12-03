#!/usr/bin/env python
# coding: utf-8

# In[12]:


'''
Value Iteration Algorithm v.2

Differences include:
    modifications to simulate that pacman and the ghost both move simultaneously in the game:
        - adjusted the calculate_reward function
        - adjusted the transition probability matrix (also calculates the ghost's next move now)
'''


# In[17]:


import sys
import numpy as np

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


# In[18]:


'''
Enumerate states for a 3x3 grid ==> 81 states 
(9 choices for pacman location x 9 choices for ghost location)

^    _0_|_1_|_2_
|    _3_|_4_|_5_
y     6 | 7 | 8
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


# In[19]:


class PacmanEnv:
    '''
    Class to initialize and store information about the Pacman environment for program planning algorithms.

    Properties:
        P[s][a] is a list of is a list of transition tuples (prob, next_state, reward, done)
        num_states = number of states (set to default for 3x3 grid)
        num_actions = number of actions (set to 4)
        pellet_loc = location of pellet (set to 2, i.e. [2,0] by default)

    Methods:
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
        
        def return_state(p, g):
            return states.index( (p,g) )
        
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
        


# In[20]:


def value_iteration(env=PacmanEnv(), gamma=0.5, theta=1e-5):
    '''
    Value Iteration Algorithm

    Inputs:
        env: PacmanEnv as defined in class above.
        gamma: Discount rate for future rewards.
        theta: Stopping criterion value. When change in Value function is less than theta for every state, stop.

    Helper Methods:
        calculate_action_values: Calculates the values for all actions for a given state.
                                Returns a vector action_values of length num_actions, where 
                                action_values[a] = expected value of action a.
                                The expected value is calculated according to the Bellman equation:
                                V(s) = P(s'|s,a) * ( R(s,a) + (gamma * V(s')) )
        extract_policy: Returns the optimal policy for a given value function. It is run once at the end of the algorithm
                        after the optimal V (value function) has been calculated.

    Outputs:
        A tuple (policy, V, steps) of the optimal policy, the approximated optimal value function, and the number of steps
        the algorithm took to converge.
    '''
    
    def calculate_action_values(current_state, V):
        action_values = np.zeros(env.num_actions)
        for a in range(env.num_actions):
            for prob, next_state, reward, done in env.P[current_state][a]:
                action_values[a] += prob * (reward + (gamma * V[next_state]))
        return action_values
    
    def extract_policy(V):
        policy = np.zeros([env.num_states, env.num_actions])
        
        for s in range(env.num_states):
            action_values = calculate_action_values(s, V)
            best_action = np.argmax(action_values) # returns index of action that has maximum V
            policy[s, best_action] = 1 # deterministic optimal policy, i.e. always take best_action for given state
        
        return policy
    
    V = np.zeros(env.num_states) # arbitrarily initialize vector V to be all zeros
    converged = False
    steps = 0
    
    # iteratively calculate optimal V
    while not converged:
        print('Value iteration, step ', steps, '...')
        delta = 0
        for s in range(env.num_states):
            action_values = calculate_action_values(s, V)
            max_action_value = np.max(action_values)
            delta = max( delta, np.abs(max_action_value - V[s]) ) # the maximum difference between V'(s) and V(s) for all s
            V[s] = max_action_value        
        
        steps += 1
        
        #print('Delta: ', delta)
        converged = (delta < theta)
        #print(converged)
    
    # extract optimal policy after calculating optimal V
    policy = extract_policy(V)
    
    return policy, V, steps





