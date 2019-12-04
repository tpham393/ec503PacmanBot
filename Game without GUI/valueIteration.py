import sys
import numpy as np
from policyIteration import *
import game_funcs
from game import Game

def value_iteration(gamma=0.5, theta=1e-5):
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
        #action_values = np.zeros(env.num_actions)
        action_values = np.zeros(4);
       	for a in range(4):
    		# Potential next states given current state and action
            nextStates, rewards = nextMove(current_state, a);
            # Compute V(s,a)
            vNextStates = [prob*(rewards[i]+gamma*V[nextStates[i]]) for i in range(len(nextStates))];
            actionVal = sum(vNextStates);
            action_values[a] = actionVal;
            #for prob, next_state, reward, done in env.P[current_state][a]:
            #    action_values[a] += prob * (reward + (gamma * V[next_state]))
        return action_values
    
    def extract_policy(V):
        #policy = np.zeros([env.num_states, env.num_actions])
        policy = np.zeros(numStates); 
        for s in range(numStates):
            action_values = calculate_action_values(s, V)
            best_action = np.argmax(action_values); # returns index of action that has maximum V
            #policy[s, best_action] = 1 # deterministic optimal policy, i.e. always take best_action for given state
            policy[s] = best_action;
        return policy
    
    V = np.zeros(numStates) # arbitrarily initialize vector V to be all zeros
    converged = False
    steps = 0
    
    # iteratively calculate optimal V
    while ~converged:
        # print('Value iteration, step ', steps, '...')
        delta = 0
        for s in range(numStates):
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
    
    print('Completed algorithm')
    return policy, V, steps

   ############################################################################

'''
# intervals of 0.05
# note: algo runs for a long time if gamma=0 or 1
gammas = np.arange(0.05,1,0.05) # np.arange includes the lower bound, excludes upper bound
# print(gammas)

convergence_steps = []

for g in range(len(gammas)):
    policy, V, steps = value_iteration(gamma=gammas[g])
    convergence_steps.append(steps)

print(convergence_steps)

###############################################################################

import matplotlib.pyplot as plt

plt.plot(gammas, convergence_steps)
plt.xlabel('gamma')
plt.ylabel('# steps to convergence')
plt.xticks(np.arange(0,1,0.1))
plt.show()
'''
###############################################################################
############################  Game Simulation #################################
###############################################################################
policy, V, steps = value_iteration(gamma=0.25)

f = open("valueIter.txt","w")
for i in policy:
    f.write(str(i)+"\n");
f.close(); 

game = Game(col,row);

## Random spawn
'''
pacman_x, pacman_y = 2,0;
while (pacman_x==game.goal_x and pacman_y==game.goal_y):
    pacman_x = ri(0,col-1);
    pacman_y = ri(0,row-1);

ghost_x, ghost_y = 2,0;
while (ghost_x==game.goal_x and ghost_y==game.goal_y) or (ghost_x==pacman_x and ghost_y==pacman_y):
    ghost_x = ri(0,col-1);
    ghost_y = ri(0,row-1);
'''
'''
pacman_x,pacman_y = 0,0;
ghost_x, ghost_y = 0,0;
game.updateState(pacman_x, pacman_y, ghost_x, ghost_y); # update internal grid

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
    pacman_x2, pacman_y2, ghost_x2, ghost_y2, game.goal_x, game.goal_y, game.ended, game.won, game.moved = game_funcs.game_func(move, game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, game.goal_x,game.goal_y,col,row);
    game.moves.append(move);
    game.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2); # update internal grid
# Update one last time before game end
game.update(); 
'''