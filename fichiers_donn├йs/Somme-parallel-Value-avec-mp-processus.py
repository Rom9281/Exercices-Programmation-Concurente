# Nov 2020, CPE concurrent Python
# Exemple du cours 
# Somme parallèle avec fork d'abord

import os
import multiprocessing as mp # pour Value et Process

def somme(num_process, Val, tableau) :
    print("Je suis le fils num ", num_process, "et je fais la somme du tableau ", tableau )
    S_local=0
    for i in range(len(tableau)) :
        S_local += tableau[i]
    Val.value += S_local
    
    
if __name__ == "__main__" :
    taille = 15
    tableau = [i for i in range(taille)]
    
    somme_totale = mp.Value('i', 0)
    id_fils = mp.Process(target=somme,args=(1, somme_totale, tableau[:taille // 2],))
    id_fils.start()
    somme(0, somme_totale, tableau[taille // 2:])
    id_fils.join()
    print("La somme totale du tableau (par mp.process) : ", somme_totale.value)
    print("Comparer avec La somme calculée par Python  : ", sum(tableau))
"""
TRACE :
Je suis le fils num  0 et je fais la somme du tableau  [7, 8, 9, 10, 11, 12, 13, 14]
Je suis le fils num  1 et je fais la somme du tableau  [0, 1, 2, 3, 4, 5, 6]
La somme totale du tableau (par mp.process) :  105
Comparer avec La somme calculée par Python  :  105
"""
