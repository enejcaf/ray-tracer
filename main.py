# -*- coding: utf-8 -*-
#/usr/bin/env python3

import pygame
import Buttons #v isti mapi
import raytr #v isti mapi
from pygame.locals import *
import numpy as np
import os.path
from math import floor
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from print_on_json import print_json, read_json #mora bit v isti mapi
import matplotlib.pyplot as plt
from numpy import random

root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')
#root.withdraw()


GRAY = (150, 150, 150)
#Initialize pygame
pygame.init()
x=300*3
y=200*3
#!!! vedno shrani sliko še na ta size 600*400
#Create a display
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("Ray tracer")

Narisi = Buttons.Button()
Nalozi = Buttons.Button()
luc = Buttons.Button()
krogla = Buttons.Button()
ravnina = Buttons.Button()
Naslov= Buttons.Button_noalpha()
Button_close= Buttons.Button_noalpha()
Button_save=Buttons.Button_noalpha()
#Update the display and show the button
def update_display():
    screen.fill((255,255,255))
    #Parameters: surface, color, x, y, length, height, width, text, text_color
    x_size, y_size = 100, 50
    Narisi.create_button(screen, (102, 0, 204), (x-2*x_size)//2+300-10, y//2+200+10, x_size, y_size, 0, "Nariši", (255,255,255))
    Nalozi.create_button(screen, (102, 0, 204), x//2-300+10, y//2+200+10, x_size, y_size, 0, "Naloži", (255,255,255))
    Naslov.create_button(screen, (255, 255, 255), 0, 0, 5*x_size, 2*y_size, 0, "Ray tracer", (0, 0, 0))
    luc.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+10, x_size, y_size, 0, "Žarnica", (255,255,255))
    ravnina.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+20+y_size, x_size, y_size, 0, "Ravnina", (255,255,255))
    krogla.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+30+2*y_size, x_size, y_size, 0, "Krogla", (255,255,255))
    block_size = 20
    height, width = 400//20, 600//20
    for b in range(height):
        for a in range(width):
            rect = pygame.Rect((x-600)//2+a*block_size, (y-400)//2+b*block_size, block_size, block_size)
            pygame.draw.rect(screen, GRAY, rect, 1)
    pygame.display.flip()


#Run the loop
update_display()

butC=0
butS=0
uploaded=0 #različen od nič, ko damo noter json parametre postavitve

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            if Narisi.pressed(pygame.mouse.get_pos()):
                #img = pygame.image.load('image.png')
                if uploaded>0:
                    gen=raytr.slika(zaslon[0]['width'],zaslon[0]['height'],3, kamera[0]['position'], svetila[0], objekti)
                    for i in range(0,y):
                        trenutna=next(gen)
                        if i%10==0 or i==y-1:
                            plt.imsave('trenutna.png', trenutna)
                            #trenutna2=Image.fromarray(trenutna, "RGB")
                            img = pygame.image.load('trenutna.png')

                            (x_img, y_img)=img.get_rect().size
                            img.convert()
                            rect = img.get_rect()
                            rect.center = x//2, y//2
                            screen.fill(GRAY)
                            screen.blit(img, rect)
                            pygame.display.update()

                    img = pygame.image.load('trenutna.png')

                    (x_img, y_img)=img.get_rect().size
                    img.convert()
                    rect = img.get_rect()
                    rect.center = x//2, y//2
                    screen.fill(GRAY)
                    screen.blit(img, rect)
                    #button size: w, h

                    w, h = 40, 20
                    w2, h2=100,20
                    Button_close.create_button(screen, (255,0,0), (x+x_img)//2 - w, (y-y_img)//2, w, h, 0, "x", (255,255,255))
                    Button_save.create_button(screen, (255,0,0), (x+x_img)//2 - w2, (y+y_img)//2-h2, w2, h2, 0, "Save", (255,255,255))
                    pygame.display.update()
                    butC+=1
                    butS+=1
                else:
                    print('Naložena ni bila še nobena datoteka!')

            if Nalozi.pressed(pygame.mouse.get_pos()):
                pot = filedialog.askopenfilename()
                print('Nalagam: '+pot)

                #potrebno je pametno skaliranje slike tlorisa
                #naloži file pot/ime.json
                if os.path.isfile(pot) == True:
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    uploaded+=1
                    for i in objekti:
                        if i['radius'] < 5:
                            pygame.draw.circle(screen, (floor(2550*i['ambient'][0]), floor(2550*i['ambient'][1]), floor(2550*i['ambient'][2])),((300*i['center'][0])//5+450, (200*i['center'][2])//5+300), 200*i['radius']//5, width=0)
                    for i in svetila:
                        pygame.draw.circle(screen, (floor(255*i['ambient'][0]), floor(255*i['ambient'][1]), floor(255*i['ambient'][2])), ((300*i['position'][0])//5+450, (200*i['position'][2])//5+300), 20, width=0)
                        pygame.draw.circle(screen, GRAY, ((300*i['position'][0])//5+450, (200*i['position'][2])//5+300), 20, width=1)
                    for i in kamera:
                        rect = pygame.Rect((300*i['position'][0])//5+450, (200*i['position'][2])//5+300, 10, 10)
                        pygame.draw.rect(screen, (0,0,0), rect)
                    pygame.display.update()
                else:
                    print('Datoteka na lokaciji '+pot+' ne obstaja.')
                    update_display()
                    break
                root.mainloop()
            '''
            if luc.pressed(pygame.mouse.get_pos()):
                barva=askcolor((255, 255, 0))[0]
                root.mainloop()

                #pygame.display.update()


            if ravnina.pressed(pygame.mouse.get_pos()):
                barva=askcolor((255, 255, 0))[0]
                root.mainloop()
                #barva[0]
                #pygame.display.update()
            '''
            if krogla.pressed(pygame.mouse.get_pos()):
                if uploaded>0:
                    barva=askcolor((255, 255, 0))[0]
                    center_x=random.rand(2)
                    center_y=random.rand(2)
                    center_z=random.rand(1)
                    r1=random.rand(1)

                    pygame.draw.circle(screen, barva,(300*center_x//5+450, (200*center_y)//5+300), 200*r1//5, width=0)

                    objekti, svetila, kamera, zaslon = read_json(pot)
                    objekti.append({ 'center': np.array([center_x, center_y, center_z]), 'radius': r1, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 })
                    print_json(objekti, svetila, kamera, zaslon, pot)
                    pygame.display.update()
                else:
                    print('Niste še naložili datoteke oblike json z začetnimi podatki.')
                    
                root.mainloop()

            if butC > 0:
                if Button_close.pressed(pygame.mouse.get_pos()):
                    butC-=1
                    update_display()
            if butS > 0:
                if Button_save.pressed(pygame.mouse.get_pos()):
                    ime=filedialog.asksaveasfilename(title = "Select file", filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
                    pygame.image.save(img, ime)
                    Button_save.create_button(screen, (255,0,0), (x+x_img)//2 - w2, (y+y_img)//2, w2, h2, 0, "Saved", (255,255,255))
                    pygame.display.update()
                    butS-=1
                    print('Image saved!')
                    root.mainloop()
