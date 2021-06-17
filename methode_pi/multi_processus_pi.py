##############      Methode parallele Multi_Processus        ##############
import random, time, math   #importation des bibliothéques nécéssaires
import multiprocessing as mp

# _____________________________________   FONCTIONS   ____________________________________

def Calcul_Pi_Multi_Processus(nb_it, variable_partagee, verrou): #création fonction et ses parametres
    count=0 #initialisation de count
    for i in range(nb_it): #boucle sur le nombre d'iterations
        x = random.random() #valeur aléatoire de x comprise entre 0 et 1 (coordonnée)
        y = random.random() #valeur aléatoire de y comprise entre 0 et 1 (coordonnée)
        if x*x + y*y <= 1: #on verifie si le point créé appartient au cercle unite
            count += 1 #si oui, on incrémente le nombre de count de 1.  
    with verrou:    
        variable_partagee.value+=count

# ___________________________________   VARIABLES   ___________________________________

nombre_processus = 4   #nombre de processus que l'on utilise

variable_partagee = mp.Value("i", 0) #création d'une variable partagée
verrou = mp.Semaphore(1)             #création d'un verrou
iteration_par_processus=int(nb_total_iterations /nb_processus) #énoncé : chaque process effectue N/k iterations
nb_iter = nb_total_iterations-iteration_par_processus*nb_processus  #énoncé  
    
processus = [] 
for p in range(nb_processus): #calcul du nombre d'itérations
    if p == nb_processus-1:
        iteration_par_processus+=nb_iter #nombre d'itération que l'on met dans le calcul multi-processus parallèle
    processus.append(mp.Process(target = Calcul_Pi_Multi_Processus, args = (iteration_par_processus,variable_partagee,verrou))) #création d'un processus qui appelle la fonction

debut = time.time() #démarrage du chronomètre
for p in processus:
    p.start() #Démarrage de chaque processus créé
    print( Calcul_Pi_Multi_Processus(iteration_par_processus,variable_partagee,verrou)) #Dans chaque processus, on appelle notre fonction
    p.join()  #On attend la fin de chaque processus
fin = time.time() #fin du chronomètre

estimation = 2*float(variable_partagee.value)/float(nb_total_iterations) #calcul de Pi, en utilisant la méthode du cercle unité donnée en énoncé
print("Valeur estimee de PI par la methode Multi-Processus_Parallele:" ,estimation) #affichage de pi
ecart_relatif = 100*abs((estimation- math.pi)/math.pi) #calcul de l'écart-relatif
print("Ecart Relatif : ", ecart_relatif, "%") #affichage écart-relatif
print("Temps de calcul : ", round(fin - debut, 3)*1000, "ms") #affichage temps de calcul


