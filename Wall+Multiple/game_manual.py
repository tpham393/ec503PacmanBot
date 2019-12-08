# A version of the game with a GUI you need to have pygame to run this
# pip install pygame

import pygame
import math
import random
import time

gridsize = [7, 7];
grid = [[True, True, True, True, True, True, True], 
		[True, False, False, False, False, False, True],
		[True, False, True, False, True, False, True],
		[True, False, False, False, False, False, True],
		[True, False, True, True, True, False, True],
		[True, False, False, False, False, False, True],
		[True, True, True, True, True, True, True]];
		
pacman_x, pacman_y = 1, 5;
ghost_x, ghost_y = [1, 1], [2, 1];
ghost_type = ['Random', 'Chase'];
numGhosts = 2;
goal_x, goal_y = 5, 1;
pacman = [[False for x in range(gridsize[0])] for y in range(gridsize[1])]
ghost  = [[False for x in range(gridsize[0])] for y in range(gridsize[1])]
goal = [[False for x in range(gridsize[0])] for y in range(gridsize[1])]
pacman[pacman_y][pacman_x] = True;
for i in range(numGhosts):
	ghost[ghost_y[i]][ghost_x[i]]=ghost_type[i]
goal[goal_y][goal_x] = True;
won = False
lost = False
turn_count=-1
ended=False
valid_m = True;

class Game():
	def __init__(self):
		pass
		pygame.init()
		pygame.font.init()
		width, height = 65*gridsize[0], 65*gridsize[1]+74
		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption("Game")
		global pacman
		global pacman_x
		global pacman_y
		global ghost
		global ghost_type
		global numGhosts
		global ghost_x
		global ghost_y
		global goal
		global goal_x
		global goal_y
		global won
		global tied
		global loaded
		global turn_count
		global ended
		global valid_m
		self.clock = pygame.time.Clock()
		self.initGraphics()
		
	def initGraphics(self):
		self.linev=pygame.image.load("Graphics/line.png")
		self.lineh=pygame.transform.rotate(pygame.image.load("Graphics/line.png"), -90)
		self.score=pygame.image.load("Graphics/score.png")
		self.p=pygame.image.load("Graphics/p.png")
		self.g=pygame.image.load("Graphics/g.png")
		self.g2=pygame.image.load("Graphics/g2.png")
		self.w=pygame.image.load("Graphics/w.png")
		self.wall=pygame.image.load("Graphics/wall.png")
		
	def drawBoard(self):
		for x in range(gridsize[0]):
			for y in range(gridsize[1]-1):
				self.screen.blit(self.lineh, [x*64+5, (y+1)*64])
		
		for y in range(gridsize[1]):
			for x in range(gridsize[0]-1):
				self.screen.blit(self.linev, [(x+1)*64, (y)*64+5])
		
		for x in range(gridsize[0]):
			for y in range(gridsize[1]):
				if ghost[y][x] == 'Random':
					self.screen.blit(self.g, [(x)*64+5, (y)*64+5])
				elif ghost[y][x] == 'Chase':
					self.screen.blit(self.g2, [(x)*64+5, (y)*64+5])
				elif pacman[y][x] == True:
					self.screen.blit(self.p, [(x)*64+5, (y)*64+5])
				elif goal[y][x] == True:
					self.screen.blit(self.w, [(x)*64+5, (y)*64+5])
				elif grid[y][x] == True:
					self.screen.blit(self.wall, [(x)*64+5, (y)*64+5])
		
	def drawHUD(self):
		global won
		if not ended:
			self.screen.blit(self.score,[0, 65*gridsize[1]])
			myfont = pygame.font.SysFont(None, 32)
			label1 = myfont.render("1: Up, 2: Right", 1, (255,255,255))
			label2 = myfont.render("3: Down, 4: Left", 1, (255,255,255))
		else:
			self.screen.blit(self.score,[0, 65*gridsize[1]])
			myfont = pygame.font.SysFont(None, 32)
			label2 = myfont.render("", 1, (255,255,255))
			if won == False:
				label1 = myfont.render("You've been eaten!", 1, (255,255,255))
			else: 
				label1 = myfont.render("You've won!", 1, (255,255,255))
		self.screen.blit(label1,(5,65*gridsize[1] + 10))
		self.screen.blit(label2,(5,65*gridsize[1] + 40))
		
	def update(self):
		global loaded
		global pacman_x
		global pacman_y
		global ghost_x
		global ghost_y
		global goal
		global won
		global tied
		global ended
		global grid
		if not ended:
			self.clock.tick(60)
			self.screen.fill(0)
			self.drawBoard()
			self.drawHUD()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				key=pygame.key.get_pressed()
				if key[pygame.K_1] and not (grid[pacman_y - 1][pacman_x] == True):
					pacman[pacman_y][pacman_x]=False
					pacman_y = pacman_y - 1;
					pacman[pacman_y][pacman_x]=True
					temp = True;
					for i in range(len(ghost_x)):
						if (pacman_x == ghost_x[i] and pacman_y == ghost_y[i]):
							temp = False;
					if temp:
						self.ghost_move()
					self.win_check()
				elif  key[pygame.K_2] and not (grid[pacman_y][pacman_x + 1] == True):
					pacman[pacman_y][pacman_x]=False
					pacman_x = pacman_x + 1;
					pacman[pacman_y][pacman_x]=True
					temp = True;
					for i in range(len(ghost_x)):
						if (pacman_x == ghost_x[i] and pacman_y == ghost_y[i]):
							temp = False;
					if temp:
						self.ghost_move()
					self.win_check()
				elif  key[pygame.K_3] and not (grid[pacman_y + 1][pacman_x] == True):
					pacman[pacman_y][pacman_x]=False
					pacman_y = pacman_y + 1;
					pacman[pacman_y][pacman_x]=True
					temp = True;
					for i in range(len(ghost_x)):
						if (pacman_x == ghost_x[i] and pacman_y == ghost_y[i]):
							temp = False;
					if temp:
						self.ghost_move()
					self.win_check()
				elif  key[pygame.K_4] and not (grid[pacman_y][pacman_x - 1] == True):
					pacman[pacman_y][pacman_x]=False
					pacman_x = pacman_x - 1;
					pacman[pacman_y][pacman_x]=True
					temp = True;
					for i in range(len(ghost_x)):
						if (pacman_x == ghost_x[i] and pacman_y == ghost_y[i]):
							temp = False;
					if temp:
						self.ghost_move()
					self.win_check()
				elif key[pygame.K_SPACE]: # ghost move and not pacman
					self.ghost_move()
				
			pygame.display.flip()
		else:
			self.end()
		
	def validGhostMove(self, x, y):
		'''
		Given new ghost location and locations of the other ghosts, see if new location is valid.
		'''
		global valid_m
		valid_m = True;
		# Check if ghost move is into a wall or not
		if (grid[y][x] == True): 
			valid_m = False;
		# Check if new ghost position overlaps with other ghost positions
		for i in range(len(ghost_x)):
			if (x==ghost_x[i]) and (y==ghost_y[i]):
				valid_m = False;

	# Random Moving Ghost.
	def ghost_move(self): 
		global pacman_x
		global pacman_y
		global ghost_x
		global ghost_y
		global valid_m
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
			self.validGhostMove(t_x[i], t_y[i]-1)
			if valid_m:
				distance.append(((((pacman_x-ghost_x[i])**2) + ((pacman_y-(ghost_y[i]-1))**2))**0.5));
				potentialMoves.append(1);
			self.validGhostMove(t_x[i]+1, t_y[i])
			if valid_m:
				distance.append(((((pacman_x-(ghost_x[i]+1))**2) + ((pacman_y-(ghost_y[i]))**2))**0.5));
				potentialMoves.append(2);
			self.validGhostMove(t_x[i], t_y[i]+1)
			if valid_m:
				distance.append(((((pacman_x-ghost_x[i])**2) + ((pacman_y-(ghost_y[i]+1))**2))**0.5));
				potentialMoves.append(3);
			self.validGhostMove(t_x[i]-1, t_y[i])
			if valid_m:
				distance.append(((((pacman_x-(ghost_x[i]-1))**2) + ((pacman_y-(ghost_y[i]))**2))**0.5));
				potentialMoves.append(4);

			# Randomly choose a valid move
			if potentialMoves: 
				if (ghost_type[i] == 'Random'):
					ghost_idx = random.randint(0,len(potentialMoves)-1);
					ghost_m = potentialMoves[ghost_idx]; # Random move
					# Update ghost location
					if (ghost_m == 1):
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_y[i] = ghost_y[i] - 1;
						ghost[ghost_y[i]][ghost_x[i]]='Random'
					elif (ghost_m == 2):
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_x[i] = ghost_x[i] + 1;
						ghost[ghost_y[i]][ghost_x[i]]='Random'
					elif (ghost_m == 3):
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_y[i] = ghost_y[i] + 1;
						ghost[ghost_y[i]][ghost_x[i]]='Random'
					else:
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_x[i] = ghost_x[i] - 1;
						ghost[ghost_y[i]][ghost_x[i]]='Random'
				elif (ghost_type[i] == 'Chase'):
					r = random.randint(1,2) # If there are two optimal moves allows it to randomly choose one
					if r == 1:
						ghost_m = potentialMoves[distance.index(min(distance))]
					else:
						potentialMoves.reverse() # Flipping the moves is one way that lets the script find a different equivalent minimum
						distance.reverse()
						ghost_m = potentialMoves[distance.index(min(distance))]
					
					if (ghost_m == 1):
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_y[i] = ghost_y[i] - 1;
						ghost[ghost_y[i]][ghost_x[i]]='Chase'
					elif (ghost_m == 2):
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_x[i] = ghost_x[i] + 1;
						ghost[ghost_y[i]][ghost_x[i]]='Chase'
					elif (ghost_m == 3):
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_y[i] = ghost_y[i] + 1;
						ghost[ghost_y[i]][ghost_x[i]]='Chase'
					else:
						ghost[ghost_y[i]][ghost_x[i]]=False
						ghost_x[i] = ghost_x[i] - 1;
						ghost[ghost_y[i]][ghost_x[i]]='Chase'
				else:
					print('Ghost move error');      
	
	def win_check(self):
		global pacman
		global pacman_x
		global pacman_y
		global ghost
		global ghost_x
		global ghost_y
		global goal_x
		global goal_y
		global won
		global turn_count
		global ended
		turn_count = turn_count + 1
		for i in range(len(ghost_x)):
			if (ghost_x[i] == pacman_x) and (ghost_y[i] == pacman_y):
				won = False
				ended = True
			elif (goal_x == pacman_x) and (goal_y == pacman_y):
				won = True
				ended = True
	
	def end(self):
		self.screen.fill(0)
		self.drawBoard()
		self.drawHUD()
		pygame.display.flip()
		time.sleep(5)
		exit()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()
		
		
tg = Game()
while True:
	tg.update()
