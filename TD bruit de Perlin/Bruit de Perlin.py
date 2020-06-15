# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:40:43 2019

@author: pierrehb
"""

from random import randint
from math import sqrt, pi

#%% Partie I

"1)"
def element_aleatoire(liste):
    i = randint(0, len(liste)-1)
    liste[i], liste[-1] = liste[-1], liste[i]
    return liste.pop()

"2)"
def liste_aleatoire(n):
    liste = list(range(n))
    melange = []
    while len(liste) != 0:
        melange.append(element_aleatoire(liste))
    return melange

"3)"
def vecteur_unitaire():
    diag = sqrt(2) / 2
    return [(0,1), (0,-1), (1,0), (-1,0), (diag, diag), (-diag, diag), (-diag, -diag), (diag, -diag)]

"4)"
def obtenir_vecteur(x, y, vecteurs, entiers):
    m, n = len(vecteurs), len(entiers)
    k = entiers[(y + entiers[x % n]) % n] % m
    return vecteurs[k]

"5)"
def scalaire(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    return x1*x2 + y1*y2

def vecteur(x1, y1, x2, y2):
    return (x2 - x1, y2 - y1)

"6-10)"
def generer_bruit_de_perlin(resolution):
    vecteurs = vecteur_unitaire()
    entiers = liste_aleatoire(256)

    def bruit_de_perlin(x, y):
        x/=resolution
        y/=resolution
        x0 = int(x)
        y0 = int(y)
        x1 = x0 + 1
        y1 = y0 + 1
        X = x - x0
        Y = y - y0
        dx = 3*X*X - 2*X*X*X
        dy = 3*Y*Y - 2*Y*Y*Y

        u1 = obtenir_vecteur(x0, y0, vecteurs, entiers)
        v1 = vecteur (x0, y0, x, y)
        s_x0y0 = scalaire(u1, v1)
        u2 = obtenir_vecteur(x1, y0, vecteurs, entiers)
        v2 = vecteur (x1, y0, x, y)
        s_x1y0 = scalaire(u2, v2)
        u3 = obtenir_vecteur(x0, y1, vecteurs, entiers)
        v3 = vecteur (x0, y1, x, y)
        s_x0y1 = scalaire(u3, v3)
        u4 = obtenir_vecteur(x1, y1, vecteurs, entiers)
        v4 = vecteur (x1, y1, x, y)
        s_x1y1 = scalaire(u4, v4)

        l1 = dx*s_x1y0 + (1-dx)*s_x0y0
        l2 = dx*s_x1y1 + (1-dx)*s_x0y1
        l = dy*l2 + (1-dy)*l1

        return l

    return bruit_de_perlin

#%% Partie II

"11)"
def generer_bruit_de_perlin_2(resolution):
    perlin1 = generer_bruit_de_perlin(resolution)
    perlin2 = generer_bruit_de_perlin(resolution*pi/2)
    def perlin(x, y):
        return (perlin1(x, y) + perlin2(x, y))/2
    return perlin

"12)"
def generer_bruit_de_perlin_3(layers):
    perlins = []
    total = 0
    for resolution, coeficiant in layers:
        total += coeficiant
        perlins.append((generer_bruit_de_perlin(resolution), coeficiant))

    def perlin(x, y):
        result = 0
        for noise, coef in perlins:
            result+= noise(x, y)*coef
        return result/total

    return perlin

#%% Partie III

"13)"
def increment_base(indicateur, base):
    n = len(indicateur)
    i = 0
    for i in range(n):
        indicateur[i]+=1
        if indicateur[i] == base:indicateur[i] = 0
        else:break

"14)"
def coef_null(indicateur):
    total = 0
    for coef in indicateur:
        if coef == 0: total += 1
    return total

def vecteurs_dimension_n(n):
    unit = [sqrt(k)/k for k in range(1,n+1)]
    vectors = []
    indicateur = [1]+[0 for i in range(n-1)]

    for i in range(3**n-1):
        k = coef_null(indicateur)
        coef = unit[n-k-1]
        coefs = [0, coef, -coef]
        vecteur = [coefs[i] for i in indicateur]#indicateur est une list de 0, de 1 et de 2
        vectors.append(vecteur)
        increment_base(indicateur, 3)
    return vectors

"15)"
def obtenir_vecteur_n(p, vecteurs, entiers):
    m, n = len(vecteurs), len(entiers)
    indice = 0
    for x in p:
        indice = (x + entiers[indice]) % n
    k = entiers[indice] % m
    return vecteurs[k]

def scalaire_n(v1, v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def vecteur_n(p1, p2):
    return [p2[i] - p1[i] for i in range(len(p1))]

def generer_bruit_de_perlin_n(resolution, n):
    vecteurs = vecteurs_dimension_n(n)
    entiers = liste_aleatoire(len(vecteurs)*len(vecteurs))

    def bruit_de_perlin(point):
        p  = [x/resolution for x in point]

        p0 = [int(x) for x in p]
        p1 = [x+1 for x in p0]
        p_ = [p0, p1]

        P  = [p[i] - p0[i] for i in range(n)]
        dp = [3*P[i]*P[i] - 2*P[i]*P[i]*P[i] for i in range(n)]

        indicateur = [0 for i in range(n)]
        s = []
        for i in range(2**n):#on calcul tout les produits scalaires
            v = [p_[i][indice] for indice, i in enumerate(indicateur)]#indicateur est une liste de 0 et de 1
            u = vecteur_n(v, p)
            s.append(scalaire_n(u, obtenir_vecteur_n(v, vecteurs, entiers)))
            increment_base(indicateur, 2)
        l = s
        for i in range(n):#on calcul toutes les interpolations
            l = [l[j+1]*dp[i] + l[j]*(1-dp[i]) for j in range(0, len(l), 2)]
        return l[0]

    return bruit_de_perlin