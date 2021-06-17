from multiprocessing import Process, Value, Lock, Pool
import os, time,math, random, sys
from array import array  
import SharedArray as sadef 
import multiprocessing

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-   /!\   DISCLAMER   /!\   -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

"""
Du à sa difficulté,
ce programme n'est pas finit et une certaine partie du code à été prit sur internet!
Nous invitons le professeur à le regarder,  mais à ne pas le compter comme un programme valide
Ni à mettre des points

"""

# -*-*-*-*-*-*-**-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# ___________________________________   FONCTIONS   ____________________________________


def process_cellules_1(): 
    #process qui gere le cadrant haut gauche
    name=multiprocessing.current_process().name
    print ('Lancement cadrant haut gauche',name)
    with cond:#dispense de prendre le verrou
        print("%s:cadrant gauche terminé:les process cadrant suivants peuvent commencer" %name)
        cond.notify_all()

def process_cellules_2(): 
    #process qui gere le cadrant haut droit
    name=multiprocessing.current_process().name
    print('lancement cadrant haut droit',name)
    with cond:
        cond.wait()
        print('%s en cours'%name)

def process_cellules_3():
    #process qui gere le cadrant bas gauche
    name=multiprocessing.current_process().name
    print('Lancement  cadrant bas gauche',name)
    with cond:
        cond.wait()
        print('%s:en cours'%name)
    
def process_cellules_4():
    #process qui gere le cadrant bas droit
    name=multiprocessing.current_process().name
    print('Lancement cadrant bas droit',name)
    with cond:
        cond.wait()
        print('%s:en cours'%name)
        

def travail_chaque_process():
    while True : 
        #traitement 1er process
        RDV()
        #suite traitements

def RDV():
    with verrou:
        nb_process_arrives_RDV +=1
        on_est_combien=nb_process_arrives_RDV
    if on_est_combien==k : #tt le monde arrivé au RDV
        with verrou : #reinitialiser la variable nb_process_arrives_RDV
            nb_process_arrives_RDV=0 #pour le prochain RDV
        #liberer tt le monde sauf l'actuel en attente sur sem
        tous_la.notify_all()
    else:
        tous_la.wait() #on se bloque sur cette condition


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

# _______________________________________   VARIABLES   ______________________________________________


k=4
nb_process_arrives_RDV=0 #valeur initiale, valeur partagee
verrou = multiprocessing.Lock() #pour proteger variable partagee nb_process arrives_RDV
#tous_la:condition


# ___________________________________   DEMARAGE PROGRAMME   ___________________________________



condition=multiprocessing.Condition()

s1=multiprocessing.Process(name='cadrant haut gauche',target=process_cellules_1,args=(condition,))
s2=multiprocessing.Process(name='cadrant haut droit',target=process_cellules_2,args=(condition,)) 
s3=multiprocessing.Process(name='cadrant bas gauche',target=process_cellules_3,args=(condition,)) 
s4=multiprocessing.Process(name='cadrant bas droit',target=process_cellules_4,args=(condition,)) 


s1.start()
s2.start()
s3.start()
s4.start()


s1.join()
s2.join()
s3.join()
s4.join()


