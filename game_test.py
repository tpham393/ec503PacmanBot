# A version of the game with a GUI you need to have pygame to run this
# pip install pygame

import pygame
import math
import random
import time
import game_funcs as g
from random import randint as ri
import threading

gridsize = [7, 7];
grid = [['True', 'True', 'True', 'True', 'True', 'True', 'True'], 
        ['True', 'False', 'False', 'False', 'False', 'False', 'True'],
        ['True', 'False', 'True', 'False', 'True', 'False', 'True'],
        ['True', 'False', 'False', 'False', 'False', 'False', 'True'],
        ['True', 'False', 'True', 'True', 'True', 'False', 'True'],
        ['True', 'False', 'False', 'False', 'False', 'False', 'True'],
        ['True', 'True', 'True', 'True', 'True', 'True', 'True']];

pacman_x, pacman_y = 1, 5;
ghost_x, ghost_y = 1, 1;
goal_x, goal_y = 5, 1;
moves = [];
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
        self.clock = pygame.time.Clock()
        self.initGraphics()
        
    def initGraphics(self):
        self.linev=pygame.image.load("Graphics/line.png")
        self.lineh=pygame.transform.rotate(pygame.image.load("Graphics/line.png"), -90)
        self.score=pygame.image.load("Graphics/score.png")
        self.p=pygame.image.load("Graphics/p.png")
        self.g=pygame.image.load("Graphics/g.png")
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
                if ghost[y][x] == 'True':
                    self.screen.blit(self.g, [(x)*64+5, (y)*64+5])
                elif pacman[y][x] == 'True':
                    self.screen.blit(self.p, [(x)*64+5, (y)*64+5])
                elif goal[y][x] == 'True':
                    self.screen.blit(self.w, [(x)*64+5, (y)*64+5])
                elif grid[y][x] == 'True':
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
        global ghost_x
        global ghost_y
        global goal
        global won
        global tied
        if not ended:
            self.clock.tick(60)
            self.screen.fill(0)
            self.drawBoard()
            self.drawHUD()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                key=pygame.key.get_pressed()               
            pygame.display.flip()
        else:
            self.end()
     
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

# Updating the visuals with this thread is smoother than in the while loop but is not necessary. 
def turn_timer():
   tg.update()
   threading.Timer(0.01, turn_timer).start()

turn_timer();

while not ended:
    # tg.update(); Updating the game here skips ending sequence updates. Fine for testing but visually the above function is required to be smoother. 
    # There are still minor bugs though with this but I haven't figure out what's happening yet.
    time.sleep(1)
    move = ri(1,4);
    pacman_x2, pacman_y2, ghost_x2, ghost_y2, goal_x, goal_y, ended, won, moved = g.game_func(move, pacman_x, pacman_y, ghost_x, ghost_y, goal_x, goal_y, gridsize, grid)
    if moved:
        moves.append(move)
        pacman[pacman_y][pacman_x]='False'
        ghost[ghost_y][ghost_x]='False'
        pacman_x, pacman_y, ghost_x, ghost_y = pacman_x2, pacman_y2, ghost_x2, ghost_y2
        pacman[pacman_y][pacman_x]='True'
        ghost[ghost_y][ghost_x]='True'
    
print(moves)

    
