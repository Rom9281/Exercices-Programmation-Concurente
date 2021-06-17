# Sujet centrale de controle pression et température

# CPE LYON

# 3 ETI

# 2021

# Groupe D

# Projet process

# Capucine CASTELNEAU | Romain GAUD



# - - - - - /!\   CODE DU PROFESSEUR /!\  - - - - - - - - 


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

# ____________________   FONCTIONS AFFICHAGE   ________________________

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def erase_current_line():
    print(CLEARELN, end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')

def ecrire_um_message(nom_tache, mess) :
    ligne_messages, col_messages=dict_messages_des_taches[nom_tache]
    move_to(ligne_messages, col_messages) 
    erase_current_line()
    move_to(ligne_messages, col_messages) 
    print("Tache ", nom_tache, " : ", mess)    
    
def placer_le_cadre() :
    effacer_ecran()
    move_to(x_coin_H_G_cadre, y_coin_H_G_cadre) 
    print(ligne_traits)
    for i in range(17) :
        move_to(x_coin_H_G_cadre+i+1, y_coin_H_G_cadre) 
        print(une_ligne_vid_avec_barres)
    move_to(x_coin_B_G_cadre, y_coin_B_G_cadre) 
    print(ligne_traits)    
    
def ecrire_donnees_temp(val_consigne = 21.0, val_actuelle = 0.0):
    move_to(x_coin_H_G_Temperature, y_coin_H_G_Temperature) 
    print("* Température ")
    move_to(x_coin_H_G_Temperature+1, y_coin_H_G_Temperature+3) 
    print("-Consigne : ", round(val_consigne,2))
    move_to(x_coin_H_G_Temperature+2, y_coin_H_G_Temperature+3) 
    print("-Actuel : ", round(val_actuelle,2)   )
    
def ecrire_donnees_pression(val_consigne = 2.0, val_actuelle = 0.0):
    move_to(x_coin_H_G_Pression, y_coin_H_G_Pression)
    print("* Pression ")
    move_to(x_coin_H_G_Pression+1, y_coin_H_G_Pression+3) 
    print("-Consigne : ", val_consigne)
    move_to(x_coin_H_G_Pression+2, y_coin_H_G_Pression+3) 
    print("-Actuel : ", round(val_actuelle,2))       
  
def ecrire_etats_T_P_et_rel_TP(chauffage_is_on=False, pompe_is_on=False) :
    move_to(x_coin_H_G_Chauffage, y_coin_H_G_Chauffage) 
    print("* Etat Chauffage :", "True " if chauffage_is_on else "False") 
    move_to(x_coin_H_G_Pompe, y_coin_H_G_Pompe) 
    print("* Etat Pompe :", "True " if pompe_is_on else "False")   
    move_to(x_coin_H_G_relation_T_P, y_coin_H_G_relation_T_P) 
    print("* Relation T/P :", relation_entre_T_et_P_courte)

# _*_*_*_*_*_*_*_*_*_*_*_*_*_*_   FONCTIONS DE L'équipe   _*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_

# Tache de la temperature
# _______________________

def interruption(signal,frame):
    process_temp.terminate()
    process_press.terminate()
    process_ecran.terminate()
    process_pompe.terminate()
    
    sys.exit(0)

def tache_temperature(val_pression,val_temperature,chauffage_is_on,lock_val_t,lock_val_p,lock_val_chauff_on,sem_ecran,Cste_Alpha):
    """Tache effectué par la temperature"""

    process_actif = True

    while process_actif:
        delta=0.0 
        # Lecture de la Temperature
        lock_val_t.acquire()
        temp = val_temperature.value
        lock_val_t.release()

        # Etablissement du lien T et P    
        pression = (temp + 273.15) * Cste_Alpha

        # Ecriture de la pression
        lock_val_p.acquire()
        val_pression.value = pression
        lock_val_p.release()

        #Lecture de la valeur de chauffage
        lock_val_chauff_on.acquire()
        chauff_on = chauffage_is_on.value
        lock_val_chauff_on.release()


        if (not chauff_on) : # on baisse la température de 0.1 par seconde
            delta = 0.5-random.random()
            if delta > 0 : delta=-0.3            
        else :
            delta=0.2

        # Ecriture dans temperature
        lock_val_t.acquire()
        val_temperature.value += delta
        lock_val_t.release()

        ecrire_um_message("tache_capteur_temperature", "Chauffage allumé" if chauff_on else "Chauffage eteint")
        time.sleep(1)
        # Relache un jeton pour que l'écran puisse faire son travail
        sem_ecran.release() 

# Tache de la Pression
# _______________________

def tache_pression(val_pression,pompe_is_on,lock_val_p,lock_val_pompe_on,sem_ecran,sem_pompe):
    """ Processus gérant l'état de la pression"""
    process_actif = True

    while process_actif:
        # Lecture pour savoir si la pompe est active
        lock_val_pompe_on.acquire()
        pompe_on = pompe_is_on.value
        lock_val_pompe_on.release()

        # Lecture de la valeur de la pression
        lock_val_p.acquire()
        pression = val_pression.value
        lock_val_p.release()


        if (not pompe_on) : # on augmente la température de 10% par unité de temps   
            pression -=1 # KPa
        else :
            pression*=0.1 # On suppose que la pression augmente de 10% par unité de temps. Vol=Cste
        
        # Ecriture de la nouvelle valeur de la pression
        lock_val_p.acquire()
        val_pression.value = pression
        lock_val_p.release()

        time.sleep(1)

        # Relache un jeton pour que l'écran et la pompe puissent faire leur travaux
        sem_ecran.release();sem_pompe.release()

# Tache de l'écran
# _______________________

def tache_ecran(val_pression,val_temperature,chauffage_is_on,pompe_is_on,lock_val_t,lock_val_p,lock_val_chauff_on,lock_val_pompe_on,sem_ecran,Cste_Consigne_Temperature,Cste_Consigne_Pression):
    process_actif = True

    while process_actif:
        # Prend deux jeton pour que l'écran puisse faire son travail
        sem_ecran.acquire();sem_ecran.acquire();   

        # - - COMMENCE TRAVAUX - - 

        # Ecriture des donnés
        # ___________________

        # Lecture de la Temperature
        lock_val_t.acquire()
        temp = val_temperature.value
        lock_val_t.release()

        ecrire_donnees_temp(Cste_Consigne_Temperature, temp)

        # Lecture de la valeur de la pression
        lock_val_p.acquire()
        pression = val_pression.value
        lock_val_p.release()

        ecrire_donnees_pression(Cste_Consigne_Pression, pression)

        # Ecriture pour activer ou non la pompe
        lock_val_pompe_on.acquire()
        pompe_on = pompe_is_on.value
        lock_val_pompe_on.release() 

        #Ecriture de l'activité du chauffage
        lock_val_chauff_on.acquire()
        chauffage_on = chauffage_is_on.value
        lock_val_chauff_on.release()

        ecrire_etats_T_P_et_rel_TP(chauffage_on, pompe_on)

# Tache de la pompe
# _________________

def tache_pompe(val_pression,val_temperature,chauffage_is_on,pompe_is_on,lock_val_t,lock_val_p,lock_val_chauff_on,lock_val_pompe_on,sem_pompe,Cste_Consigne_Temperature,max_temperature_possible,min_temperature_possible,max_pression_possible,min_pression_possible,Cste_Alpha,Cste_Consigne_Pression):
    """ Gere la tache de la pompe """
    process_actif = True

    while process_actif:
        # Recupere un jeton qui lui permet de faire ses réglages
        sem_pompe.acquire()

        # - - COMMENCE TRAVAUX - - 

        # Regalge consigne temperature
        # ____________________________

        # Lecture de la Temperature
        lock_val_t.acquire()
        temp = val_temperature.value
        lock_val_t.release()

        if (Cste_Consigne_Temperature > temp) : chauffage_on=True
            # if ( not value_Chauffage_on) :chauffage_is_on=Truechauffage_is_on=True 
        else : chauffage_on=False # consigne_temperature  <=  val_temperature
            # if (chauffage_is_on) :  chauffage_is_on=Fal"j'teints"se
        
        #Ecriture de l'activité du chauffage
        lock_val_chauff_on.acquire()
        chauffage_is_on.value = chauffage_on
        lock_val_chauff_on.release()

        # Regalge consigne pression
        # ____________________________

        # Lecture de la valeur de la pression
        lock_val_p.acquire()
        pression = val_pression.value
        lock_val_p.release()

        if (Cste_Consigne_Pression > pression) : pompe_on=True
            # if ( not value_Chauffage_on) :chauffage_is_on=Truechauffage_is_on=True
        else : pompe_on=False # consigne_temperature  <=  val_temperature
            # if (chauffage_is_on) :  chauffage_is_on=False  

        # Ecriture pour activer ou non la pompe
        lock_val_pompe_on.acquire()
        pompe_is_on.value = pompe_on
        lock_val_pompe_on.release() 

        # Reglage du chauffage et temperature selon temperature
        # _____________________________________________________
        
        if (temp >= max_temperature_possible) :
            temp = max_temperature_possible
            chauffage_on=False
        if (temp < min_temperature_possible) :
            temp = min_temperature_possible
            chauffage_on=True      
        
        # Ecriture de la Temperature
        lock_val_t.acquire()
        val_temperature.value = temp
        lock_val_t.release()

        #Ecriture de l'activité du chauffage
        lock_val_chauff_on.acquire()
        chauffage_is_on.value = chauffage_on
        lock_val_chauff_on.release()

        # Lien T et P 
        # ___________  
         
        pression = (temp+ 273.15) * Cste_Alpha
        
            
        if (pression >= max_pression_possible) :
            pression = max_pression_possible
            pompe_on=False
        if (pression < min_pression_possible) :
            pression = min_pression_possible
            pompe_on=True  
        
        # Ecriture de la valeur de la pression
        lock_val_p.acquire()
        val_pression.value = pression
        lock_val_p.release()

        # Ecriture pour activer ou non la pompe
        lock_val_pompe_on.acquire()
        pompe_is_on.value = pompe_on
        lock_val_pompe_on.release() 

        # Ecriture du message
        #___________________
    
        ecrire_um_message("tache_controleur_central : Pompe" , " --> j'allume" if pompe_is_on else "--> j'teints")
        ecrire_um_message("tache_controleur_central : Chauffage", " --> j'allume" if chauffage_is_on else "--> j'teints")
    

#_____________________________   CONSTANTES   _________________________________
keep_running=True # Fin de la course ?
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

x_coin_H_G_cadre, y_coin_H_G_cadre= 5, 10
x_coin_B_G_cadre, y_coin_B_G_cadre= 22, 10
x_coin_H_G_Temperature, y_coin_H_G_Temperature= 7, 12
x_coin_H_G_Pression, y_coin_H_G_Pression= 12, 12
x_coin_H_G_Chauffage, y_coin_H_G_Chauffage= 17, 12
x_coin_H_G_Pompe, y_coin_H_G_Pompe= 18, 12
x_coin_H_G_relation_T_P, y_coin_H_G_relation_T_P= 20, 12


# Partie trace et messages :
# 'Nom tache' : [ligne_mess, col_mess]
dict_messages_des_taches={'tache_controleur_central : Pompe' : [25,1], 
                          'tache_controleur_central : Chauffage' : [26,1],
                          'tache_capteur_temperature' : [26,1]
                          #'tache_capteur_pression' : [27,1],
                          #'tache_screen' :[28,1]
                          }

ligne_prompt_systeme, col_prompt_systeme= 30,1
relation_entre_T_et_P_courte="P.V = n.8,3.T"
relation_entre_T_et_P_longue="Pression_en_Pa * Volume_en_m3 = nb_molécules * 8.31441 * Temp_en_C"
# avec R = 8,31441 [J/mol.K ] , T en [K] , V en [m3] , p en [Pa], n en [mol]

nb_traits=35
ligne_traits="-"*nb_traits
une_ligne_vid_avec_barres="|"+(" "*(nb_traits-2))+"|"

# Les constantes 
max_temperature_possible=40.0
min_temperature_possible=-10.0
max_pression_possible=200.0
min_pression_possible=50.0 

Temp_init=18.0
Pression_init=10.0
chauffage_init_on=False
Pompe_init_on=False
Cste_Consigne_Temperature=22.0
Cste_Consigne_Pression=117.0

Cste_Alpha=0.345642         # 0.02 # On a P = T * Alpha et T=P/alpha



# _____________________   LANCEMENT DU PROGRAMME _________________________

    
if __name__ == "__main__" :
    global chauffage_is_on, val_temperature, pompe_is_on, val_pression

    # Initialisation
    # ______________
    placer_le_cadre()
    ecrire_donnees_temp()
    ecrire_donnees_pression()
    ecrire_etats_T_P_et_rel_TP()
    liste_process=[]

    curseur_invisible()

    # - - - - - - - - - - - - - -  CODE ELEVE - - - - - - - - - - - - - -
    # Definition du signal d'interruption
    signal.signal(signal.SIGINT,interruption) 

    # Variables de multiprocessing
    #_____________________________
    # Variables Partagés
    val_temperature = mp.Value("f",Temp_init)
    val_pression = mp.Value("f",Pression_init)
    chauffage_is_on = mp.Value("b",chauffage_init_on)
    pompe_is_on = mp.Value("b",Pompe_init_on)

    # Locks
    lock_val_t = mp.Lock()
    lock_val_p = mp.Lock()
    lock_val_chauff_on = mp.Lock()
    lock_val_pompe_on = mp.Lock()

    # Semaphores
    sem_ecran = mp.Semaphore(0)
    sem_pompe = mp.Semaphore(0)

    # Process
    process_temp = mp.Process(target = tache_temperature, args = (val_pression,val_temperature,chauffage_is_on,lock_val_t,lock_val_p,lock_val_chauff_on,sem_ecran,Cste_Alpha))
    process_press = mp.Process(target = tache_pression, args = (val_pression,pompe_is_on,lock_val_p,lock_val_pompe_on,sem_ecran,sem_pompe))
    process_ecran= mp.Process(target = tache_ecran, args = (val_pression,val_temperature,chauffage_is_on,pompe_is_on,lock_val_t,lock_val_p,lock_val_chauff_on,lock_val_pompe_on,sem_ecran,Cste_Consigne_Temperature,Cste_Consigne_Pression))
    process_pompe = mp.Process(target = tache_pompe, args = (val_pression,val_temperature,chauffage_is_on,pompe_is_on,lock_val_t,lock_val_p,lock_val_chauff_on,lock_val_pompe_on,sem_pompe,Cste_Consigne_Temperature,max_temperature_possible,min_temperature_possible,max_pression_possible,min_pression_possible,Cste_Alpha,Cste_Consigne_Pression))

    process_temp.start()
    process_ecran.start()
    process_pompe.start()
    process_press.start()

    process_temp.join()
    process_ecran.join()
    process_pompe.join()
    process_press.join()


    # /!\  Code en TRAVAUX
    # ____________________
    """

    tache_ecran() # Première appel pour la mise en place des affichages
    while True : 
        tache_temperature()
        tache_pression
        tache_pompe()
        tache_ecran()

        try : time.sleep(1)
        except : 
            os.system("tset;reset") 
            raise SystemExit('On sort')
    """

    curseur_visible()
    




