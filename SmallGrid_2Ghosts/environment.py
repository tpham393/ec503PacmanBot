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
        ghost_type = type of ghosts (random or chase)
        pellet_x = x location of pellet
        pellet_y = y location of pellet
        grid = game grid, indicating where walls are placed
        winReward = reward for winning game (set to 1000)
        loseReward = reward for losing game (set to -1000)
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
        ''' 
        Attempt to make some action from location (x,y).
        ARGS:
            x (int) = starting x location
            y (int) = starting y location
            action (int) = action to take, from 0 to 3
        RETURN:
            x (int) = resulting x location
            y (int) = resulting y location
        '''
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
        return x, y

    def calculate_reward(self, pacmanLocX, pacmanLocY, ghostLocX, ghostLocY):
        '''
        Return reward and whether current state is an end state (game done).

        ARGS:
            pacmanLocX (int): X location of pacman
            pacmanLocY (int): Y location of pacman 
            ghostLocX (list): X locations of all ghost 
            ghostLocY (list): Y locations of all ghost 
        RETURN:
            reward: either self.winReward, self.loseReward, or 0 depending on whether
                    pacman has eaten the pellet, pacman was eaten by the ghost, or else
            done: whether the current state indicates the game has ended, 
                  True - game ended, False - game not ended
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

    def nextMoveChaseRandom(self, currState, action):
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

        # Check whether current state w/in bounds
        if (self.grid[pacmanLocY][pacmanLocX] == True):
            return probs, nextStates, rewards, done;
        # Check whether current state is in done state: eaten by ghost or eaten pellet
        _, currStateDone = self.calculate_reward(pacmanLocX,pacmanLocY,ghostLocX,ghostLocY);
        if (currStateDone):
            return probs, nextStates, rewards, done;
        # Get pacman location after performing action
        pacmanLocX_next, pacmanLocY_next = self.move(pacmanLocX, pacmanLocY, action);

        ## Get all possible ghost states
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

    def nextMoveRandomRandom(self, currState, action):
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

        # Check whether current state w/in bounds
        if (self.grid[pacmanLocY][pacmanLocX] == True):
            return probs, nextStates, rewards, done;
        # Check whether current state is in done state: eaten by ghost or eaten pellet
        _, currStateDone = self.calculate_reward(pacmanLocX,pacmanLocY,ghostLocX,ghostLocY);
        if (currStateDone):
            return probs, nextStates, rewards, done;
        # Get pacman location after performing action
        pacmanLocX_next, pacmanLocY_next = self.move(pacmanLocX, pacmanLocY, action);

        ## Get all possible ghost states
        for i in range(4): # need to be hardcoded, <numGhosts> number of loops
            for j in range(4):
                # Get ghost next location given action
                ghostLocX_next, ghostLocY_next = self.evalGhostAction(ghostLocX, ghostLocY, [i,j]);
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

    def nextMoveOne(self, state, pacmanAction):
        ''' 
        For Q-Learning use. Don't loop through all possible next states,
        just calculate one next state.

        ARGS:
            state: current Game state, numbering from 0 to num_states-1
            pacmanAction: action for pacman to take, numbering from 0 to 3 for the four directions
        RETURN:
            nextState: next state returned by environment after taking the action
            reward: reward at next state
            done: whether next state is an end state

        '''
        pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = self.state2coord(state);
        # Move pacman
        pacmanLocX_next, pacmanLocY_next = self.move(pacmanLocX, pacmanLocY, pacmanAction);
        # Get next action for chasing ghost
        t_x, t_y = ghost_move(pacmanLocX, pacmanLocY, ghostLocX, ghostLocY, self.num_ghosts, self.grid, self.ghost_type);
        if (not self.moveThrough(pacmanLocX_next, pacmanLocY_next, pacmanLocX, pacmanLocY, t_x, t_y, ghostLocX, ghostLocY)):
            nextState = self.coord2state(pacmanLocX_next, pacmanLocY_next, t_x, t_y);
            reward, done = self.calculate_reward(pacmanLocX_next, pacmanLocY_next, t_x, t_y);
        else:
            nextState = self.coord2state(pacmanLocX_next, pacmanLocY_next, ghostLocX, ghostLocY);
            reward = self.loseReward;
            done = True;
        return nextState, reward, done;

    def __init__(self, grid_len=3, num_ghosts=1, ghost_type = ['Random','Random'], pellet_x=2, pellet_y=0, winReward=1000, loseReward=-1000, grid=[], createP = True):
        '''
        ARGS:
            grid_len (int): length of grid side (not including walls)
            num_ghosts (int): number of ghosts to introduce to the environment
            ghost_type (list): ghost_type corresponding to each ghost, can be 'Random' or 'Chase'
            pellet_x (int): x location of pellet
            pellet_y (int): y location of pellet
            winReward (int): reward for winning the game
            loseReward (int) reward for losing the game
            grid (2D list): game grid of booleans, with True indicating tile occupied by a wall, 
                            and False indicating tile that Pacman and ghosts can move into
            createP (boolean): Whether to create the list of transition tuples

        '''
        self.num_ghosts = num_ghosts
        self.grid_len = grid_len;
        self.grid_size = grid_len*grid_len;
        self.num_states = int(math.pow(self.grid_size, 1+self.num_ghosts))
        self.pellet_x, self.pellet_y = pellet_x, pellet_y;
        self.winReward = winReward;
        self.loseReward = loseReward;
        self.grid = grid;
        self.ghost_type = ghost_type;

        if createP:
            self.P = {s : {a : [] for a in range(4)} for s in range(self.num_states)}
                
            # Calculate P[s][a]
            for s in range(self.num_states):
                for a in range(4):
                    pacmanLocX,pacmanLocY,ghostLocX,ghostLocY = self.state2coord(s);
                    if 'Chase' in ghost_type:
                        probs, nextStates, rewards, done = self.nextMoveChaseRandom(s, a);
                    else:
                        probs, nextStates, rewards, done = self.nextMoveRandomRandom(s, a);
                    self.P[s][a] = [[probs[i], nextStates[i], rewards[i], done[i]] for i in range(len(nextStates))];
 