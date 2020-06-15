# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 10:01:24 2019

@author: pierrehb
"""
from random import randint
# 1
def coordonnees_aleatoire(taille):
    return (randint(0,taille-1), randint(0,taille-1))
# 2
def element_aleatoire(tableau):
    if len(tableau)==0:return
    return tableau[randint(0,len(tableau)-1)]
#3
def serpent(jeu):
    return list(map(lambda x:x[1], jeu[0]))
# 4
def cree_jeu(taille):
    time=0
    snake=[(time,coordonnees_aleatoire(taille))]
    libre=[(x,y) for x in range(taille) for y in range(taille) if (x,y) != snake[0][1]]
    nouriture=element_aleatoire(libre)
    return [snake, nouriture, time, taille]



import snakeScreen as s

# 5
jeu=cree_jeu(5)

def fenetre():
    global jeu
    strategie(jeu)
    pas(jeu)
    for corp in jeu[0]:
        carre(*corp[1], jeu[3])
    carre(*jeu[1], jeu[3], 'lime')
# 6
def carre(x,y, taille, color='white'):
    x1=int((x/taille)*500)
    x2=int(((x+1)/taille)*500)
    y1=int((y/taille)*500)
    y2=int(((y+1)/taille)*500)
    s.canvas.create_rectangle(x1,y1,x2,y2,fill = color)
# 8
def indice_du_max(tab):
    i=0
    for j in range(1,len(tab)):
        if tab[j]>tab[i]:
            i=j
    return i

def indice_du_min(tab):
    i=0
    for j in range(1,len(tab)):
        if tab[j]<tab[i]:
            i=j
    return i
# 9
def supprime_petit(tableau):
    tableau[indice_du_min(tableau)]=tableau[-1]
    tableau.pop()
# 10
def deplacement_permit(jeu, position):
    return (not position in serpent(jeu)) and all(0<=p<jeu[3] for p in position)
# 11
def recommencer():
    global jeu
    jeu=cree_jeu(jeu[3])
    s.direction=None
# 12
def pas(jeu):
    if s.direction == None:return
    jeu[2]+=1
    position=jeu[0][indice_du_max(jeu[0])][1]
    orientation=[(0,-1),(1,0),(0,1),(-1,0)]
    nouvelle_position=(position[0]+orientation[s.direction][0], position[1]+orientation[s.direction][1])
    if deplacement_permit(jeu, nouvelle_position):
        jeu[0].append((jeu[2], nouvelle_position))
        if nouvelle_position==jeu[1]:
            libre=[(x,y) for x in range(jeu[3]) for y in range(jeu[3]) if not (x,y) in serpent(jeu)]
            if len(libre)==0:
                print("Win!")
                recommencer()
            jeu[1]=element_aleatoire(libre)
        else:
            supprime_petit(jeu[0])
    else:
        recommencer()

#POUR ALLER PLUS LOIN===

# 13
"""
Pour gagner il suffit de faire des aller retour de gauche à droite sur l'écran
à chaque fois que le serpent atteint un bord, il monte. (il faut toutefois veillez à garder
les collones à l'extrème droite et gauche afin de pouvoir redescendre).
Le serpent va alors parcourir toute la grille (il mangera donc toujours la nourriture)
sans jamais se toucher.(mais bon... ce n'est pas une strategie très passionante...)
"""
# 14
def convertir_grille(jeu):
    return [[not (x,y) in serpent(jeu) for x in range(jeu[3])] for y in range(jeu[3]) ]
# 15
def voisins(grille, po):
    s=[(0,-1),(1,0),(0,1),(-1,0)]
    steps=[]
    for i in range(4):
        p=(po[0]+s[i][0],po[1]+s[i][1])
        if all(0<=po<len(grille) for po in p) and grille[p[1]][p[0]]:steps.append(p)
    return steps
# 16
def front_voisin(grille, steps):
    front=[]
    for p in steps:
        steps=voisins(grille, p)
        for step in steps:
            grille[step[1]][step[0]]=False
        front+=steps
    return front
# 17
def plus_court_chemin(grille, start, end):
    front=[start]
    time=0
    while len(front)!=0:
        time+=1
        if end in front:
            return time
        front=front_voisin(grille, front)
    return False

# 18
def copie(grille):#Pour copier une liste de liste
    return [[v for v in l] for l in grille]

def element_minimum_aleatoire(m):
    if len([n for n in m if n])==0:return None
    mi=min([n for n in m if n])
    i=[]
    for j in range(len(m)):
        if m[j]==mi:i.append(j)
    if len(i)==0:return None
    return element_aleatoire(i)

def strategie(jeu):
    grille=convertir_grille(jeu)
    position=jeu[0][indice_du_max(jeu[0])][1]
    m=[False]*4
    d=[(0,-1),(1,0),(0,1),(-1,0)]
    for i in range(4):
        step=(position[0]+d[i][0],position[1]+d[i][1])
        if all(0<=p<len(grille) for p in step) and grille[step[1]][step[0]]:
            m[i]=plus_court_chemin(copie(grille), step, jeu[1])
    d=element_minimum_aleatoire(m)
    if d!=None:
        s.direction=element_minimum_aleatoire(m)
    else:
        steps=voisins(grille, position)
        if len(steps)!=0:
            orientation=element_aleatoire(steps)
            if orientation==(position[0],position[1]-1):s.direction=0
            if orientation==(position[0]+1,position[1]):s.direction=1
            if orientation==(position[0],position[1]+1):s.direction=2
            if orientation==(position[0]-1,position[1]):s.direction=3

s.start(fenetre)