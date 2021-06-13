# Nov 2020, CPE concurrent Python
# Exemple du cours 
# Somme parallèle avec fork d'abord

import os
import multiprocessing as mp # pour Value

def somme(num_process, Val, tableau) :
    print("Je suis le fils num ", num_process, "et je fais la somme du tableau ", tableau )
    S_local=0
    for i in range(len(tableau)) :
        S_local += tableau[i]
    Val.value += S_local
    
    
if __name__ == "__main__" :
    taille = 15
    tableau = [1 for i in range(taille)]
    
    somme_totale = mp.Value('i', 0)
    id_fils = os.fork()
    if not id_fils : # Je suis le fils
        somme(1, somme_totale, tableau[:taille // 2])
    else : # Le père fais l'autre moitié
        somme(0, somme_totale, tableau[taille // 2:])
        os.wait()
        print("La somme totale du tableau est ", somme_totale.value)
"""
TRACE :
Je suis le fils num  0 et je fais la somme du tableau  [1, 1, 1, 1, 1, 1]
Je suis le fils num  1 et je fais la somme du tableau  [1, 1, 1, 1, 1]
La somme totale du tableau est  11
"""