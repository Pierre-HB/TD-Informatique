# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 22:03:48 2019

@author: pierrehb
"""

phrase = "The answer to the ultimate question of life, the universe and everything is 42."
lettres = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890 ,;:.?!"

#I
"""
l'algorithme naïf devra effectuer autant de comparaison qu'il y a de phrase
possible avec 68 caractères et avec moins de 79 lettres.
cela représente:
sum([69**i for i in range(79+1)]) =
18854644412227220464594165446810819883887201867131792944088342529866110690631845421096734844077020525092444972569229811895549444695061823286458800
(Python est une très bonne calculette)
Ce qui est de l'ordre de 10**145

En suposant que les comparaison avec la phrase ne soit qu'une opération, la machine étant capable de faire 1 milliard de comparaison par seconde
Il nous faudrait 10**128 ans pour trouver la phrase, ce qui est plus long que l'age actuelle de l'univers...
"""

from random import random, choice
#II
def cree_population(settings):
    return [[None, [choice(lettres)]] for _ in range(42)]

#III
def muttation_soustracive(individu):
    if len(individu[1]) != 0: individu[1].pop()

#IV
def mutation_additive(individu):
    individu[1].append(choice(lettres))

#V
def mutation_aléatoire(individu, parametres):
    for i in range(len(individu[1])):
        if random() < parametres[0]:individu[1][i] = choice(lettres)

#VI
def mutation(individu, parametres):#
    mutation_aléatoire(individu, parametres)
    if random() < parametres[1]:
        mutation_additive(individu)
    if random() < parametres[2]:
        muttation_soustracive(individu)

#VII
def reproduction(individu1, individu2):
    enfant = [None, []]
    s = individu1[0]+individu2[0]
    m = min(len(individu1[1]), len(individu2[1]))

    for i in range(m):
        if random()*s < individu1[0]:#on fait passer le s de se coté de l'inéquation pour évité une division par 0
            enfant[1].append(individu1[1][i])
        else:
            enfant[1].append(individu2[1][i])
    enfant[1] += individu1[1][m:] + individu2[1][m:]
    return enfant

#VIII
def evaluation(individu):
    p = 0
    for i in range(min(len(phrase), len(individu[1]))):
        if phrase[i] == individu[1][i]: p+=1
    individu[0] = p - 10*abs(len(phrase) - len(individu[1]))

#IX
def selection(population, settings):
    pop=sorted(population)
    newPop=[]
    for i,item in enumerate(pop):
        #on passe le i de l'autre coté de l'inéaquation pour évité une division par 0
        if random()*i>len(population)*settings[3] or i==len(pop)-1:newPop.append(item)
    return newPop

#X
def devine_la_phrase(parametres):
    population = cree_population(parametres)

    for individu in population:
        evaluation(individu)

    survivant = selection(population, parametres)

    generation = 0
    while survivant[-1][0] != len(phrase) and generation <= parametres[5]:
        generation+=1

        nouvellePopulation = []
        for _ in range(parametres[4]):
            nouvellePopulation.append(reproduction(choice(survivant), choice(survivant)))

        for individu in nouvellePopulation:
            mutation(individu, parametres)

        for individu in nouvellePopulation:
            evaluation(individu)

        survivant = selection(nouvellePopulation, parametres)
    return generation, survivant[-1]

#XI
parametres = [0.01, 0.1, 0.1, 0.4, 42, 20000]
generation, meilleurIndividu = devine_la_phrase(parametres)
resultat = ''
for lettre in meilleurIndividu[1]:
    resultat+=lettre
print("l'algoritme a effectué {} génération, testé {} phrase pour finalement obtenir {}".format(generation, generation*parametres[4], resultat))