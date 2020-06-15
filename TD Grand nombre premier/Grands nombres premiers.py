# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:36:15 2019

@author: pierrehb
"""

"""
On rapelle que les operateurs <<n et >>n permettent de decaler les bits d'un nombre de n emplacements
notament <<1 est une multiplication par 2 et >>1 est une ddivision entière par 2.
"""


#1
def puissance_modulaire(a, e, n):
    s=1
    while e > 0:
        s = s*a % n
        e -= 1
    return s

#2
def puissance_modulaire_rapide_1(a, e, n):
    s = 1
    a_power_2 = a
    #cette variable va prendre les valeurs : a, a**2, a**4, a**8...
    while e > 0:
        if e % 2 == 1:s = s*a_power_2 % n
        #si le dernier bit de e est un 1, on multiplie s par la puissance de a correspondante
        a_power_2 = a_power_2*a_power_2 % n
        e //= 2
        #on décale les bits de e vers la droite (une division par 2)
    return s

#On peut remarquer qu'en modifiant certain opérateurs, on peut avoir des opérations moins couteuses et donc un algoritme plus rapide
def puissance_modulaire_rapide_2(a, e, n):
    s = 1
    a_power_2 = a
    while e > 0:
        if e & 1 == 1:s = s*a_power_2 % n# l'operateur & 1 ne conserve que le dernier bit de e
        a_power_2 = a_power_2*a_power_2 % n
        e >>= 1
    return s

#3
"""
(en considerant que la multiplication et le modulo se font en tend constant)
La première méthode a une compléxité de O(e)
alors que la deuxième a une compléxité en O(log(e)),
la deuxième est plus efficasse, d'où son nom.
"""

from random import randint

#4
def entier_aleatoire(taille):
    return randint(0, 1 << taille)

#5
def entier_impair_aleatoire(taille):
    nb = entier_aleatoire(taille)
    if nb % 2 == 0: return nb + 1
    return nb

#6
def est_compose(n, a):
    return puissance_modulaire_rapide_2(a, n-1, n) != 1

#7
def est_potentiellement_premier(n):
    for a in [2, 3, 5, 7]:
        if est_compose(n, a): return False
    return True

#8
def est_compose_2(n, a):
    return a*a % n != 1 #on a suposé a diferent de 1 ou -1 modulo n

#9
def est_potentiellement_premier_2(n):
    a = randint(2, n-1)
    power = 1
    while power < n-1:
        if a == n-1: return True#les carrés suivants ne seront que des 1, on ne poura pas conclure que a est composé...
        if a == 1: return False#le carré précédant n'était ni 1 ni -1, a est composé
        a = a*a % n
        power <<= 1#on multiplie l'éxposant par deux car on a mis a au carré
    return True

#10
def composition_1(n):
    nb = n-1
    s = 0
    while nb % 2 == 0:
        s += 1
        nb //= 2
    return s, nb

#on peut améliorer légerement le temps de calcule en utilisant des opérations moins couteuses:
def composition_2(n):
    nb = n-1
    s = 0
    while nb & 1 == 0:
        s += 1
        nb >>= 1
    return s, nb

#11
def test_miller_rabin(n, a):
    s, d = composition_2(n)
    a = puissance_modulaire_rapide_2(a, d, n)

    if a == 1 or a == n-1: return False

    while s > 0:
        a = a*a % n

        if a == -1: return False
        if a ==  1: return True#l'équation x*x = 1 a une autre solution que 1 et -1

        s -= 1
    return True#le théorème de Fermat n'est pas verifié

#12
def est_premier(n, k = 25):
    if n <= 1:return False#n == 0 ou n == 1
    if n <= 3:return True#n == 2 ou n == 3
    #on traite les cas qui provoqueraient une erreur dans le randint

    for i in range(k):
        a = randint(2, n-1)
        #on supose n très grand, il est alors peu probable de tirer deux fois la même valeur
        #si jamais n est trop petit (n < 29) cela permet de ne pas avoir d'erreur en tirant deux fois le même chiffre
        if test_miller_rabin(n, a): return False
    return True

#13
def random_prime(taille):
    nb = entier_impair_aleatoire(taille)
    while not est_premier(nb):
        nb += 2#on test le prochain nombre impair
    return nb

print(random_prime(512))