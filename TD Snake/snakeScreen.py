# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:14:28 2019

@author: pierrehb
"""
from tkinter import Canvas,Tk,ALL
attente = 200
canvas=Canvas
direction=None
callback=lambda :None

def boucle():#la fonction qui vas s'executé sans arret dans le programme
    canvas.delete(ALL)
    callback()
    windows.after(attente, boucle)

def clavier(event):
    global direction
    if event.keysym== 'Up'  :direction=0
    if event.keysym=='Right':direction=1
    if event.keysym== 'Down':direction=2
    if event.keysym== 'Left':direction=3

def cree_fenetre(ecran):
    global windows
    global canvas
    windows = Tk()#on crée la fenêtre
    windows.title('Snake')
    windows.resizable(False, False)
    canvas=Canvas(width=ecran, height=ecran, background='black')
    canvas.focus_force()
    canvas.bind('<KeyPress>',clavier, True)
    canvas.pack()

def start(fonction, ecran=500):
    global callback
    callback=fonction
    cree_fenetre(ecran)#on crée une fenêtre
    windows.after(attente, boucle)#on lance la boucle infinit
    windows.mainloop()#on affiche la fenêtre