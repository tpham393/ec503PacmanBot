'''
Q-learning algorithm
"Stochastic formulation" of Value Iteration policy. Uses a slightly different update equation, such that information
about the state transition probabilities is no longer needed. Introduces the concept of exploration vs exploitation, i.e.
how to choose the value of epsilon/alpha (the learning rate) of the agent.
'''

import game_funcs as g
from game import Game
from environment import *
import numpy 

import random
import time
import numpy as np
        
def q_learning(env, gamma=0.9, alpha=0.9, epsilon=0.25, episodes=5):
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
    

    def stateValid(state, env):
        # check whether state valid within grid bounds
        pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = env.state2coord(state);

        if (env.grid[pacmanLocY][pacmanLocX] == True):
            return False;
        for i in range(env.num_ghosts):
            if (env.grid[ghostLocY[i]][ghostLocX[i]] == True):
                return False;
        if pacmanLocX==env.pellet_x and pacmanLocY==env.pellet_y:
            return False;
        return True;

    def extract_policy(Q):
        policy = [0]*env.num_states
        
        for s in range(env.num_states):
            best_action = np.argmax(Q[s, :])
            policy[s] = best_action; # deterministic optimal policy, i.e. always take best_action for given state
        
        return policy
    
    # initialize Q(s,a) matrix to all zeros
    Q = np.zeros([env.num_states, 4])
    steps = 0
    
    metStates = [];
    initAlpha = 1
    minAlpha = 0.005;
    for t in range(episodes):
        converged = False        
      
        # Keep same start state as in game simulation
        # select random state
        state = random.randint(0, env.num_states-1);
        while (not stateValid(state,env)):
            state = random.randint(0, env.num_states-1)

        convSteps = 0;
        # run inner loop for each episode until a terminal state has been reached
        alpha = max(minAlpha, initAlpha * (0.85 ** (t//100)))
        #if t == 0:
        #    epsilon = 1;
        #else:
        #    epsilon = 1/t;
        while not converged:
            metStates.append(state);

            #if (t>8000):
            #    game.update(); # update graphics
            #    time.sleep(2.6);

            #print('Q learning, step ', steps, '...')
            
            # select action
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0,3) # exploration
            else:
                action = np.argmax(Q[state, :]) # exploitation
                #print('exploit action: ', action)

            next_state, reward, done = env.nextMoveOne(state, action);   
            # in next state, select action with highest Q-value
            max_next_action_value = np.max(Q[next_state, :])
            Q[state][action] = (1-alpha)*Q[state][action] + (alpha*(reward + (gamma * max_next_action_value)));
            # set next state as current state & repeat
            state = next_state 
            steps += 1
            convSteps += 1;
            # if reached terminal state (i.e. next state = terminal state), converged = True
            #converged = env.P[next_state][action][0][3]
            converged = done;
            #if t > 5000:
            #    pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = env.state2coord(next_state);
            #    game.updateState(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY, 1, env.ghost_type)
        #if t>8000:
        #    print("converged", reward)
        #print("Episode",t,"converged at", convSteps);
    # extract optimal policy after calculating optimal V

    x = numpy.array(metStates);
    print("Met states:",len(np.unique(x)));
    policy = extract_policy(Q)
    return policy, Q, steps




if __name__ == '__main__':
    # Init
    eps = 100000;
    game = Game();
    env = PacmanEnv(num_ghosts=2, ghost_type=['Chase','Random'], grid_len=7, pellet_x=1, pellet_y=5, grid=game.grid, createP=False);
    policy, Q, steps = q_learning(env, gamma=0.9, alpha=0.9, epsilon=0.25, episodes=eps)


    ###########################3
    pacman_x,pacman_y = 5,1;
    ghost_x = [2, 3];
    ghost_y = [5, 1];
    state = env.coord2state(pacman_x, pacman_y, ghost_x, ghost_y);

    # Write policy to file
    f = open("qLearning_eps"+str(eps)+".txt", "w");
    for val in policy:
      f.write(str(val)+'\n');
    f.close();