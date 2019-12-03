#!/usr/bin/env python
# coding: utf-8

# In[19]:


'''
Q-learning algorithm
"Stochastic formulation" of Value Iteration policy. Uses a slightly different update equation, such that information
about the state transition probabilities is no longer needed. Introduces the concept of exploration vs exploitation, i.e.
how to choose the value of epsilon/alpha (the learning rate) of the agent.
'''


# In[20]:


import sys
import numpy as np
import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


# In[21]:


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


# In[25]:


'''
Define some global methods. Previously part of PacmanEnv class but extracted b/c they'll
also be used by the Q-learning algorithm function
'''
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

def return_state(states, p, g):
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


# In[26]:


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
                    next_state = return_state(states, next_pacman_loc, next_ghost_loc) 
                    reward = calculate_reward(next_pacman_loc, next_ghost_loc, ghost_grid_loc, pellet_loc) # calculate the reward at this state

                    if (pacman_grid_loc == pellet_loc or pacman_grid_loc == ghost_grid_loc):
                        done = True

                    temp.append( (0.25, next_state, reward, done) )
        
        self.P = P
        


# In[6]:


def q_learning(env=PacmanEnv(), gamma=0.5, alpha=0.1, epsilon=0.1, episodes=5):
    '''
    Q-Learning Algorithm

    Inputs:
        env: PacmanEnv as defined in class above. This will be used for simplicity of implementation, however in the case
            of Q-learning, the state transition probability matrix is assumed to be unknown.
        gamma: Discount rate for future rewards.
        alpha: Learning rate. "How much you accept the new value vs the old value," i.e. how much weight will you assign
            to the old vs new value of Q.
        epsilon: Used to control balance of exploration (choose a random action) vs exploitation, i.e. we pick a value at
            random in the range (0,1) and if this value < epsilon, we will choose a random action. Else, we pick the action
            that maximizes Q (based on current knowledge of Q).
        episodes: Number of epochs to run.

    Helper Methods:
        extract_policy: Returns the optimal policy for a given value function. It is run once at the end of the algorithm
                        after the optimal Q (value function) has been estimated.

    Outputs:
        A tuple (policy, Q, steps) of the policy extracted from the estimated Q function, the approximated optimal value 
        function, and the number of steps the algorithm took to converge.
    '''
    
    def extract_policy(Q):
        policy = np.zeros([env.num_states, env.num_actions])
        
        for s in range(env.num_states):
            best_action = np.argmax(Q[s, :]) # returns index of action that has maximum V
            policy[s, best_action] = 1 # deterministic optimal policy, i.e. always take best_action for given state
        
        return policy
    
    # initialize Q(s,a) matrix to all zeros
    Q = np.zeros([env.num_states, env.num_actions])
    converged = False
    steps = 0
    
    for t in range(episodes):
        print('Episode #', t)
        
         # select random state
        state = random.randint(0, env.num_states-1)
        
        # run inner loop for each episode until a terminal state has been reached
        while ~converged:
            print('Q learning, step ', steps, '...')
            
            # select action
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0,3) # exploration
            else:
                action = np.argmax(Q[state, :]) # exploitation
            
            ghost_mvmt = random.randint(0,3) # simulate random movement for the ghost

            # travel to the next state, taking action selected above
            pacman_grid_loc = env.states[state][0] # for the given state, where is pacman
            ghost_grid_loc = env.states[state][1] # in the given state, where is the ghost

            [x_p, y_p] = grid_to_xy(pacman_grid_loc)
            next_pacman_loc = move(x_p, y_p, action)
            [x_g, y_g] = grid_to_xy(ghost_grid_loc)
            next_ghost_loc = move(x_g, y_g, ghost_mvmt)

            next_state = return_state(env.states, next_pacman_loc, next_ghost_loc)
        
            # to get reward, need to find specific entry of P[s][a] with same next_state...
            reward = 0
            for ns in range( len(env.P[state][action]) ): # array of tuples (probability, next_state, reward, done)
                if (env.P[state][action][ns][1] == next_state):
                    reward = env.P[state][action][ns][2]

            # in next state, select action with highest Q-value
            max_next_action_value = np.max(Q[next_state, :])

            # update Q-values tables with equation
            Q[state][action] = ((1-alpha)*Q[state][action]) + (alpha*(reward + (gamma * max_next_action_value)))

            # if reached terminal state (i.e. next state = terminal state), converged = True
            if (next_pacman_loc == next_ghost_loc or next_pacman_loc == env.pellet_loc):
                converged = True
            
            # set next state as current state & repeat
            state = next_state 

            steps += 1

        # extract optimal policy after calculating optimal V
        policy = extract_policy(Q)

        return policy, Q, steps


# In[ ]:




