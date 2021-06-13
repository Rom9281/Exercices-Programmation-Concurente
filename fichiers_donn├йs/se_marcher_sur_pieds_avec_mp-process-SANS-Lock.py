# Nov 2020
# Ex SC simple : incrémentations
# Avec mp.Process

import multiprocessing as mp


# Incrémentation avec protection de la variable partagée
def count2_on_protege_la_section_critique(nb_iterations):
    """ Chacun incrémente dans la section protégée """
    
    for i in range(nb_iterations):      
        variable_partagee.value += 1

        
#----------- PARTIE principale (le point d'entrée de cet exemple -------
if __name__ == '__main__' :
    nb_iterations = 5000
    # La variable partagée
    variable_partagee = mp.Value('i',0)  # ce sera un entier
    
    # On recommence avec la version protégée par un verrou
    verrou=mp.Lock()

    print("la valeur de variable_partagee AVANT les incrémentations : ", variable_partagee.value)

    # On crée 2 process
    pid1=mp.Process(target=count2_on_protege_la_section_critique, args=(nb_iterations,)); pid1.start()
    pid2=mp.Process(target=count2_on_protege_la_section_critique, args=(nb_iterations,)); pid2.start()
    pid1.join(); pid2.join()
    
    print("la valeur de variable_partagee APRES les incrémentations %d (attendu %d): " % (variable_partagee.value,nb_iterations*2))
