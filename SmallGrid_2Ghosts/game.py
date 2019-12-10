import pygame
import math
import random
import time
from random import randint as ri
import threading

class Game():
    def __init__(self):
        pass
        pygame.init()
        pygame.font.init()
        gridX = 5;
        gridY = 5;
        self.gridsize = [gridX,gridY];
        self.grid = [[True, True, True, True, True],
                    [True, False, False, False, True],
                    [True, False, False, False, True],
                    [True, False, False, False, True],
                    [True, True, True, True, True]];
   
        width, height = 65*self.gridsize[0], 65*self.gridsize[1]+74
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Game")
        self.pacman_x, self.pacman_y = 1, 1;
        self.ghost_x = [];
        self.ghost_y = [];
        self.ghost_type = ['Chase', 'Random'];
        self.goal_x, self.goal_y = 3,1;
        self.moves = [];
        self.pacman = [[False for x in range(self.gridsize[0])] for y in range(self.gridsize[1])]
        self.ghost = [[False for x in range(self.gridsize[0])] for y in range(self.gridsize[1])]
        self.goal = [[False for x in range(self.gridsize[0])] for y in range(self.gridsize[1])]
        self.pacman[self.pacman_y][self.pacman_x] = True;
        #self.ghost[self.ghost_y][self.ghost_x] = True;
        self.goal[self.goal_y][self.goal_x] = True;
        self.won = False
        self.lost = False
        self.turn_count=-1
        self.ended = False
        self.s_num = 0;
		

        self.clock = pygame.time.Clock()
        self.initGraphics()
        
    def updateState(self, pacman_x, pacman_y, ghost_x, ghost_y, numGhosts, ghost_type):
        '''
        test
        '''
        self.pacman[self.pacman_y][self.pacman_x]=False
        for i in range(len(self.ghost_x)):
            self.ghost[self.ghost_y[i]][self.ghost_x[i]]=False

        self.pacman_x = pacman_x;
        self.pacman_y = pacman_y;
        self.ghost_x = ghost_x;
        self.ghost_y = ghost_y;
		
        filen = 'ss_' + str(self.s_num) + '.png';
        pygame.image.save(self.screen,filen)
        self.s_num = self.s_num + 1;
        
        self.pacman[self.pacman_y][self.pacman_x]=True
        for i in range(numGhosts):
            self.ghost[self.ghost_y[i]][self.ghost_x[i]] = ghost_type[i]

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
        for x in range(self.gridsize[0]):
            for y in range(self.gridsize[1]-1):
                self.screen.blit(self.lineh, [x*64+5, (y+1)*64])
        
        for y in range(self.gridsize[1]):
            for x in range(self.gridsize[0]-1):
                self.screen.blit(self.linev, [(x+1)*64, (y)*64+5])
        
        for x in range(self.gridsize[0]):
            for y in range(self.gridsize[1]):
                if self.ghost[y][x] == 'Random':
                    self.screen.blit(self.g, [(x)*64+5, (y)*64+5])
                elif self.ghost[y][x] == 'Chase':
                    self.screen.blit(self.g2, [(x)*64+5, (y)*64+5])
                elif self.pacman[y][x] == True:
                    self.screen.blit(self.p, [(x)*64+5, (y)*64+5])
                elif self.goal[y][x] == True:
                    self.screen.blit(self.w, [(x)*64+5, (y)*64+5])
                elif self.grid[y][x] == True:
                    self.screen.blit(self.wall, [(x)*64+5, (y)*64+5])
        
    def drawHUD(self):
        if not self.ended:
            self.screen.blit(self.score,[0, 65*self.gridsize[1]])
            myfont = pygame.font.SysFont(None, 32)
            label1 = myfont.render("1: Up, 2: Right", 1, (255,255,255))
            label2 = myfont.render("3: Down, 4: Left", 1, (255,255,255))
        else:
            self.screen.blit(self.score,[0, 65*self.gridsize[1]])
            myfont = pygame.font.SysFont(None, 32)
            label2 = myfont.render("", 1, (255,255,255))
            if self.won == False:
                label1 = myfont.render("You've been eaten!", 1, (255,255,255))
            else: 
                label1 = myfont.render("You've won!", 1, (255,255,255))
        self.screen.blit(label1,(5,65*self.gridsize[1] + 10))
        self.screen.blit(label2,(5,65*self.gridsize[1] + 40))
        
    def update(self):
        #if not self.ended:
        self.clock.tick(60)
        self.screen.fill(0)
        self.drawBoard()
        #self.drawHUD()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()              
        pygame.display.flip()
        if self.ended:
            self.end()
     
    def end(self):
        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()
        pygame.display.flip()
        filen = 'ss_' + str(self.s_num) + '.png';
        pygame.image.save(self.screen,filen)
        time.sleep(0.4)
        #exit()
        #while True:
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            exit()
        #    pygame.display.flip()
        

