from multiprocessing import Process, Value, Lock, Pool
import os, time,math, random, sys
from array import array  
import SharedArray as sadef 

def cree_matrice(): #fct qui gere la creation/l'affichage de la grille et la creation aleatoire des etats de cellules
 """returns a grid of 15x15 values"""
    return np.choice(vals, 15*15, p=[0.2, 0.8]).reshape(N, N)




def merge(left, right):
    tableau = array('i', [])  # tableau vide qui recoit les resultats
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))

    tableau += left + right
    return tableau
