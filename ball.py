#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 21:23:51 2016

The position and movement of the ball. Killing bricks and bonuses.

@author: mateusz
"""

import pygame, os, random
import math
import numpy as np


import const

screen = pygame.display.set_mode(const.Screen.size, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self,board,disc1,net,net2,net3,live):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.board = board
        self.disc = disc1
        self.update = self.start
        self.net = net
        self.net2 = net2
        self.net3 = net3
        self.count2 = 0
        self.nr = 0
        self.live = live
        self.start_bonus = 0 

    def live(self):
        return self.live
        
    def start(self):
        self.rect.centerx = self.disc.rect.centerx
        self.rect.bottom = self.disc.rect.top
        if pygame.key.get_pressed()[pygame.K_RETURN] == 1: # klikniecie - start 
            self.x = self.rect.centerx
            self.y = self.rect.centery
            self.dx = 0
            self.dy = 1
            self.update = self.move

    def setint(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
    def move(self):
        # odbicie
        if self.rect.colliderect(self.disc.rect) and self.dy > 0:
            b_pos = self.rect.width + self.rect.left - self.disc.rect.left - 1
            b_max = self.rect.width + self.disc.rect.width - 2
            fac = float(b_pos)/b_max
            ang = math.radians(const.ang_h - fac*(const.ang_h - const.ang_l))
            self.dx = const.b_speed*math.cos(ang)
            self.dy = -const.b_speed*math.sin(ang)
            
        #poruszamnie
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.setint()

        #odbicie od ścian
        if self.rect.left < self.board.rect.left:
            self.rect.left = self.board.rect.left
            self.dx = -self.dx
            
        if self.rect.right > self.board.rect.right:
            self.rect.right = self.board.rect.right
            self.dx = -self.dx
            
        if self.rect.top < self.board.rect.top:
            self.rect.top = self.board.rect.top
            self.dy = -self.dy
            
        if self.rect.top > self.board.rect.bottom:
            self.update = self.start
            self.live -= 1
            
        sound = const.load_sound('bomb.wav')  
        
        kost2 = pygame.sprite.spritecollide(self, self.net2, False) #nie da się zniszczyć
        if kost2:
            for k2 in kost2:

                if self.rect.top > k2.rect.top:
                    self.rect.top = k2.rect.top
                    self.dy = -self.dy
                    
                if self.rect.bottom < k2.rect.bottom:
                    self.rect.bottom = k2.rect.bottom
                    self.dy =  -self.dy                 

                if self.rect.left < k2.rect.left:
                    self.rect.left = k2.rect.left
                    self.dx = -self.dx
                    
                if self.rect.right > k2.rect.right:
                    self.rect.right = k2.rect.right
                    self.dx = -self.dx
                    

                    
        kost3 = pygame.sprite.spritecollide(self, self.net3, False) # bonusy
        if kost3:
            oldrect = self.rect
            left = right = up = down = 0
            for k3 in kost3:
                if oldrect.top < k3.rect.top < oldrect.bottom < k3.rect.bottom:
                    self.rect.bottom = k3.rect.top
                    self.setint()
                    up = -1

                if k3.rect.top < oldrect.top < k3.rect.bottom < oldrect.bottom:
                    self.rect.top = k3.rect.bottom
                    self.setint()
                    down = 1            

                if oldrect.left < k3.rect.left < oldrect.right < k3.rect.right:
                    self.rect.right = k3.rect.left
                    self.setint()
                    left = -1

                if k3.rect.left < oldrect.left < k3.rect.right < oldrect.right:
                    self.rect.left = k3.rect.right
                    self.setint()
                    right = 1
              
                k3.kill()  
                nr1 = random.choice(range(1,7,1))
                bon = Bonus(self.disc, nr1)
                self.start_bonus = bon
                
        kost = pygame.sprite.spritecollide(self, self.net, False)
        if kost:
            oldrect = self.rect
            left = right = up = down = 0
            for k in kost:
            
                if oldrect.top < k.rect.top < oldrect.bottom < k.rect.bottom:
                    self.rect.bottom = k.rect.top
                    self.setint()
                    up = -1

                if k.rect.top < oldrect.top < k.rect.bottom < oldrect.bottom:
                    self.rect.top = k.rect.bottom
                    self.setint()
                    down = 1            

                if oldrect.left < k.rect.left < oldrect.right < k.rect.right:
                    self.rect.right = k.rect.left
                    self.setint()
                    left = -1

                if k.rect.left < oldrect.left < k.rect.right < oldrect.right:
                    self.rect.left = k.rect.right
                    self.setint()
                    right = 1
        
                sound.play()            
                self.count2+=1
                k.kill()

            # odbicie od kostek
            if left + right != 0:
                self.dx = (left + right)*abs(self.dx)
            if up + down != 0:
                self.dy = (up + down)*abs(self.dy)
                
    def nr(self):
        return self.nr
       
    def count2(self):
        return self.count2
        
    def start_bonus (self):
        return self.start_bonus

        
class Bonus(pygame.sprite.Sprite):

    def __init__(self,disc1, nr):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.nr = nr
        self.image = const.load_image(const.bonus_image[self.nr],-1)
        self.rect = self.image.get_rect()        
        self.disc = disc1
        self.speed = 0
        self.liv = 0        
        self.rect.centerx = random.choice(range(60,600,1))
        self.rect.centery = 50
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.dy = 3
        self.dx = 0        
        self.update = self.move
        
    def setint(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y        

    def move(self):
        # odbicie
        if self.rect.colliderect(self.disc.rect) and self.dy > 0:
                    sound = const.load_sound('happy.wav')
                    self.x += 1000
                    self.dy = 0
                    sound.play()
                    
                    if self.nr == 1:
                        self.liv = 1
                        return 1
                       
                    if self.nr == 2:
                        self.liv=  - 1
                        return -1
                        
                    if self.nr == 3:
                        self.liv = 120
                        return 120
                        
                    if  self.nr == 4:
                        self.liv = 30
                        return 30
                    if self.nr == 5:
                        self.liv = 100
                        return 100
                    if self.nr ==6:
                        self.liv = -100
                        return -100

        #poruszamnie
        self.speed = 0
        self.liv = 0 
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.setint()
        
 