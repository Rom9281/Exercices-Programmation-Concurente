# MIT DANS LE MAIN : fonction pour le developpement

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
        
        # Relache un jeton pour que l'écran puisse faire son travail
        sem_ecran.release()      
      