# CPE 2019-20
# Les codes des exemples pour CPE (Python concurrent)
#===================================================================================
# Ex page 3
#===================================================================================
import multiprocessing as mp

# Incrémentation sans protéger la variable partagée
# NOTE : si variable_partagee est déclarée dans une section "main", on n'aura pas besoin de la passer en paramètre.
# Ici, on la passe en paramètre car la fonction "code_page_3_incrementation" n'est pas une section main.

def count1_on_se_marche_sur_les_pieds(nb_iterations,variable_partagee):
    """ Chacun écrit à son rythme (non protégée)"""
 
    for i in range(nb_iterations): 
        variable_partagee.value += 1

#----------- PARTIE principale (le point d'entrée de cet exemple -------

def code_page_3_incrementation():
    nb_iterations = 5000
    # La variable partagée
    variable_partagee = mp.Value('i',0)  # ce sera un entier initialisé à 0
    print("la valeur de variable_partagee AVANT les incrémentations : ", variable_partagee.value)
    # On crée 2 process
    pid1=mp.Process(target=count1_on_se_marche_sur_les_pieds, args=(nb_iterations,variable_partagee)); pid1.start()
    pid2=mp.Process(target=count1_on_se_marche_sur_les_pieds, args=(nb_iterations,variable_partagee)); pid2.start()
    pid1.join(); pid2.join()

    print("la valeur de variable_partagee APRES les incrémentations %d (attendu %d) "% (variable_partagee.value,nb_iterations*2))
#===================================================================================
# Ex page 4 
#===================================================================================
import multiprocessing as mp

# Incrémentation avec protection de la variable partagée
def count2_on_protege_la_section_critique(nb_iterations,variable_partagee,verrou):
    """ Chacun incrémente dans la section protégée """
    
    for i in range(nb_iterations):
        verrou.acquire()
        variable_partagee.value += 1
        verrou.release()  
         
         
def code_page_4_incrementation_avec_mutex():
    nb_iterations = 5000
    # La variable partagée
    variable_partagee = mp.Value('i',0)  # ce sera un entier
    
    # On recommence avec la version protégée par un verrou
    verrou=mp.Lock()

    print("la valeur de variable_partagee AVANT les incrémentations : ", variable_partagee.value)

    # On crée 2 process
    pid1=mp.Process(target=count2_on_protege_la_section_critique, args=(nb_iterations,variable_partagee,verrou)); pid1.start()
    pid2=mp.Process(target=count2_on_protege_la_section_critique, args=(nb_iterations,variable_partagee,verrou)); pid2.start()
    pid1.join(); pid2.join()
    
    print("la valeur de variable_partagee APRES les incrémentations %d (attendu %d): " % 
          (variable_partagee.value,nb_iterations*2))  
    
#===================================================================================
# Ex page 6
#===================================================================================
import multiprocessing as mp

variable_partagee = mp.Value('i', 0)  # ce sera un entier initialisé à 0
verrou = mp.Semaphore()  # Val init=1


def count2_SC_sem(nb_iterations):
    """ Chacun écrit à son rythme (non protégée)"""
    global variable_partagee
    for i in range(nb_iterations):
        with verrou : 
            variable_partagee.value += 1

def test_SC_protege_par_Sem():
    # if __name__ == '__main__' :
    nb_iterations = 5000

    # La variable partagée : placée hors cette fonction (sinon, la passr en param)
    # variable_partagee = mp.Value('i',0)  # ce sera un entier initialisé à 0

    print("la valeur de variable_partagee AVANT les incrémentations : ",
          variable_partagee.value)
    # On crée 2 process
    pid1 = mp.Process(target=count2_SC_sem, args=(nb_iterations,))
    pid1.start()
    pid2 = mp.Process(target=count2_SC_sem, args=(nb_iterations,))
    pid2.start()
    pid1.join()
    pid2.join()

    print("la valeur de variable_partagee APRES les incrémentations %d (attendu %d) " % (
        variable_partagee.value, nb_iterations * 2))

def code_page_6_incrementation_avec_semaphore():
    test_SC_protege_par_Sem()

#===================================================================================
# Ex page 7
#===================================================================================
import multiprocessing as mp

# Ici, chaque process incrémente la valeur de SA case 
# ATTENTION : l'écriture ci-dessus n'est pas efficace (mais là n'est pas le but !). Cependant on peut écrire écrire : 
# def count3\_on\_travaille\_dans\_un\_array\_VERSION\_PLUS\_RAPIDE(nb\_iterations):

def count3_on_travaille_dans_un_array(nb_iterations,tableau_partage):
    for i in range(1,nb_iterations):
        mon_indice = mp.current_process().pid % 2  # donnera 0 / 1 selon le process
        tableau_partage[mon_indice]+=1  

    var_local_a_moi_tout_seul=0
    for i in range(nb_iterations): var_local_a_moi_tout_seul+=1
    # Et on écrit UNE SEULE FOIS :
    mon_indice = mp.current_process().pid % 2
    tableau_partage[mon_indice]+=1 
#-------------------------- Avec Array -----------------------------
def code_page_7_incrementation_avec_array():
    tableau_partage = mp.Array('i', 2)  # tableau de 2 entiers
    
    # Initialisation des array :
    tableau_partage[0]=0; tableau_partage[1]=0;   # Initialisation de l'arra
    # Ou via
    tableau_partage[:]= [0 for _ in range(2) ] # IL FAUT les [:] sinon, ne marche pas (et tableau_partage devient une liste !)
    
    # ATTENTION : NE PAS INITIALISER comme ceci : tableau_partage= [0 for _ in range(2) ]
    # Cette écriture redéfinira  notre Array comme une liste ! (principe de la prog. fonctionnelle)
    
    # Egalement, sans [:], print dennera le type de l'Array, pas son contenu
    print("le contenu du tableau_partage AVANT les incrémentations : ", tableau_partage[:])
    
    # On crée 2 process
    nb_iterations = 5000
    pid1=mp.Process(target=count3_on_travaille_dans_un_array, args=(nb_iterations,tableau_partage)); pid1.start()
    pid2=mp.Process(target=count3_on_travaille_dans_un_array, args=(nb_iterations,tableau_partage)); pid2.start()
    pid1.join(); pid2.join()
    
    print(tableau_partage[0], " et " , tableau_partage[1])
    print("la somme du tableau partage APRES les incrémentations : %d (doit etre %d)"\
            %(sum(tableau_partage),nb_iterations*2) )
#===================================================================================
# Ex page 14
#===================================================================================
# Juin 2019
# Cours hippique
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagant, ... ...

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

from multiprocessing import Process 
import os, time,math, random, sys, ctypes

LONGEUR_COURSE = 100 # Tout le monde aura la même copie (donc no need to have a 'value')
keep_running=mp.Value(ctypes.c_bool, True)

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !


# La tache d'un cheval
def un_cheval(ma_ligne : int) : # ma_ligne commence à 0
    col=1

    while col < LONGEUR_COURSE and keep_running.value :
        move_to(ma_ligne+1,col)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'>')

        col+=1
        time.sleep(0.1 * random.randint(1,5))

#------------------------------------------------
# La partie principale :
def code_page_14_course_hippique() :
    Nb_process=20
    mes_process = [0 for i in range(Nb_process)]
    

    effacer_ecran()
    curseur_invisible()

    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = Process(target=un_cheval, args= (i,))
        mes_process[i].start()

    move_to(Nb_process+10, 1)
    print("tous lancés")



    for i in range(Nb_process): mes_process[i].join()

    move_to(24, 1)
    curseur_visible()
    print("Fini")
#===================================================================================
# Ex page
#===================================================================================
import random, time

# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()

        # si le point est dans  l'unit circle
        if x * x + y * y <= 1: count += 1
    return count

def code_page_17_Monte_Carlo() :
    # Nombre d'essai pour l'estimation
    nb_total_iteration = 10000000
    
    nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
    
    print("Valeur estimée  Pi par la méthode Mono-Processus : ", 4 * nb_hits / nb_total_iteration)
 
#TRACE :
# Calcul Mono-Processus :  Valeur estimée  Pi par la méthode Mono-Processus : 3.1412604
#===================================================================================
# Ex page 19
#===================================================================================
import math, random
from array import array

def merge(left, right):
    tableau = array('i', [])  # tableau vide qui reçoit les résultats
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))

    tableau += left + right
    return tableau

def merge_sort(Tableau):
    length_Tableau = len(Tableau)
    if length_Tableau <= 1: return Tableau
    mid = length_Tableau // 2
    tab_left = Tableau[0:mid]
    tab_right = Tableau[mid:]
    tab_left = merge_sort(tab_left)
    tab_right = merge_sort(tab_right)
    return merge(tab_left, tab_right)

def version_de_base(N):
    Tab = array('i', [random.randint(0, 2 * N) for _ in range(N)]) 
    print("Avant : ", Tab)
    start=time.time()
    Tab = merge_sort(Tab)
    end=time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")
        


def code_page_19_Merge_sort():
    N=1000
    version_de_base(N)
#===================================================================================
# Ex page 28
#===================================================================================
def calcul_PI_OK_selon_mes_slides_on_evite_use_of_PI_version_sequentielle() :
    L_lg_needle=10 # cm
    D_dist_parquet= 10 # distance entre 2 lattes du parquet
    Nb_iteration=10**6

    def tirage_dans_un_cercle_unitaire_et_sinus_evite_PI() : 
        def tirage_un_point_dans_cercle_unitaire_et_calcul_sinus_theta() :
            while True :
                dx = random.uniform(0,1)
                dy = random.uniform(0,1)
                if dx**2 + dy**2 <= 1 : break
            sinus_theta = dy/(math.sqrt(dx*dx+dy*dy)) 
            return sinus_theta

        nb_hits=0
        for i in range(Nb_iteration) :
            # Theta=random.uniform(0,180) ne marche pas, il faut PI à la place de 180 
            # Mais puisqu'on veut le sinuus(theta), on se passe de theta et on caclcule sinus(theta) à 
            # l'ancienne = (cote_opposé / hypothenuse)
            sinus_theta = tirage_un_point_dans_cercle_unitaire_et_calcul_sinus_theta()
            A=random.uniform(0,D_dist_parquet)
            if A <  L_lg_needle * sinus_theta :
                nb_hits+=1

        return nb_hits

    nb_hits=tirage_dans_un_cercle_unitaire_et_sinus_evite_PI()

    print("nb_hits : ",  nb_hits, " sur ", Nb_iteration , " essais")
    Proba=(nb_hits)/Nb_iteration # +1 pour éviter 0

    print("Pi   serait : ", (2*L_lg_needle)/(D_dist_parquet*Proba))

def code_page_28_Buffon():
    calcul_PI_OK_selon_mes_slides_on_evite_use_of_PI_version_sequentielle()    



#===================================================================================
# Code projet / sujet Image
#===================================================================================
#====
# -*- coding: utf-8 -*-
"""
Split d'une image (Mono-Process)
"""

from PIL import Image # Importation de la librairie d'image PIL
from math import sqrt # Importation de la fonction sqrt de la librairie math
 
image_ = None     # sera chargée dans la partie Mian (ici,  on la 'pré-déclare')
width, height = None,  None # respectivement,  la largeur et la hauteur de l'image 
 
def GetPixel(x, y):  
    global matrice_pixels
    return matrice_pixels[x, y]
    
def PutPixel(x, y, r, g, b): 
    global matrice_pixels    
    matrice_pixels[x, y]= int(r),  int(g),  int(b) # Il faut des ints !
    
def PutRegion(x, y, width, height, triplet_color):
    for i in range(x,   x+width):
        for j in range(y,  y+height):
            PutPixel(i, j, triplet_color[0], triplet_color[1], triplet_color[2])

def Average(corner_x,  corner_y, region_w, region_h):  
    sum_red,  sum_green,  sum_blue = 0, 0, 0    #Initialisation des compteurs   
    area = region_w*region_h       #Calcul de la superficie de la région
    
    for i in range(corner_x,  corner_x+region_w):
        for j in range(corner_y,  corner_y+region_h):
            r, g, b=GetPixel(i, j)# Nous lisons les données r, v, b d'un pixel
            sum_red += r       # somme de chaque composant
            sum_green += g
            sum_blue += b 
    #Normalisation            
    sum_red/=area
    sum_green/=area
    sum_blue/=area

    return(sum_red,  sum_green, sum_blue)   #Retour des valeurs r, g, b moyennes

def Mesures_Std_et_Mu(corner_x,  corner_y,  region_w,  region_h):    
    av_red,  av_blue,  av_green = Average(corner_x, corner_y, region_w, region_h)    
    sum_red2, sum_green2, sum_blue2 = 0.0,  0.0,  0.0

    for i in range(corner_x,  corner_x+region_w):
        for j in range(corner_y,  corner_y+region_h):             
            red, green, blue = GetPixel(i, j)
            sum_red2  += (red**2)
            sum_green2 += (green**2)
            sum_blue2 += (blue**2)

    area=region_w*region_h*1.0
    r, g, b=0, 0, 0 
    r = sqrt(abs(sum_red2 / area - av_red**2))
    g= sqrt(abs(sum_green2 / area - av_green**2))
    b = sqrt(abs(sum_blue2 / area - av_blue**2))
    return ((av_red,  av_blue,  av_green),  (r+b+g)/3.0)

def Decouper_en4(x, y, width, height, threshold_alpha):
    if height*width < 4 :  return   # rien à découper

    #Cas de région uniforme : une couleur uniforme est affectée à la partition 
    color, rm = Mesures_Std_et_Mu(x,  y,  width,  height)
    if rm < threshold_alpha:  #Affectation de la couleur moyenne à la partition      
        PutRegion(x, y, width, height, color)
    else: #Dans le cas contraire,  la partition non-uniforme est coupée en 4 (récursivement)
        Decouper_en4(x, y, width//2, height//2, threshold_alpha)
        Decouper_en4(x + width//2,  y,  width//2,  height//2, threshold_alpha)
        Decouper_en4(x,  y + height//2,  width//2,  height//2, threshold_alpha)
        Decouper_en4(x+width//2,  y+height//2,  width//2, height//2, threshold_alpha)
        
def code_projet_image() :
    # nom_fic_image="Image_Lyon.bmp"
    dir_image="Images"
    nom_fic_image="steve.png"
    nom_fic_in=dir_image+'/'+nom_fic_image
    try : 
        image_ = Image.open(nom_fic_in).convert("RGB") #  nécessaire pour une image "png"
    except :
        print("Problème avec le fichier ",nom_fic_in)
        quit(1)
        
    global matrice_pixels    
    matrice_pixels = image_.load()    # Importation des pixels de l'image
    width, height=image_.size  

    image_.show()   # Montrez l'image originale
    
    Decouper_en4(0, 0, width, height, 15) # tester avec les seuils différents 3,  10,  15,  20,  ...

    image_.show()
   
    # On sauvegarde le résultat
    nom_fic_out=dir_image+'/'+"out_"+nom_fic_image   # On construit le nom de l'image sauvegardée
    image_.save(nom_fic_out)

#=======================
# TOUS les tests

if __name__ == '__main__' :
    # code_page_3_incrementation()
    # code_page_4_incrementation_avec_mutex()
    # code_page_6_incrementation_avec_semaphore()
    # code_page_7_incrementation_avec_array()
    # code_page_14_course_hippique()
    # code_page_17_Monte_Carlo()
    # code_page_19_Merge_sort()
    # code_page_28_Buffon()
    # code_projet_image()