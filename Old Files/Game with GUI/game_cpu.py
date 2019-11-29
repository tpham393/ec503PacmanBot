# A version of the game with a GUI you need to have pygame to run this
# pip install pygame

import pygame
import math
import random
import time
import threading

gridsize = [5, 5];
pacman_x, pacman_y = 1, 3;
ghost_x, ghost_y = 3, 3;
goal_x, goal_y = 3, 1;
pacman = [['False' for x in range(gridsize[0])] for y in range(gridsize[1])]
ghost  = [['False' for x in range(gridsize[0])] for y in range(gridsize[1])]
goal = [['False' for x in range(gridsize[0])] for y in range(gridsize[1])]
pacman[pacman_y][pacman_x] = 'True';
ghost[ghost_y][ghost_x] = 'True';
goal[goal_y][goal_x] = 'True';
won = 'False'
lost = 'False'
turn_count=-1
ended=False
loaded=False
pacman_move = 0;
moved = True

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
        global pacman_move
        global ghost
        global ghost_x
        global ghost_y
        global goal
        global goal_x
        global goal_y
        global loaded
        global won
        global tied
        global loaded
        global turn
        global turn_count
        global ended
        global moved
        self.clock = pygame.time.Clock()
        self.initGraphics()
        
    def initGraphics(self):
        self.linev=pygame.image.load("Graphics/line.png")
        self.lineh=pygame.transform.rotate(pygame.image.load("Graphics/line.png"), -90)
        self.score=pygame.image.load("Graphics/score.png")
        self.p=pygame.image.load("Graphics/p.png")
        self.g=pygame.image.load("Graphics/g.png")
        self.w=pygame.image.load("Graphics/w.png")
        
    def drawBoard(self):
        for x in range(gridsize[0]):
            for y in range(gridsize[1]-1):
                self.screen.blit(self.lineh, [x*64+5, (y+1)*64])
        
        for y in range(gridsize[1]):
            for x in range(gridsize[0]-1):
                self.screen.blit(self.linev, [(x+1)*64, (y)*64+5])
        
        for x in range(gridsize[0]):
            for y in range(gridsize[1]):
                if ghost[y][x] == 'True':
                    self.screen.blit(self.g, [(x)*64+5, (y)*64+5])
                elif pacman[y][x] == 'True':
                    self.screen.blit(self.p, [(x)*64+5, (y)*64+5])
                elif goal[y][x] == 'True':
                    self.screen.blit(self.w, [(x)*64+5, (y)*64+5])
        
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
            if won == 'False':
                label1 = myfont.render("You've been eaten!", 1, (255,255,255))
            else: 
                label1 = myfont.render("You've won!", 1, (255,255,255))
        self.screen.blit(label1,(5,65*gridsize[1] + 10))
        self.screen.blit(label2,(5,65*gridsize[1] + 40))
        
    def update(self):
        global loaded
        global pacman_x
        global pacman_y
        global pacman_move
        global ghost_x
        global ghost_y
        global goal
        global loaded
        global won
        global turn
        global tied
        global moved
        if not ended:
            self.clock.tick(60)
            self.screen.fill(0)
            self.drawBoard()
            self.drawHUD()
            if not loaded:
                turn = False
                loaded = True
                self.turn_timer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if (pacman_move == 1) and not (pacman_y - 1 == -1):
                    pacman[pacman_y][pacman_x]='False'
                    pacman_y = pacman_y - 1;
                    pacman[pacman_y][pacman_x]='True'
                    self.ghost_move()
                    self.win_check()
                    turn = False
                    moved = True
                elif (pacman_move == 2) and not (pacman_x + 1 == gridsize[0]):
                    pacman[pacman_y][pacman_x]='False'
                    pacman_x = pacman_x + 1;
                    pacman[pacman_y][pacman_x]='True'
                    self.ghost_move()
                    self.win_check()
                    turn = False
                    moved = True
                elif (pacman_move == 3) and not (pacman_y + 1 == gridsize[1]):
                    pacman[pacman_y][pacman_x]='False'
                    pacman_y = pacman_y + 1;
                    pacman[pacman_y][pacman_x]='True'
                    self.ghost_move()
                    self.win_check()
                    turn = False
                    moved = True
                elif (pacman_move == 4) and not (pacman_x - 1 == -1):
                    pacman[pacman_y][pacman_x]='False'
                    pacman_x = pacman_x - 1;
                    pacman[pacman_y][pacman_x]='True'
                    self.ghost_move()
                    self.win_check()
                    turn = False
                    moved = True
                
            pygame.display.flip()
        else:
            self.end()
        
    def ghost_move(self):
        global ghost_x
        global ghost_y
        self.drawBoard()
        self.win_check()
        ghost_move = random.randint(1,4)
        if (ghost_move == 1) and not (ghost_y - 1 == -1):
            ghost[ghost_y][ghost_x]='False'
            ghost_y = ghost_y - 1;
            ghost[ghost_y][ghost_x]='True'
        elif (ghost_move == 2) and not (ghost_x + 1 == gridsize[0]):
            ghost[ghost_y][ghost_x]='False'
            ghost_x = ghost_x + 1;
            ghost[ghost_y][ghost_x]='True'
        elif (ghost_move == 3) and not (ghost_y + 1 == gridsize[1]):
            ghost[ghost_y][ghost_x]='False'
            ghost_y = ghost_y + 1;
            ghost[ghost_y][ghost_x]='True'
        elif (ghost_move == 4) and not (ghost_x - 1 == -1):
            ghost[ghost_y][ghost_x]='False'
            ghost_x = ghost_x - 1;
            ghost[ghost_y][ghost_x]='True'
        else:
            self.ghost_move()
            
    def turn_timer(self):
        global ended
        global turn
        global pacman_move
        global moved

        if moved:
            pacman_move = random.randint(1,4) #This is where you can edit for the random moves
            print(pacman_move)
            turn = True;
            moved = False
        threading.Timer(2.0, self.turn_timer).start()
            
    
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
        if (ghost_x == pacman_x) and (ghost_y == pacman_y):
            won = 'False'
            ended = True
        elif (goal_x == pacman_x) and (goal_y == pacman_y):
            won = 'True'
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