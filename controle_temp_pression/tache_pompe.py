# MIT DANS LE MAIN : fonction pour le developpement

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
    
    