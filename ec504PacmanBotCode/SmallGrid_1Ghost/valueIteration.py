import game_funcs as g
from game import Game
from environment import *

from random import randint as ri
import time
import numpy as np

gamma = 0.25;

def value_iteration(env, gamma):
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
        action_values = np.zeros(4)
        for a in range(4):
            for prob, next_state, reward, done in env.P[current_state][a]:
                action_values[a] += prob * (reward + (gamma * V[next_state]))
        return action_values
    
    def extract_policy(V):
        policy = [0]*env.num_states
        
        for s in range(env.num_states):
            action_values = calculate_action_values(s, V)
            best_action = np.argmax(action_values) # returns index of action that has maximum V
            policy[s] = best_action; # deterministic optimal policy, i.e. always take best_action for given state
        
        return policy
    
    theta=1e-5
    V = np.zeros(env.num_states) # arbitrarily initialize vector V to be all zeros
    converged = False
    steps = 0
    
    # iteratively calculate optimal V
    while not converged:
        delta = 0
        for s in range(env.num_states):
            action_values = calculate_action_values(s, V)
            max_action_value = np.max(action_values)
            delta = max( delta, np.abs(max_action_value - V[s]) ) # the maximum difference between V'(s) and V(s) for all s
            V[s] = max_action_value
        
        steps += 1
        
        print('Delta: ', delta)
        converged = (delta < theta)
    
    # extract optimal policy after calculating optimal V
    policy = extract_policy(V)
    
    print('Converged at', steps);
    return policy, V, steps

if __name__ == '__main__':
    ########################### Change the following ##########################
    ghostType = 'Chase' # 'Chase' or 'Random'
    ###########################################################################
    # Init
    num_ghosts = 1;
    game = Game()
    env = PacmanEnv(num_ghosts=1, ghost_type=[ghostType], grid_len=5, pellet_x=3, pellet_y=1, grid=game.grid);
    policy, v, steps = value_iteration(env, gamma=0.5);

    # Write policy to file
    f = open("valueIter_"+ghostType+".txt", "w");
    for val in policy:
      f.write(str(val)+'\n');
    f.close();
