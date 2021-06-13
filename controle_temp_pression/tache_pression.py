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

        # Relache un jeton pour que l'écran et la pompe puissent faire leur travaux
        sem_ecran.release();sem_pompe.release()