#-------------------------------------------------------------
#On met en place ici 4 process differents pour gerer plus facilement 
#l'ensemble de la matrice : chaque process s'occupe d'un quart de 
#la matrice. 
#Attention, car du coup, il y aura des zones critiques (les frontieres
#entre deux quadrants) à gerer. Il faudra les integrer aux deux 
#processus et faire attention à respecter les conditions pour leur 
#etat (vivant ou mort)  
#-------------------------------------------------------------
#Regles de transition des etats des cellules : 
#soit n le nombre de voisins d'une cellule
    #si n<2 l’état suivant est : Mort
    #si n=2 la cellule ne change pas d’état
    #si n=3 l’état suivant est : Vivant
    #si n>3 l’état suivant est : Mort
#-------------------------------------------------------------

#variables de conditions
#-------------------------------------------------------------
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
        


k=4
nb_process_arrives_RDV=0 #valeur initiale, valeur partagee
verrou=Lock #pour proteger variable partagee nb_process arrives_RDV
tous_la:condition

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
        