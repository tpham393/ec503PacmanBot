import math
from game_funcs import ghost_move

UP = 2
DOWN = 0
RIGHT = 1
LEFT = 3

class PacmanEnv:
    '''
    Class to initialize and store information about the Pacman environment for program planning algorithms.

    Properties:
        P[s][a] is a list of is a list of transition tuples (prob, next_state, reward, done)
        grid_len = length of side of square grid (set to 3 for 3x3 grid)
        num_ghosts = number of ghosts (set to 1)
        winReward = reward for winning game (set to 1000)
        loseReward = reward for losing game (set to -1000)
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

    def state2coord(self, state):
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
        pacmanLocLin = math.floor(state / math.pow(self.grid_size,self.num_ghosts));
        ghostLocLin = [];
        runningMod = state%math.pow(self.grid_size, self.num_ghosts);
        for i in range(self.num_ghosts):
            ghostLocLin.append(math.floor(runningMod/math.pow(self.grid_size,self.num_ghosts-i-1)));
            runningMod = runningMod%math.pow(self.grid_size, self.num_ghosts-i-1);
        pacmanLocX = pacmanLocLin % self.grid_len;
        pacmanLocY = math.floor(pacmanLocLin / self.grid_len);
        # Convert linearized grid index into grid coordinates
        ghostLocX = [];
        ghostLocY = [];
        for i in range(self.num_ghosts):
            ghostLocX.append(ghostLocLin[i]%self.grid_len);
            ghostLocY.append(math.floor(ghostLocLin[i]/self.grid_len));

        return pacmanLocX, pacmanLocY, ghostLocX, ghostLocY;

    def coord2state(self, pacmanLocX, pacmanLocY, ghostLocX, ghostLocY):
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
        pacmanLocLin = pacmanLocY*self.grid_len + pacmanLocX;
        ghostLocLin = [];
        for i in range(self.num_ghosts):
            ghostLocLin.append(ghostLocY[i]*self.grid_len + ghostLocX[i]);
        # Calculate state
        state = pacmanLocLin * math.pow(self.grid_size,self.num_ghosts);
        for i in range(self.num_ghosts):
            state = state + ghostLocLin[i]*math.pow(self.grid_size,self.num_ghosts-i-1);
        return int(state);

    def move(self, x, y, action):
        if action == UP:
            if y+1<self.grid_len and self.grid[y+1][x] == False:
                y = y+1;
        elif action == RIGHT:
            if x+1<self.grid_len and self.grid[y][x+1] == False:
                x = x+1;
        elif action ==  DOWN:
            if y-1>=0 and self.grid[y-1][x] == False:
                y = y-1;
        elif action==LEFT:
            if x-1>=0 and self.grid[y][x-1] == False:
                x = x-1;
        '''
        if action == UP:
            y = min(self.grid_len-1, y+1)
        elif action == RIGHT:
            x = min(self.grid_len-1, x+1);
        elif action == DOWN:
            y = max(0, y-1);
        elif action == LEFT:
            x = max(0, x-1);
        '''
        return x, y

    def calculate_reward(self, pacmanLocX, pacmanLocY, ghostLocX, ghostLocY):
        '''
        Return reward and whether game done
        '''
        done = False;
        # Check if eaten by ghost BEFORE if eaten pellet, since if pacman and ghost and pellet overlap, count as loss
        for i in range(self.num_ghosts): # check each ghost if game lost
            if [pacmanLocX,pacmanLocY] == [ghostLocX[i],ghostLocY[i]]:
                done = True;
                return self.loseReward, done;
        if [pacmanLocX,pacmanLocY] == [self.pellet_x,self.pellet_y]: # game won
            done = True;
            return self.winReward, done
        return 0, done # default reward
    
    def moveThrough(self, pacman_x, pacman_y, prevPacman_x, prevPacman_y, ghost_x, ghost_y, prevGhost_x, prevGhost_y):
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

    def evalGhostAction(self, ghostLocX, ghostLocY, actions):
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
        for i in range(self.num_ghosts): # Perform action for each ghost
            locX = t_x[i];
            locY = t_y[i];
            locX, locY = self.move(locX, locY, actions[i]); # Ensure action within grid bounds
            # Check if new location overlaps with locations of other ghosts
            valid = True;
            for j in range(self.num_ghosts):
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

    def nextMove(self, currState, action):
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
        nextStates = []; # possible next states
        rewards = []; # rewards for each next state
        done = []; # whether game is done for each next state
        probs = []; # transition probs for each next state
        defaultProb = 1/math.pow(4,self.num_ghosts);

        # Get currState coordinates
        pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = self.state2coord(currState);

        # Check whether current w/in bounds
        if (self.grid[pacmanLocY][pacmanLocX] == True):
            return probs, nextStates, rewards, done;
        # Get pacman location after performing action
        pacmanLocX_next, pacmanLocY_next = self.move(pacmanLocX, pacmanLocY, action);

        ## Get all possible ghost states
        # Check whether current state is in done state: eaten by ghost or eaten pellet
        _, currStateDone = self.calculate_reward(pacmanLocX,pacmanLocY,ghostLocX,ghostLocY);
        if (currStateDone):
            return probs, nextStates, rewards, done;

        # Get next location from chasing ghost
        t_x, t_y = ghost_move(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY, self.num_ghosts, self.grid, ['Chase','Random']);
        chaseLocX, chaseLocY = t_x[0], t_y[0];
        if (chaseLocX > ghostLocX[0]):
            chaseGhostAction = RIGHT;
        elif (chaseLocX < ghostLocX[0]):
            chaseGhostAction = LEFT;
        elif (chaseLocY > ghostLocY[0]):
            chaseGhostAction = UP;
        else:
            chaseGhostAction = DOWN;

        for i in range(4): # need to be hardcoded, <numGhosts> number of loops
            # Get ghost next location given action
            ghostLocX_next, ghostLocY_next = self.evalGhostAction(ghostLocX, ghostLocY, [chaseGhostAction, i]);
            # if pacman not moving through ghost
            if (not self.moveThrough(pacmanLocX_next, pacmanLocY_next, pacmanLocX, pacmanLocY, ghostLocX_next, ghostLocY_next, ghostLocX, ghostLocY)):
                state = self.coord2state(pacmanLocX_next, pacmanLocY_next, ghostLocX_next, ghostLocY_next);
                nextStates.append(state);
                reward, doneStatus = self.calculate_reward(pacmanLocX_next, pacmanLocY_next, ghostLocX_next, ghostLocY_next);
                rewards.append(reward);
                done.append(doneStatus);
            else: # if pacman moving through ghost, set pacman as new state and keep old ghost states so pacman and ghost overlaps and game ends
                state = self.coord2state(pacmanLocX_next, pacmanLocY_next, ghostLocX, ghostLocY);
                nextStates.append(state);
                rewards.append(self.loseReward);
                done.append(True);
            probs.append(defaultProb);

        return probs, nextStates, rewards, done;

    def __init__(self, grid_len=3, num_ghosts=1, pellet_x=2, pellet_y=0, winReward=1000, loseReward=-1000, grid=[]):
        self.num_ghosts = num_ghosts
        self.grid_len = grid_len;
        self.grid_size = grid_len*grid_len;
        self.num_states = int(math.pow(self.grid_size, 1+self.num_ghosts))
        self.pellet_x, self.pellet_y = pellet_x, pellet_y;
        self.winReward = winReward;
        self.loseReward = loseReward;
        self.grid = grid;

        self.P = {s : {a : [] for a in range(4)} for s in range(self.num_states)}
            
        # Calculate P[s][a]
        for s in range(self.num_states):
            for a in range(4):
                pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = self.state2coord(s);
                probs, nextStates, rewards, done = self.nextMove(s, a);
                self.P[s][a] = [[probs[i], nextStates[i], rewards[i], done[i]] for i in range(len(nextStates))];

        
