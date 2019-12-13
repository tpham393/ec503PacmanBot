import game_funcs as g
from game import Game
from environment import *

from random import randint as ri
import time
import numpy as np


# Set discount factor
gamma = 0.25;

########################## Policy evaluation ##################################
def policyEvaluation(policy, v, env):
    '''
    Update V based on following given policy.
    ARGS:
        policy = policy to follow
        v = V to update
        env = Pacman environment containing state information.
    RETURN:
        v = updated V
    '''
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
    print("Policy evaluation converged at", cnt);
    return v;


########################## Policy Improvement #################################
def policyImprovement(policy, v, env):
    '''
    Improve the policy based off v.
    ARGS:
        policy = policy to update
        v = v to use for updating the policy
        env = Pacman environment containing state information.
    RETURN:
        policy = updated policy
        policyStable = whether policy has converged
    '''
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
    '''
    Run policy evaluation and policy improvement.
    ARGS:
        env = Pacman environment containing state information
    RETURN:
        policy = converged policy
        v = final V that lead to the policy to converge
        policyIter = number of iterations taken for policy to converge
    '''
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
    ########################### Change the following ##########################
    ghostType = ['Random','Random'] # 'Chase' or 'Random'
    ###########################################################################

    # Init
    game = Game();
    env = PacmanEnv(num_ghosts=2, ghost_type=ghostType, grid_len=5, pellet_x=3, pellet_y=1, grid=game.grid);
    policy, v, policyIter = policyIteration(env);

    # Write policy to file
    if 'Chase' in ghostType:
        f = open("policyIter_ChaseRandom.txt", "w");
    else:
        f = open("policyIter_RandomX2.txt", "w");
    for val in policy:
      f.write(str(val)+'\n');
    f.close();


   