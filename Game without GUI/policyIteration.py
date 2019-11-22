import game_funcs as g
from game import Game
import time
from random import randint as ri
import threading
import math

pelletLocX = 2;
pelletLocY = 0;

row, col = (3,3);
numStates = 81;
directions = 4;


def state2coord(state):
    '''
    Coverts state to pacman and ghost coordinates. 
    ARGS:
        state: Game state, ranges 0 to 80
    RETURN: 
        pacmanLocX: X location of pacman on 3x3 grid
        pacmanLocY: Y location of pacman on 3x3 grid
        ghostLocX: X location of ghost on 3x3 grid
        ghostLocY: Y location of ghost on 3x3 grid
    '''
    pacmanLocLin = math.floor(state / 9);
    ghostLocLin = state % 9;

    pacmanLocX = pacmanLocLin % 3;
    pacmanLocY = math.floor(pacmanLocLin / 3);

    ghostLocX = ghostLocLin % 3;
    ghostLocY = math.floor(ghostLocLin / 3);

    return pacmanLocX, pacmanLocY, ghostLocX, ghostLocY;

def coord2state(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY):
    '''
    Coverts pacman and ghost coordinates to state. 
    ARGS:
        pacmanLocX: X location of pacman on 3x3 grid
        pacmanLocY: Y location of pacman on 3x3 grid
        ghostLocX: X location of ghost on 3x3 grid
        ghostLocY: Y location of ghost on 3x3 grid
    RETURN: 
        state: Game state, ranges 0 to 80
    '''
    pacmanLocLin = pacmanLocY * 3 + pacmanLocX;
    ghostLocLin = ghostLocY * 3 + ghostLocX;
    state = pacmanLocLin * 9 + ghostLocLin;
    return state;

def evalAction(locX, locY, action):
    '''
    Perform action given current location.
    ARGS:
        locX: X location of game object.
        locY: Y location of game object.
        action: Action to be performed
            0 - down
            1 - right
            2 - up
            3 - left
    RETURN:
        locX: Updated X location
        locY: Updated Y location
    '''
    action = action + 1;
    if (action == 2): # right
        if (locX + 1 < 3):
            locX += 1;
    elif (action == 4): # left
        if (locX - 1 >= 0):
            locX -= 1;
    elif (action == 3): # up
        if (locY + 1 < 3):
            locY += 1;
    else: # down
        if (locY - 1 >= 0):
            locY -= 1;
    return locX, locY;

def nextMove(currState, action):
    '''
    Returns all possible next states given action, and the reward given next states.
    ARGS:
        currState: Current game state, ranges from 0 to 80.
        action: Action to perform.
    RETURN:
        nextStates: List of possible next states give current state and action.
                    Largly depends on potential ghost movements.
        rewards: List of rewards for each potential next state.
    '''
    nextStates = [];
    # Get currState coordinates
    pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = state2coord(currState);
    # Get pacman location after performing action
    pacmanLocX_next, pacmanLocY_next = evalAction(pacmanLocX, pacmanLocY, action);
    # Initialize rewards
    if (pacmanLocX_next == pelletLocX) and (pacmanLocY_next == pelletLocY): 
        rewards = [100]*4;
    else:
        rewards = [0]*4;

    # Iterate through possible ghost states
    for ghostAction in range(4):
        ghostLocX_next, ghostLocY_next = evalAction(ghostLocX, ghostLocY, ghostAction);
        state = coord2state(pacmanLocX_next, pacmanLocY_next, ghostLocX_next, ghostLocY_next);
        nextStates.append(state);     
        # Evaluate reward - pacman eaten by ghost
        if (pacmanLocX_next == ghostLocX_next) and (pacmanLocY_next == ghostLocY_next):
            rewards[ghostAction] = -100;

    return nextStates, rewards;

def gameEnd(state):
    ''' 
    Check if game has ended.
    ARGS:
        state: Current game state, ranges from 0 to 80.
    RETURN:
        True if game has ended.
        False if game has not ended.
    '''
    pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = state2coord(state);
    if (pacmanLocX == ghostLocX) and (pacmanLocY == ghostLocY):
        return True;
    elif (pacmanLocX == pelletLocX) and (pacmanLocY == pelletLocY):
        return True;
    return False;

###############################################################################
########################## Policy evaluation ##################################
###############################################################################

# Set parameters
gamma = 0.25;
prob = 0.25;
deltaLim = 1;
delta = 10000;
# Initial V
v = [0]*numStates;
while (delta > deltaLim): 
    delta = 0;
    for state in range(numStates):
        if (gameEnd(state)): # game has ended
            v[state] = 0;
            continue;
        vStateSum = 0;
        vStateOld = v[state]; 
        for action in range(4): 
            # Potential next states given current state and action
            nextStates, rewards = nextMove(state, action); 
            # Compute V(s)
            vNextStates = [prob*(rewards[i]+gamma*v[nextStates[i]]) for i in range(len(nextStates))];
            vStateSum += sum(vNextStates);
        v[state] = vStateSum;

        delta = max(delta, abs(v[state]-vStateOld));
    print("Delta",delta);


###############################################################################
########################## Policy Improvement #################################
###############################################################################

policy = [0]*81;
for i in range(3000):
    policyStable = True;
    for state in range(numStates):
        if (gameEnd(state)): # game ended
            continue;
        oldAction = policy[state];
        # Optimal action and V(s,a)
        optAction = 0; 
        optActionVal = None;
        for action in range(4):
            # Potential next states given current state and action
            nextStates, rewards = nextMove(state, action);
            # Compute V(s,a)
            vNextStates = [prob*(rewards[i]+gamma*v[nextStates[i]]) for i in range(len(nextStates))];
            actionVal = sum(vNextStates);
            if (optActionVal == None):
                optActionVal = actionVal;
            if (actionVal > optActionVal): # Choose action with largest V(s,a)
                optActionVal = actionVal;
                optAction = action;
        # Continue if no convergence
        if (oldAction != optAction):
            policyStable = False;
            policy[state] = optAction;
    if (policyStable == True): # Converged
        print("Policy converged at",i);
        break;

###############################################################################
############################  Game Simulation #################################
###############################################################################
game = Game();

'''
## Random spawn
pacman_x, pacman_y = 2,0;
while (pacman_x==game.goal_x and pacman_y==game.goal_y):
    pacman_x = ri(0,2);
    pacman_y = ri(0,2);

ghost_x, ghost_y = 2,0;
while (ghost_x==game.goal_x and ghost_y==game.goal_y) or (ghost_x==pacman_x and ghost_y==pacman_y):
    ghost_x = ri(0,2);
    ghost_y = ri(0,2);

game.updateState(pacman_x, pacman_y, ghost_x, ghost_y); # update internal grid
'''

## Start game
while not game.ended:
    game.update(); # update graphics
    time.sleep(1)
    # Get state (0 to 80) from pacman and ghost coordinates
    state = coord2state(game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y);

    ###########################################################################
    ########################## For Thuy to Change #############################
    # Use your policy function
    # Make sure that the that your action (1 to 4) aligns with the pacman direction of movement in game_func
    # My policy[state] outputs 0 to 3, that's why I add 1, because Steven's actions go 1 to 4
    move = policy[state] + 1;
    ###########################################################################

    # Get game status given current state and move (action)
    pacman_x2, pacman_y2, ghost_x2, ghost_y2, game.goal_x, game.goal_y, game.ended, game.won, game.moved = g.game_func(move, game.pacman_x, game.pacman_y, game.ghost_x, game.ghost_y, game.goal_x,game.goal_y);
    if game.moved: # if moved, update grid
        game.moves.append(move);
        game.updateState(pacman_x2, pacman_y2, ghost_x2, ghost_y2); # update internal grid
# Update one last time before game end
game.update(); 
