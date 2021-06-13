# MIT DANS LE MAIN : fonction pour le developpement


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