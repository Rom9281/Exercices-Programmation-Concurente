# Sujet pi''

# CPE LYON

# 3 ETI

# 2021

# Groupe D

# Projet process

# Capucine CASTELNEAU | Romain GAUD



import random, time, math   #importation des bibliothéques nécéssaires
import multiprocessing as mp


####### Méthode Mono_Processus #######

def Calcul_Mono_Processus(nb_iterations): #création fonction
    count = 0 #initialisation count
    hits = 0

    for i in range(nb_iterations): #boucle
        x = random.random() #valeur aléatoire de x comprise entre 0 et 1 (coordonnée)
        y = random.random() #valeur aléatoire de y comprise entre 0 et 1 (coordonnée)
        if x*x + y*y <= 1: #vérification de l'appartenance du point généré au cercle unité
            hits += 1 #si c'est le cas, on incrémente le nombre de hits de 1.
    return hits

nb_total_iterations = 10000000 #nombre d'itérations que l'on fait
debut = time.time() #démarrage du chronomètre
nb_hits = Calcul_Mono_Processus(nb_total_iterations) #appel de la fonction 

fin = time.time() #fin du chrono
print ("valeur estimee de PI Mono-Processus : " ,4*nb_hits/nb_total_iterations) #calcul de Pi, en utilisant la méthode du cercle unité donnée en énoncé
ecart_relatif = 100*(4*nb_hits/nb_total_iterations - math.pi)/math.pi #calcul de l'écart-relatif entre la valeur trouvée et la valeur théorique
print("Ecart Relatif : ",abs(ecart_relatif), "%") #affichage de l'écart-relatif
print("Temps de calcul : ", round(fin - debut, 3)*1000, "ms") #affichage du temps de calcul


    