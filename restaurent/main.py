# Sujet restaurent


# - - - - - /!\   CODE DU PROFESSEUR ISSUS DE CTRL PRESSION TEMPERATURE  /!\  - - - - - - - - 


#______________________   COULEURS   _____________________________

# VT100 : Couleurs
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"         

CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                  #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné

#__________________________   IMPORTS   __________________________________

# SYSTEME
# _______

from multiprocessing import process
import os, time,math, random, sys, signal
from array import array  # Attention : différent des 'Array' des Process
import multiprocessing as mp
import ctypes

# ____________________   FONCTIONS AFFICHAGE   ________________________

def effacer_ecran(): print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def erase_current_line():
    print(CLEARELN, end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def ecrire_un_message(message,ligne,colonne) :
    move_to(ligne,colonne) 
    erase_current_line()
    print(message) 


# _*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_**_*_   FONCTIONS DE LEQUIPE   _*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_

def s_value_to_lol(s_value):
    """ On transforme un str de la forme a,a;b,b;c,c;d,d en [[a,a],[b,b],..."""
    ret = []

    # On split une premiere fois
    liste = s_value.split(";")

    #On split chaque sous element
    for element in liste:
        ret.append(element.split(","))
    
    return ret

def lol_to_s_value(lol):
    """ On transforme [[a,a],[b,b],... en un str de la forme a,a;b,b;c,c;d,d"""
    ret = ""
    liste = []
    
    for element in lol:
        liste.append(",".join(element))
    
    ret = ";".join(liste)
    
    return ret 

def tache_client(menu,periode_commande,queue_attentes,lock_queue,sem_tache):
    tache_active = True
    numero_commande = 0

    while tache_active:
        numero_commande += 1
        commande = random.randint(1,len(menu)-1)

        # Ajout du de la commande dans la file
        lock_queue.acquire()
        queue_attentes.put([numero_commande,commande])
        lock_queue.release()

        # Permet a un serveur de recupere une commande
        sem_tache.release()

        # Attente 
        time.sleep(periode_commande)
  

def tache_serveur(i,queue_attentes,lock_queue,liste_action_serveur,lock_action_serveur,sem_tache,periode_prepa,lock_phrase_servi,phrase_servi):
    tache_active = True

    while tache_active:
        # Demande l'acces a une commande
        sem_tache.acquire()

        # Essaye de recuperer une commande
        # Tache sous la forme (numero, plat)
        lock_queue.acquire()
        tache = queue_attentes.get()
        lock_queue.release()

        # Dit au major d'homme qu'il a une commande
        # _________________________________________

        # prend controle de la liste des commandes en cours
        lock_action_serveur.acquire()

        # Remplace son ancienne tache par sa nouvelle tache en cours qu'il declare au major d'homme
        liste_action_serveur[2*i] = tache[0]
        liste_action_serveur[2*i+1] = tache[1]

        lock_action_serveur.release()

        # Effectue la tache
        # _________________
        time.sleep(periode_prepa)

        # Dire la tache effectué
        #_______________________
        lock_phrase_servi.acquire()
        phrase_servi[0] = i
        phrase_servi[1] = tache[0]
        phrase_servi[2] = tache[1]
        lock_phrase_servi.release()
        # Dit au major d'homme qu'il est en attente
        # _________________________________________

        # prend controle de la liste des commandes en cours
        lock_action_serveur.acquire()

        # Annonce au major d'homme qu'il ne fait rien
        liste_action_serveur[2*i] = 0
        liste_action_serveur[2*i+1] = 0

        lock_action_serveur.release()

def tache_major_dhomme(queue_attentes,lock_queue,liste_etat_server,lock_action_serveur,nb_proc,menu,phrase_servi,lock_phrase_servi,flag):
    tache_active = True

    # Liste temporaire des elements de la queue
    liste_elements = []

    # Boucle active
    while tache_active:
        # Affichage de la queue
        # _____________________

        # Ouverture de la queue
        lock_queue.acquire()

        # Recupere tout les elements de la queue
        while not (queue_attentes.empty()):
            element_queue = queue_attentes.get()
            liste_elements.append([str(element_queue[0]),str(element_queue[1])])
        
        # Formatage pour l'impression
        liste_elements_str = [",".join(x) for x in liste_elements]

        # Les imprimes
        ligne = 1
        
        if liste_elements != []:
            ecrire_un_message("Liste des commandes en attentes : "+("|".join(liste_elements_str)),ligne,0)
            flag = False
        if flag:
            ecrire_un_message("Liste des commandes en attentes : Vide",ligne,0)

        # Les remets
        while liste_elements != []:
            # Met le premier element de la liste dans le queue
            queue_attentes.put([int(liste_elements[0][0]),int(liste_elements[0][1])])
            # Enleve le premier element
            liste_elements.pop(0)
        
        # Repermet d'acceder a la queue
        lock_queue.release()
        
        # Affichage des etats des differents process des serveurs
        # _______________________________________________________
        ligne += 1

        # Monopolise l'acces aux etats des serveurs
        lock_action_serveur.acquire()
        
        for k in range(nb_proc):
            ligne += 1
            num_com = liste_action_serveur[2*k]
            com = liste_action_serveur[2*k+1]
            if (num_com == 0) or (com == 0):
                ecrire_un_message("Le serveur (%s) est en attente"%(k+1,),ligne,0)
            else:
                ecrire_un_message("Le serveur (%s) traite la commande (%s|%s)"%(k+1,num_com,menu[com]),ligne,0)

        # On relache le jeton pour que d'autres accedent à la liste
        lock_action_serveur.release()

        # Affiche le plat servi
        lock_phrase_servi.acquire()
        ligne += 2
        num_menu = phrase_servi[2]
        ecrire_un_message("Le serveur  (%s) à finit la commande (%s|%s)"%(phrase_servi[0],phrase_servi[1],menu[num_menu]),ligne,0)
        lock_phrase_servi.release()



        
#  - - - - - - - - - - - - - - - Effacer l'ecran  - - - - -- - - -- - - -- - - - - - - -
effacer_ecran()
# ________________________________   VARIABLES   ______________________________________

# Majour d'hommme
# _______________
flag = True

# Du Processus Serveurs
# __________________

# Nombre de processus représentant le nombre de serveurs
nb_proc = 8


# Du Processus Clients
# __________________

# Periode de commande
periode_commande = 1

# Ce qu'il y a sur le menu
menu = [False,"Nouilles","Hot-Dog","Biere","Plateau_charcuterie","Vin rouge","Sushi","Pankakes"]


# La queue de commande en attentes et son lock
# ____________________________________________

queue_attentes = mp.Queue()
lock_queue = mp.Lock()

# Tache des serveurs en cours
# ___________________________

lock_action_serveur = mp.Lock()
liste_action_serveur = mp.Array('i',nb_proc*2)
# actionserveur[case_à tirer]

# Semaphores qui permet au serveur de commencer une tache
sem_tache = mp.Semaphore(0)

# Plat servi
# __________
periode_prepa = 7

# Value du plat servi
lock_phrase_servi = mp.Lock()
phrase_servi = mp.Array('i',3)

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*--*-*-*-*-* PROCESSUS -*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-
curseur_invisible()
# Processus Serveur
process_client = mp.Process(target=tache_client,args=(menu,periode_commande,queue_attentes,lock_queue,sem_tache))

# Processus major d'homme
processus_major_dhomme =  mp.Process(target=tache_major_dhomme,args=(queue_attentes,lock_queue,liste_action_serveur,lock_action_serveur,nb_proc,menu,phrase_servi,lock_phrase_servi,flag))

# Création des process des serveurs
liste_process_server = []

for i in range(nb_proc):
    liste_process_server.append(mp.Process(target=tache_serveur,args=(i,queue_attentes,lock_queue,liste_action_serveur,lock_action_serveur,sem_tache,periode_prepa,lock_phrase_servi,phrase_servi)))

# ________________________________________ Demarage process ______________________________
processus_major_dhomme.start()
process_client.start()
for process in liste_process_server:
    process.start()

processus_major_dhomme.join()
process_client.join()
for process in liste_process_server:
    process.join()


curseur_visible()

