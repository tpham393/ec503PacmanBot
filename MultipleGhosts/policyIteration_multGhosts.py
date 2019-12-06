import game_funcs_multGhosts as g
from game_multGhosts import Game
import time
from random import randint as ri
import math

# Initial game parameters
numGhosts = 2;

pelletLocX = 2;
pelletLocY = 0;

row, col = (3,3);
gridSize = row*col;
numStates = int(math.pow(gridSize,1+numGhosts));
directions = 4;

winReward = 1000;
loseReward = -1000;
gamma = 0.25;
prob = 1/math.pow(directions,numGhosts);

def state2coord(state):
    '''
    Coverts state to pacman and ghost coordinates. 
    ARGS:
        state: Game state, ranges 0 to numStates-1
    RETURN: 
        pacmanLocX (int): X location of pacman
        pacmanLocY (int): Y location of pacman 
        ghostLocX (list): X locations of all ghost 
        ghostLocY (list): Y locations of all ghost 
    '''
    # Get linearized grid index for all game objects
    pacmanLocLin = math.floor(state / math.pow(gridSize,numGhosts));
    ghostLocLin = [];
    runningMod = state%math.pow(gridSize,numGhosts);
    for i in range(numGhosts):
        ghostLocLin.append(math.floor(runningMod/math.pow(gridSize,numGhosts-i-1)));
        runningMod = runningMod%math.pow(gridSize,numGhosts-i-1);
    pacmanLocX = pacmanLocLin % col;
    pacmanLocY = math.floor(pacmanLocLin / col);
    # Convert linearized grid index into grid coordinates
    ghostLocX = [];
    ghostLocY = [];
    for i in range(numGhosts):
        ghostLocX.append(ghostLocLin[i]%col);
        ghostLocY.append(math.floor(ghostLocLin[i]/col));

    return pacmanLocX, pacmanLocY, ghostLocX, ghostLocY;

def coord2state(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY):
    '''
    Coverts pacman and ghost coordinates to state. 
    ARGS:
        pacmanLocX (int): X location of pacman
        pacmanLocY (int): Y location of pacman 
        ghostLocX (list): X locations of all ghost 
        ghostLocY (list): Y locations of all ghost 
    RETURN: 
        state: Game state, ranges 0 to numStates-1 
    '''
    # Linearize grid coordinates for all game objects
    pacmanLocLin = pacmanLocY*col + pacmanLocX;
    ghostLocLin = [];
    for i in range(numGhosts):
        ghostLocLin.append(ghostLocY[i]*col + ghostLocX[i]);
    # Calculate state
    state = pacmanLocLin * math.pow(gridSize,numGhosts);
    for i in range(numGhosts):
        state = state + ghostLocLin[i]*math.pow(gridSize,numGhosts-i-1);
    return int(state);

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
    # Check if action lies within grid bounds
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

def getReward(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY, pelletLocX, pelletLocY):
    '''
    Calculate reward given game object locations.
    '''
    reward = 0; # Default reward
    if (pacmanLocX == pelletLocX and pacmanLocY == pelletLocY): # Pacman won
        reward = winReward;
    for i in range(numGhosts):
        if (pacmanLocX==ghostLocX[i] and pacmanLocY==ghostLocY[i]): # Pacman lost
            reward = loseReward;
            break;
    return reward;

def evalGhostAction(ghostLocX, ghostLocY, actions):
    '''
    Ghosts perform actions.
    ARGS:
        ghostLocX (list): X locations of all ghosts.
        ghostLocY (list): Y locations of all ghosts.
        actions (list): Actions to be made for each ghost.
    RETURN:
        t_x (list): X locations of all ghosts' new locations
        t_y (list): Y locations of all ghosts' new locations
    '''
    t_x = ghostLocX[:];
    t_y = ghostLocY[:];
    for i in range(numGhosts): # Perform action for each ghost
        locX = t_x[i];
        locY = t_y[i];
        locX, locY = evalAction(locX, locY, actions[i]); # Ensure action within grid bounds
        # Check if new location overlaps with locations of other ghosts
        valid = True;
        for j in range(numGhosts):
            if j == i: # don't consider own position
                continue;
            if (t_x[j]==locX and t_y[j]==locY): # overlap
                valid = False;
                break;
        # if no overlap, update ghost locations
        if (valid): 
            t_x[i] = locX;
            t_y[i] = locY;

    return t_x, t_y;

def moveThrough(pacman_x, pacman_y, prevPacman_x, prevPacman_y, ghost_x, ghost_y, prevGhost_x, prevGhost_y):
    '''
    Check if ghost and pacman try to move through each other.
    ARGS:
        pacman_x (int): X location of pacman after moving.
        pacman_y (int): Y location of pacman after moving.
        prevPacman_x (int): X location of pacman prior to moving.
        prevPacman_y (int):  Y location of pacman prior to moving.
        ghost_x (list): X locations of all ghosts after moving.
        ghost_y (list): Y locations of all ghosts after moving.
        prevGhost_x (list): X locations of all ghosts prior to moving.
        prevGhost_y (List): Y locations of all ghosts prior to moving.
    RETURN:
        True - Ghost and pacman tried to move through each other
        False - otherwise
    '''
    samePos1 =[];
    samePos2 = [];
    # Cond 1: Check if previous position of pacman at ghost's new position
    for i in range(len(ghost_x)): 
        if (prevPacman_x == ghost_x[i] and prevPacman_y == ghost_y[i]):
            samePos1.append(i);
    # Cond 2: Check if previous position of ghost at pacman's new position
    for i in range(len(prevGhost_x)):
        if (pacman_x == prevGhost_x[i] and pacman_y == prevGhost_y[i]):
            samePos2.append(i);
    # If both conditions true for same ghost, return true
    for val in samePos1:
        if val in samePos2:
            return True;
    return False;

def nextMove(currState, action):
    '''
    Returns all possible next states given action, and the reward given next states.
    ARGS:
        currState: Current game state, ranges from 0 to numStates-1.
        action: Action to perform.
    RETURN:
        nextStates: List of possible next states give current state and action.
                    Largly depends on potential ghost movements.
        rewards: List of rewards for each potential next state.
    '''
    # Get currState coordinates
    pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = state2coord(currState);
    # Get pacman location after performing action
    pacmanLocX_next, pacmanLocY_next = evalAction(pacmanLocX, pacmanLocY, action);
    # Get all possible ghost states
    nextStates = [];
    rewards = [];
    for i in range(4): # Needs to be hardcoded, <numGhosts> number of loops
        for j in range(4):
            # Get ghost next location given action
            ghostLocX_next, ghostLocY_next = evalGhostAction(ghostLocX, ghostLocY, [i,j]);
            # if pacman not moving through ghost
            if (not moveThrough(pacmanLocX_next, pacmanLocY_next, pacmanLocX, pacmanLocY, ghostLocX_next, ghostLocY_next, ghostLocX, ghostLocY)):
                state = coord2state(pacmanLocX_next, pacmanLocY_next, ghostLocX_next, ghostLocY_next);
                nextStates.append(state);
                rewards.append(getReward(pacmanLocX_next, pacmanLocY_next, ghostLocX_next, ghostLocY_next, pelletLocX, pelletLocY));
            else: # if pacman moving through ghost, set pacman as new state and keep old ghost states so pacman and ghost overlaps
                state = coord2state(pacmanLocX_next, pacmanLocY_next, ghostLocX, ghostLocY);
                nextStates.append(state);
                rewards.append(loseReward);

    return nextStates, rewards;

def gameEnd(state):
    ''' 
    Check if game has ended.
    ARGS:
        state: Current game state, ranges from 0 to numStates-1.
    RETURN:
        True if game has ended.
        False if game has not ended.
    '''
    pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = state2coord(state);
    for i in range(numGhosts):
        if (pacmanLocX == ghostLocX[i] and pacmanLocY == ghostLocY[i]):
            return True;
    if (pacmanLocX == pelletLocX) and (pacmanLocY == pelletLocY):
        return True;
    return False;

########################## Policy evaluation ##################################
def policyEvaluation(policy, v):
    # Set parameters
    deltaLim = 0.00001;
    delta = 10000;

    cnt = 0;
    while (delta > deltaLim): 
        delta = 0;
        for state in range(numStates):
            if (gameEnd(state)): # game has ended
                v[state] = 0;
                continue;
            vStateOld = v[state]; 
            # Choose action from policy
            action = policy[state];
            # Potential next states given current state and action
            nextStates, rewards = nextMove(state, action); 
            # Compute V(s)
            vNextStates = [prob*(rewards[i]+gamma*v[nextStates[i]]) for i in range(len(nextStates))];
            v[state] = sum(vNextStates);
            delta = max(delta, abs(v[state]-vStateOld));
        #print("Delta",delta);
        cnt += 1;
    print("Policy evalulation converged at", cnt);
    return v;


########################## Policy Improvement #################################
def policyImprovement(policy, v):
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
        # No convergence
        if (oldAction != optAction):
            policyStable = False;
            policy[state] = optAction;
    return policy, policyStable

###############################################################################
############################  Policy Iteration ################################
###############################################################################

if __name__ == '__main__':
    # Init
    v = [0]*numStates;
    policy = [0]*numStates;
    policyStable = False;

    # Run Policy Iteration
    policyIter = 1;
    while (not policyStable):
        v = policyEvaluation(policy, v);
        policy, policyStable = policyImprovement(policy, v);
        print("Total iterations:", policyIter)
        policyIter += 1;

    # Write policy to file
    filename = "Original_policy_"+"grid"+str(col)+"x"+str(row)+"_ghosts"+str(numGhosts);
    f = open(filename+".txt", "w");
    for val in policy:
        f.write(str(val)+'\n');
    f.close();