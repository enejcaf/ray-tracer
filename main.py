# -*- coding: utf-8 -*-
#/usr/bin/env python3

import pygame
import Buttons #v isti mapi
import raytr2 #v isti mapi
import plot_objects #v isti mapi
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
from numpy import random
import matplotlib.pyplot as plt


GRAY = (150, 150, 150)

#Initialize pygame
pygame.init()
x = 300 * 3
y = 200 * 3
#!!! sliko shrani npr na 600*400, če je potrebno narisati večjo sliko bo poteben tudi večji pygame screen.
#Create a display
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("Ray tracer")

Narisi = Buttons.Button()
Nalozi = Buttons.Button()
valj = Buttons.Button()
krogla = Buttons.Button()
ravnina = Buttons.Button()
stozec = Buttons.Button()
triD = Buttons.Button()
Naslov = Buttons.Button_noalpha()
Button_close = Buttons.Button_noalpha()
Button_save = Buttons.Button_noalpha()


def update_display(img, narisi):
    '''
    Funkcija, ki posodobi prikaz na zaslonu.
    Vhod:
        -img: slika ali int 0.
        -narisi: celo stevilo 0 ali narisi>0.
    Če je narisi večji od nič nariše trenutno sliko na "pygame display" in gumbe iz Buttons.py, drugače izriše sivo kockasto mrežo v velikosti
    slike, če bi jo pogram prejel.
    '''
    screen.fill((255,255,255))
    #Parameteri za gumbe: surface, color, x, y, length, height, width, text, text_color
    x_size, y_size = 100, 50
    Narisi.create_button(screen, (102, 0, 204), (x-2*x_size)//2+300-10, y//2+200+10, x_size, y_size, 0, "Nariši", (255,255,255))
    Nalozi.create_button(screen, (102, 0, 204), x//2-300+10, y//2+200+10, x_size, y_size, 0, "Naloži", (255,255,255))
    Naslov.create_button(screen, (255, 255, 255), 0, 0, 5*x_size, 2*y_size, 0, "Ray tracer", (0, 0, 0))
    valj.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+10, x_size, y_size, 0, "Valj", (255,255,255))
    ravnina.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+20+y_size, x_size, y_size, 0, "Ravnina", (255,255,255))
    krogla.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+30+2*y_size, x_size, y_size, 0, "Krogla", (255,255,255))
    stozec.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+40+3*y_size, x_size, y_size, 0, "Stožec", (255,255,255))
    triD.create_button(screen, (102, 0, 204), (x+x_size//2)//2+300-10, y//2-200+50+4*y_size, x_size, y_size, 0, "3-D shema", (255,255,255))

    if narisi==0:
        block_size = 20
        height, width = 400//20, 600//20
        for b in range(height):
            for a in range(width):
                rect = pygame.Rect((x-600)//2+a*block_size, (y-400)//2+b*block_size, block_size, block_size)
                pygame.draw.rect(screen, GRAY, rect, 1)
    else:
        height, width = 400, 600
        (x_img, y_img) = img.get_rect().size
        img.convert()
        rect = img.get_rect()
        rect.center = x//2, y//2+30
        img = pygame.transform.scale(img, (600, 400))
        screen.blit(img, rect)


    pygame.display.flip()



update_display(0, 0)

'''
Začetne vrednosti spremenljivk, ki se uporabljajo v mainloopu. "butC" in "butS" povesta, če se na zaslonu prikažeta
gumba za close in save, kar se zgodi samo, ko klinkemo gumb "Nariši". Uploaded se uporablja v resnici samo namesto
pogoja os.path.isfile(pot) == True/False, kot vhodni podatek v funkciji update_display. Torej če je uploaded>0, pomeni
os.path.isfile(pot) == True in po na displayu slika trenutne postavitve.
'''

butC=0
butS=0
uploaded=0 #različen od nič, ko damo noter json parametre postavitve

#Glavna zanka programa:
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == MOUSEBUTTONDOWN:

            if Narisi.pressed(pygame.mouse.get_pos()):

                if uploaded>0:
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    gen = raytr2.slika(zaslon[0]['width'], zaslon[0]['height'], 3, kamera[0]['position'], svetila[0], objekti)
                    for i in range(0,zaslon[0]['height']):
                        trenutna=next(gen)
                        if i%10==0 or i==zaslon[0]['height']-1:
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

                    #prikaz slike:
                    img = pygame.image.load('trenutna.png')
                    (x_img, y_img)=img.get_rect().size
                    img.convert()
                    rect = img.get_rect()
                    rect.center = x//2, y//2
                    screen.fill(GRAY)
                    screen.blit(img, rect)


                    #velikost gumbov za shranjevanje in zapiranje: w, h
                    w, h = 40, 20
                    w2, h2 = 100, 20
                    Button_close.create_button(screen, (255,0,0), (x+x_img)//2 - w, (y-y_img)//2, w, h, 0, "x", (255,255,255))
                    Button_save.create_button(screen, (255,0,0), (x+x_img)//2 - w2, (y+y_img)//2-h2, w2, h2, 0, "Save", (255,255,255))

                    pygame.display.update()
                    butC+=1
                    butS+=1

                else:
                    print('Naložena ni bila še nobena datoteka!')

            if Nalozi.pressed(pygame.mouse.get_pos()):
                root = tk.Tk()
                pot = filedialog.askopenfilename()
                root.destroy()

                print('Nalagam: '+pot)

                #naloži file pot/ime.json
                if os.path.isfile(pot) == True:
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    uploaded+=1

                    plot_objects.plot_objects(objekti, kamera[0]['position'], 0)
                    img = pygame.image.load('predogled.png')
                    update_display(img, uploaded)

                else:
                    print('Datoteka na lokaciji '+pot+' ne obstaja.')
                    update_display(0, 0)


            if valj.pressed(pygame.mouse.get_pos()):
                if uploaded>0:
                    #vprašamo po barvi
                    root = tk.Tk()
                    barva=askcolor()[0]
                    root.destroy()

                    #generiramo podatke za valj
                    r_center=np.array(random.rand(3))
                    d=np.array(random.rand(3))
                    r1=random.rand()
                    h=random.rand()

                    #preberemo objekte, dodamo in zapišemo
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    objekti.append({ 'type': 'cylinder', 'center': r_center, 'direction': d, 'height': h, 'radius': r1, 'ambient': np.array(barva)/2550, 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 })
                    print_json(objekti, svetila, kamera, zaslon, pot)

                    #narišemo novo sliko
                    plot_objects.plot_objects(objekti, kamera[0]['position'], 0)
                    img = pygame.image.load('predogled.png')
                    print('Dodajam valj.')
                    update_display(img, uploaded)

                else:
                    print('Niste še naložili datoteke oblike json z začetnimi podatki.')



            if stozec.pressed(pygame.mouse.get_pos()):
                if uploaded>0:
                    #vprašamo po barvi
                    root = tk.Tk()
                    barva=askcolor()[0]
                    root.destroy()

                    #generiramo podatke za stožec
                    r_center=np.array(random.rand(3))
                    d=np.array(random.rand(3))
                    h=random.rand()

                    #preberemo objekte, dodamo in zapišemo
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    objekti.append({ 'type': 'cone', 'center': r_center, 'direction': d, 'height': h, 'ambient': np.array(barva)/2550, 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 })
                    print_json(objekti, svetila, kamera, zaslon, pot)

                    #narišemo novo sliko
                    plot_objects.plot_objects(objekti, kamera[0]['position'], 0)
                    img = pygame.image.load('predogled.png')
                    print('Dodajam stožec.')
                    update_display(img, uploaded)

                else:
                    print('Niste še naložili datoteke oblike json z začetnimi podatki.')


            if ravnina.pressed(pygame.mouse.get_pos()):
                if uploaded>0:
                    #vprašamo po barvi
                    root = tk.Tk()
                    barva=askcolor()[0]
                    root.destroy()

                    #generiramo parametre ravnine
                    r0=np.array(random.rand(3))
                    n0=np.array(random.rand(3))

                    #preberemo objekte, dodamo in zapišemo
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    objekti.append({ 'type': 'plane', 'normal': n0, 'point': r0, 'ambient': np.array(barva)/2550, 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 })
                    print_json(objekti, svetila, kamera, zaslon, pot)

                    #narišemo novo sliko
                    plot_objects.plot_objects(objekti, kamera[0]['position'], 0)
                    img = pygame.image.load('predogled.png')
                    print('Dodajam ravnino.')
                    update_display(img, uploaded)

                else:
                    print('Niste še naložili datoteke oblike json z začetnimi podatki.')


            if krogla.pressed(pygame.mouse.get_pos()):
                if uploaded>0:
                    #Vprašamo po barvi
                    root = tk.Tk()
                    barva = askcolor()[0]
                    root.destroy()

                    #Spremenljivke za kroglo
                    center1=np.array(random.rand(3))
                    r1=random.rand()

                    #preberemo objekte, dodamo in zapišemo
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    objekti.append({'type': 'ball', 'center': center1, 'radius': r1, 'ambient': np.array(barva)/2550, 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5, 'n2': 1.52 })
                    print_json(objekti, svetila, kamera, zaslon, pot)

                    #narišemo novo sliko
                    plot_objects.plot_objects(objekti, kamera[0]['position'], 0)
                    img = pygame.image.load('predogled.png')
                    print('Dodajam kroglo.')
                    update_display(img, uploaded)

                else:
                    print('Niste še naložili datoteke oblike json z začetnimi podatki.')

            if triD.pressed(pygame.mouse.get_pos()):

                if uploaded>0:
                    objekti, svetila, kamera, zaslon = read_json(pot)
                    plot_objects.plot_objects(objekti, kamera[0]['position'], 1)
                    pygame.display.update()

                else:
                    print('Niste še naložili datoteke oblike json z začetnimi podatki.')

            if butC > 0:

                if Button_close.pressed(pygame.mouse.get_pos()):
                    butC -= 1
                    update_display(0,0)

            if butS > 0:

                if Button_save.pressed(pygame.mouse.get_pos()):
                    root = tk.Tk()
                    ime=filedialog.asksaveasfilename(title = "Izberi datoteko", filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
                    root.destroy()
                    pygame.image.save(img, ime)
                    Button_save.create_button(screen, (255,0,0), (x+x_img)//2 - w2, (y+y_img)//2, w2, h2, 0, "Saved", (255,255,255))
                    pygame.display.update()
                    butS -= 1
                    print('Slika shranjena!')
