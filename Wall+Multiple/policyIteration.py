import game_funcs as g
from game import Game
from environment import *

from random import randint as ri
import time
import numpy as np


# Initial game parameters
gamma = 0.25;
'''
numGhosts = 2;

pelletLocX = 2;
pelletLocY = 0;

row, col = (4,4);
gridSize = row*col;
numStates = int(math.pow(gridSize,1+numGhosts));
directions = 4;

winReward = 1000;
loseReward = -1000;
gamma = 0.25;
prob = 1/math.pow(directions,numGhosts);
'''

########################## Policy evaluation ##################################
def policyEvaluation(policy, v, env):
    # Set parameters
    deltaLim = 0.00001;
    delta = 10000;

    cnt = 0;
    while (delta > deltaLim): 
        delta = 0;
        for state in range(env.num_states):
            vStateOld = v[state]; 
            # Choose action from policy
            action = policy[state];
            # Potential next states given current state and action
            action_val = 0;
            for prob, nextState, reward, done in env.P[state][action]:
                action_val += prob * (reward + gamma*v[nextState]);
            v[state] = action_val;
            delta = max(delta, abs(v[state]-vStateOld));
        #print("Delta",delta);
        cnt += 1;
    print("Policy evalulation converged at", cnt);
    return v;


########################## Policy Improvement #################################
def policyImprovement(policy, v, env):
    policyStable = True;
    for state in range(env.num_states):
        old_action = policy[state];
        action_values = np.zeros(4);
        for action in range(4):
            for prob, next_state, reward, done in env.P[state][action]:
                action_values[action] += prob * (reward + gamma*v[next_state]);
        best_action = np.argmax(action_values);
        # Check convergence
        if old_action != best_action:
            policyStable = False;
            policy[state] = best_action;
    return policy, policyStable;

def policyIteration(env):
    v = [0]*env.num_states;
    policy = [0]*env.num_states;
    policyStable = False;

    # Run Policy Iteration
    policyIter = 1;
    while (not policyStable):
        v = policyEvaluation(policy, v, env);
        policy, policyStable = policyImprovement(policy, v, env);
        policyIter += 1;
    print("Total iterations:", policyIter)


    # Write policy to file
    filename = "policy_"+"grid"+str(env.grid_len)+"x"+str(env.grid_len)+"_ghosts"+str(env.num_ghosts);
    f = open(filename+"_final.txt", "w");
    for val in policy:
        f.write(str(val)+'\n');
    f.close();

    return policy, v, policyIter;

if __name__ == '__main__':
    # Init
    col, row =7,7;
    num_ghosts = 2;
    game = Game();
    env = PacmanEnv(num_ghosts=num_ghosts, ghost_type=['chase','random'], grid_len=7, pellet_x=1, pellet_y=5, grid=game.grid);
    policy, v, policyIter = policyIteration(env);


    # Write policy to file
    f = open("policyIter.txt", "w");
    for val in policy:
      f.write(str(val)+'\n');
    f.close();


   