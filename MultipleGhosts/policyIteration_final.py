import game_funcs_multGhosts as g
from game_multGhosts import Game
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
        print("Total iterations:", policyIter)
        policyIter += 1;


    # Write policy to file
    filename = "policy_"+"grid"+str(env.grid_len)+"x"+str(env.grid_len)+"_ghosts"+str(env.num_ghosts);
    f = open(filename+"_final.txt", "w");
    for val in policy:
        f.write(str(val)+'\n');
    f.close();

    return policy, v, policyIter;
if __name__ == '__main__':
    env = PacmanEnv(num_ghosts=2);
    policy, v, policyIter = policyIteration(env);

    col, row = 3,3;
    grid_len = 3;
    num_ghosts = 1;
    game = Game(3,3);

    pacman_x,pacman_y = 0,0;
    ghost_x = [1,2];
    ghost_y = [1,2]
    game.updateState(pacman_x, pacman_y, ghost_x, ghost_y); # update internal grid

    ## Start game
    while not game.ended:
        game.update(); # update graphics
        time.sleep(0.5);
        # Get state (0 to numStates-1) from pacman and ghost coordinates
        state = env.coord2state(game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y);

        ###########################################################################
        ########################## For Thuy to Change #############################
        # Use your policy function
        # Make sure that the that your action (1 to 4) aligns with the pacman direction of movement in game_func
        # My policy[state] outputs 0 to 3, that's why I add 1, because Steven's actions go 1 to 4
        move = policy[state] + 1;
        ###########################################################################

        # Get game status given current state and move (action)
        pacman_x2, pacman_y2, ghost_x2, ghost_y2, game.goal_x, game.goal_y, game.ended, game.won = g.game_func(move, game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, game.goal_x, game.goal_y, col, row);
        game.moves.append(move);
        game.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2); # update internal grid
    # Update one last time before game end
    game.update(); 