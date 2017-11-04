#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 21:16:31 2016

@author: mateusz

Here are drawn levels of the game and bricks.

"""
import pygame, os 
import numpy as np

import const




class Level():
    rect = const.screen_level
    def __init__(self,levels):
        self.levels = levels
        self.Screen = const.Screen
        self.background = pygame.Surface(self.Screen.size).convert()
        self.background.blit(const.load_image(const.tlo),(0,0))
        self.edge = const.edge
        self.count= 0 

                
    def draw_level(self, level_number):
        self.count = 0
        ''' rysowanie level'''
        for i in range(len(self.levels[level_number])):       
            for j in range(len(self.levels[level_number][i])):
                c = self.levels[level_number][i][j] -1 #zacząc od 1 czyli 0 
                if (c >- 1) and (c != 3):
                    self.count+=1
                    Net(self,j, i, c) 
                if c == 3:
                    Net2(self,j,i,c)
                if c == 4:
                    Net3(self,j,i,c)
                    
# c == 3 - nie niszczy sie
# c == 4 - bonusy
        
    def count(self):
        return self.count
            

class Net(pygame.sprite.Sprite):
    def __init__(self, board,x, y, c):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.levels[c]
        self.rect = self.image.get_rect()
        self.rect.left = board.rect.left + x*self.rect.width
        self.rect.top = board.rect.top + y*self.rect.height

        
# nie da się zniszczyć        
class Net2(pygame.sprite.Sprite):
    def __init__(self, board,x, y, c):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.levels[c]
        self.rect = self.image.get_rect()
        self.rect.left = board.rect.left + x*self.rect.width
        self.rect.top = board.rect.top + y*self.rect.height
        
# bonusy        
class Net3(pygame.sprite.Sprite):
    def __init__(self, board,x, y, c):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.levels[c]
        self.rect = self.image.get_rect()
        self.rect.left = board.rect.left + x*self.rect.width
        self.rect.top = board.rect.top + y*self.rect.height
 
