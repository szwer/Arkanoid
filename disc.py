#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 13:09:14 2016

@author: mateusz

The position and movement of the disc.

"""

import pygame 

import const

    
class Disc(pygame.sprite.Sprite):
    def __init__(self,board):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.board = board 
        self.rect.bottom = board.rect.bottom - const.edge
        
        self.rect.centerx = const.width/2
        self.speed = const.speed
    def location(self):
        if not self.board.rect.contains(self.rect):
            if self.rect.left < self.board.rect.left:
                self.rect.left = self.board.rect.left
            elif self.rect.right > self.board.rect.right:
                self.rect.right = self.board.rect.right
                
    def move_right(self):
        self.new_move = self.speed
        self.rect.centerx += self.new_move
        self.location()
        
    def move_left(self):
        self.new_move = -self.speed
        self.rect.centerx+= self.new_move
        self.location()

