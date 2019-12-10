# Functions:
# ghost_move is the function that chooses the next space for the ghost to move
# game_func is the function that the user controls the game with

# Inputs:
# move: the next move for the user
# pacman_x, pacman_y: the current x and y position of pacman
# ghost_x, ghost_y: the current x and y position of the ghost
# goal_x, goal_y: the x and y location of the goal
# (The above variables must be within the gridsize which is set in this function and can be changed)

# Outputs:
# pacman_x, pacman_y: the current x and y position of pacman
# t_x, t_y: the current x and y position of the ghost
# goal_x, goal_y: the x and y location of the goal
# ended: whether the game has ended or not
# won: whether or not you reached the goal
# moved: whether you made a valid move or not

import math
import random
import time

def validGhostMove(x, y, ghost_x, ghost_y, grid):
	'''
	Given new ghost location and locations of the other ghosts, see if new location is valid.
	'''
	if x>=len(grid) or x<0 or y>=len(grid) or y<0:
		return False;
	# Check if ghost move is into a wall or not
	if (grid[y][x] == True): 
		return False;
	# Check if new ghost position overlaps with other ghost positions
	for i in range(len(ghost_x)):
		if (x==ghost_x[i]) and (y==ghost_y[i]):
			return False;
	return True;

# Random Moving Ghost.
def ghost_move(pacman_x, pacman_y, ghost_x, ghost_y, numGhosts, grid, ghost_type): 
	''' 
	Randomly move each ghost.
	'''
	t_x = ghost_x[:];
	t_y = ghost_y[:];

	for i in range(numGhosts): # Get random move for each ghost
		# Modified ghost_x and ghost_y for preventing overlap between ghost positions
		modGhost_x = t_x[:];
		del modGhost_x[i];
		modGhost_y = t_y[:];
		del modGhost_y[i];

		# Record valid ghost moves
		distance = [];
		potentialMoves = []; 
		if validGhostMove(t_x[i], t_y[i]-1, modGhost_x, modGhost_y, grid):
			distance.append(((((pacman_x-ghost_x[i])**2) + ((pacman_y-(ghost_y[i]-1))**2))**0.5));
			potentialMoves.append(1);
		if validGhostMove(t_x[i]+1, t_y[i], modGhost_x, modGhost_y, grid):
			distance.append(((((pacman_x-(ghost_x[i]+1))**2) + ((pacman_y-(ghost_y[i]))**2))**0.5));
			potentialMoves.append(2);
		if  validGhostMove(t_x[i], t_y[i]+1, modGhost_x, modGhost_y, grid):
			distance.append(((((pacman_x-ghost_x[i])**2) + ((pacman_y-(ghost_y[i]+1))**2))**0.5));
			potentialMoves.append(3);
		if validGhostMove(t_x[i]-1, t_y[i], modGhost_x, modGhost_y, grid):
			distance.append(((((pacman_x-(ghost_x[i]-1))**2) + ((pacman_y-(ghost_y[i]))**2))**0.5));
			potentialMoves.append(4);

		# Randomly choose a valid move
		if potentialMoves: 
			if (ghost_type[i] == 'Random'):
				ghost_idx = random.randint(0,len(potentialMoves)-1);
				ghost_m = potentialMoves[ghost_idx]; # Random move
				# Update ghost location
				if (ghost_m == 1):
					t_y[i] = ghost_y[i] - 1;
				elif (ghost_m == 2):
					t_x[i] = ghost_x[i] + 1;
				elif (ghost_m == 3):
					t_y[i] = ghost_y[i] + 1;
				else:
					t_x[i] = ghost_x[i] - 1;
			elif (ghost_type[i] == 'Chase'):
				r = 1;
				#r = random.randint(1,2) # If there are two optimal moves allows it to randomly choose one
				if r == 1:
					ghost_m = potentialMoves[distance.index(min(distance))]
				else:
					potentialMoves.reverse() # Flipping the moves is one way that lets the script find a different equivalent minimum
					distance.reverse()
					ghost_m = potentialMoves[distance.index(min(distance))]
				
				if (ghost_m == 1):
					t_y[i] = ghost_y[i] - 1;
				elif (ghost_m == 2):
					t_x[i] = ghost_x[i] + 1;
				elif (ghost_m == 3):
					t_y[i] = ghost_y[i] + 1;
				else:
					t_x[i] = ghost_x[i] - 1;
			else:
				print('Ghost move error');
	return t_x, t_y

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
			print("Moving through!");
			return True;
	return False;

def gameStatus(pacman_x, pacman_y, ghost_x, ghost_y, pellet_x, pellet_y):
	'''
	Check if pacman has won or lost, and if game has ended.
	'''
	ended = False;
	won = False;
	if (pacman_x == pellet_x and pacman_y == pellet_y): # Game own
		won = True;
		ended = True;
	for i in range(len(ghost_x)): # Check if pacman eaten by any ghosts
		if (pacman_x == ghost_x[i] and pacman_y == ghost_y[i]):
			won = False;
			ended = True;
			break;  
	return ended, won;  

def game_func(move, pacman_x, pacman_y, ghost_x, ghost_y, goal_x, goal_y, grid, numGhosts, ghost_type):
	won = False
	ended = False
	prevPacman_x, prevPacman_y = pacman_x, pacman_y;
	# Pacman move
	if (move == 1) and not (grid[pacman_y - 1][pacman_x] == True):
		pacman_y = pacman_y - 1;
	elif  (move == 2) and not (grid[pacman_y][pacman_x + 1] == True):
		pacman_x = pacman_x + 1;
	elif  (move == 3) and not (grid[pacman_y + 1][pacman_x] == True):
		pacman_y = pacman_y + 1;
	elif  (move == 4) and not (grid[pacman_y][pacman_x - 1] == True):
		pacman_x = pacman_x - 1;

	# Move ghost if pacman was not eaten by pacman move
	t_x = ghost_x;
	t_y = ghost_y;
	t_x, t_y = ghost_move(prevPacman_x, prevPacman_y, ghost_x, ghost_y, numGhosts, grid, ghost_type);
	
	# Check if game has ended or won
	ended, won = gameStatus(pacman_x, pacman_y, t_x, t_y, goal_x, goal_y);

	# Check if ghost and pacman tried to move through each other
	if (moveThrough(pacman_x, pacman_y, prevPacman_x, prevPacman_y, t_x, t_y, ghost_x, ghost_y)):
		ended = True;
		won = False; 
		# Return pacman's new position and original ghost positions
		return pacman_x, pacman_y, ghost_x, ghost_y, goal_x, goal_y, ended, won;
	# Return pacman's new position and ghosts' new positions
	return pacman_x, pacman_y, t_x, t_y, goal_x, goal_y, ended, won