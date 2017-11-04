#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:37:27 2016

@author: mateusz
"""
import pygame, os, pickle
from pygame.locals import * 

import const, level, ball, disc

screen = pygame.display.set_mode(const.Screen.size, 0)

def main(poczatek,poz):
    
    start_ticks=pygame.time.get_ticks()
    lev = 0
    n = 3
    score1=0
    score2 = 0 
    t= 0
    l3= 0 
    
    ball.Bonus.image = const.load_image(const.bonus_image[0],-1)
    
    level.Net.levels = [const.load_image(const.kostka), const.load_image(const.kostka1),const.load_image(const.kostka2),const.load_image(const.kostka3),const.load_image(const.kostka4)]
    level.Net2.levels = [const.load_image(const.kostka), const.load_image(const.kostka1),const.load_image(const.kostka2),const.load_image(const.kostka3),const.load_image(const.kostka4)]
    level.Net3.levels = [const.load_image(const.kostka), const.load_image(const.kostka1),const.load_image(const.kostka2),const.load_image(const.kostka3),const.load_image(const.kostka4)]

    clock = pygame.time.Clock()
    pygame.display.set_caption('Arkanoid by Mateusz')
    levels = const.levels[poz]
    board = level.Level(levels)
    screen.blit(board.background, (0, 0))
   
    pygame.display.flip()  

    while poczatek: 
        disc.Disc.image = const.load_image(const.d)
        ball.Ball.image = const.load_image(const.b, -1)
        speed = const.speed_time
        balls = pygame.sprite.Group()
        bricks = pygame.sprite.Group()
        bricks2 = pygame.sprite.Group()
        bricks3 = pygame.sprite.Group()
        bonus = pygame.sprite.Group()
        
        all = pygame.sprite.RenderUpdates()
    
        disc.Disc.containers = all
        ball.Ball.containers = all, balls
        level.Net.containers = all, bricks
        level.Net2.containers = all, bricks2
        level.Net3.containers = all, bricks3

        ball.Bonus.containers = all, bonus
        
        paddle = disc.Disc(board)
        
        b = ball.Ball(board, paddle, bricks,bricks2,bricks3,n)   
       
        board.draw_level(lev)
        var = [False, False]

        running = True
        run = False 
        run2 = False

        l2=0
        check_live = 3
       
        while running:
                
                l1 = b.live
                live = l1 + l2 + l3
                
                if live != check_live:
                    disc.Disc.image = const.load_image(const.d)
                    ball.Ball.image = const.load_image(const.b,-1)
                    speed = const.speed_time
                    
                if b.start_bonus != 0:
                    
                    if b.start_bonus.liv ==1 or b.start_bonus.liv==-1:
                        l2= b.start_bonus.liv
                        
                    if b.start_bonus.liv == 30:
                        speed = 30
                        disc.Disc.image = const.load_image(const.d3)
                        ball.Ball.image = const.load_image(const.b3,-1)
                        
                    if b.start_bonus.liv==120:
                        speed = 120
                        disc.Disc.image = const.load_image(const.d2)
                        ball.Ball.image = const.load_image(const.b2,-1)
                        
                    if b.start_bonus.liv ==100:
                        score2 += b.start_bonus.liv
                    if b.start_bonus.liv==-100:
                        score1 += b.start_bonus.liv
                        
                check_live = live 
                             
                if board.count == b.count2:
                    lev+=1
                    n =  live
                    run2 = True
                    break
    
                if live == 0 :
                    run = True 
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                       menu()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            menu()
                        if event.key == pygame.K_r:                                           
                            l3 -= 1
                            n =  live
                            run2 = True
                            running = False
                                                        
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            start_ticks1=pygame.time.get_ticks()
                            while 1: 
                                event = pygame.event.wait()
                                pygame.display.set_caption("Pause")
                                
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    pygame.display.set_caption('Arkanoid by Mateusz')
                                    t += round((-start_ticks1+pygame.time.get_ticks())/1000)
                                    break
                                
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                   menu()
                                   
                        if event.key == pygame.K_RIGHT:
                            var[0] = True
                        if event.key == pygame.K_LEFT: 
                            var[1] = True 
                            
                                                   
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT:
                            pygame.display.update()
                            var[0] = False
                        if event.key == pygame.K_LEFT:
                            pygame.display.update()
                            var[1] = False
                if var[0]: #inaczj trzeba było klikac 
                    paddle.move_right() 
                if var[1]:
                    paddle.move_left()
                                    
                screen.fill(pygame.Color("yellow"), (0, 0, 900, 30))     
                all.clear(screen, board.background)
                all.update()

                dirty = all.draw(screen)
                pygame.display.update(dirty)
                
                score =round((-start_ticks+pygame.time.get_ticks())/1000)  + score1 + score2 -t
                
                myfont = pygame.font.SysFont(const.font, 45)  
                myfont2 = pygame.font.SysFont(const.font, 25) 
                label = myfont.render("                         Level: " + str(lev+1) + "        Lives: "+str(live)+'       Score: '+ str(score), 1, (0,0,0),board.background)
                label2 = myfont2.render(str(const.POZ[poz]), 1, (0,0,0),board.background)
                
                screen.blit(label, (0,0))
                screen.blit(label2, (0,8))
                pygame.display.flip()
                screen.fill(pygame.Color("black"), (0, 0, 0, 0))    
    
                clock.tick(speed)
            

        while run:
            sound = const.load_sound('lost.wav')
            sound.play()   
            
            all.clear(screen, board.background)
            screen.fill((255,0,0))
            myfont = pygame.font.SysFont(const.font, 85)
            label = myfont.render("Game over :( ", 1, (255,255,255))
            screen.blit(label, (300,300))
            pygame.display.flip()    
            pygame.display.update()
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sound.stop()
                        menu()
    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sound.stop()
                            menu()
                            
        while run2:
            
            if lev == len(levels):
                sound = const.load_sound('win.wav')
                sound.play()
                all.clear(screen, board.background)
                screen.fill((0,255,0))
                myfont = pygame.font.SysFont(const.font, 85)
                label = myfont.render("You win :)", 1, (255,255,255))
                screen.blit(label, (300,300))
                pygame.display.flip()    
                pygame.display.update()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            high_scores_filename = 'high_scores.dat'
                            scores = []
                            if os.path.exists(high_scores_filename):
                                with open(high_scores_filename,'rb') as rfp: 
                                    scores = pickle.load(rfp)
                                                
                            first_name = input("Please enter your name:")
                            scor = score
                                            
                            high_scores = scor, const.POZ[poz] ,first_name
                            scores.append(high_scores)
                                            
                            with open(high_scores_filename,'wb') as wfp:
                                pickle.dump(scores, wfp)
                                
                            sound.stop()
                            menu()
        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                high_scores_filename = 'high_scores.dat'
                                scores = []
                                if os.path.exists(high_scores_filename):
                                    with open(high_scores_filename,'rb') as rfp: 
                                        scores = pickle.load(rfp)
                                                
                                first_name = input("Please enter your name:")
                                scor = score
                                                
                                high_scores = scor,const.POZ[poz], first_name
                                scores.append(high_scores)
                                                
                                with open(high_scores_filename,'wb') as wfp:
                                    pickle.dump(scores, wfp)
                                sound.stop()
                                menu()
                                
                
            else:
                
                all.clear(screen, board.background)
                running=True 
                run2 = False
             
        
    
def menu(): 
    pygame.display.set_caption('Menu')
    menu_items = ['Play','Difficulty','High Score','Exit']
    menu_items2=['Easy', 'Hard']
    filename = os.path.join('photos', const.tlo2)
    tlo = pygame.image.load(filename).convert_alpha()
    screen.blit(tlo,(0,0))
    pygame.display.update()
    run = True 
    run2 = False 
    poz = 0
    while run:
        screen.blit(tlo,(0,0))
        for i in range(len(menu_items)):
            const.make_button(screen,(0,0,0),(255,255,255),const.width/2 -100,const.height/4 + (90*i),menu_items[i]) #puts the item into the make_button, `+20*i` will make each item 15px down from the last.
       
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == 5:
                if event.button == 1:
                    for i in range(len(menu_items)):
                        if const.button_check(event.pos,const.width/2-100,const.height/4 + (90*i),120,60):
                            if i == 0:
                                main(True, poz)
                                
                            elif i == 1:#wybór poziomu trudności
                                run2 = True
                                screen.blit(tlo,(0,0))
                                pygame.display.update()
                                
                                while run2:
                                    for i in range(len(menu_items2)):
                                        const.make_button(screen,(0,0,0),(255,255,255),const.width/2 -80,const.height/3 + (90*i),menu_items2[i]) #puts the item into the make_button, `+20*i` will make each item 15px down from the last.
                                        pygame.display.update()
                                        
                                        for event in pygame.event.get():
                                            if event.type == 5:
                                                if event.button == 1:
                                                    for i in range(len(menu_items2)):#check every button
                                                        if const.button_check(event.pos,const.width/2-80,const.height/3 + (90*i),120,60):
                                                            if i == 0:
                                                                poz = 0
                                                                run2 = False
                                                            
                                                            else:
                                                                poz= 1
                                                                run2 = False
                                                                
                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_ESCAPE: 
                                                    menu()
                                                    
                                        if event.type == pygame.QUIT:
                                            menu()
                            elif i == 2:
                                run3 = True
                                screen.blit(tlo,(0,0))
                                pygame.display.update()
                                high_scores_filename = 'high_scores.dat'
                                myfont = pygame.font.SysFont(const.font, 35)
                                
                                label1 = myfont.render("Rank         Score         Difficulty        Name", 1, (255,255,0))
                                screen.blit(label1, (150,12))

                                if os.path.exists(high_scores_filename):
                                    with open(high_scores_filename,'rb') as rfp:
                                        scores = pickle.load(rfp)
                                    s = sorted(scores)
                                    for i in range(len(s)):
                                        label = myfont.render("   " + str(i+1) + "              " +str(s[i][0]) + "                 " + str(s[i][1]) +"            " + str(s[i][2]), 1, (255,255,255))
                                        screen.blit(label, (150,40+i*25))
                                        
                                while run3:
                                    pygame.display.flip()    
                                    pygame.display.update()
                                    for event in pygame.event.get():
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_ESCAPE: 
                                                menu()

                            elif i == 3:
                                run = False
            
            if event.type == pygame.QUIT:
                run = False
    pygame.display.quit()                         
    pygame.quit()


if __name__ == '__main__': 
    pygame.init()
    menu()