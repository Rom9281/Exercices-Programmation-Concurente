# Nov 2020, CPE concurrent Python
# Exemple du cours 
# Somme parallèle avec fork d'abor
# Ici  somme avec "array" + Pipe (pas "Array" mais "array" comme numpy)
"""
Extrait doc Python sur mp.Pipe() :
Note that data in a pipe may become corrupted if two processes (or threads) try to read from or write 
to the same end of the pipe at the same time. Of course there is no risk of corruption from processes 
using different ends of the pipe at the same time.
"""
import array
import os
import multiprocessing as mp # pour Value, Pipe

# La fonction des fils
def somme(num_process, table, debut, fin_exclue, cote_pere_read, cote_fils_write) :
    #print("Je suis le fils num ", num_process, "et je fais la somme du tableau ", tableau[debut: fin_exclue] )
     
    # On enlève print du tableau, il est trop grand
    print("Je suis le fils num ", num_process, "et je fais la somme du tableau de taille ", fin_exclue-debut)
    S_local=0
    for i in range(debut, fin_exclue) :
        S_local += tableau[i]
    
    cote_pere_read.send(S_local) # Non bloquant
    print(f"le fils num {num_process}, envoie par send {S_local}")
    
if __name__ == "__main__" :
    taille = 10**6
    
    # Plus efficace que les listes
    tableau = array.array('i',[i for i in range(taille)])
    #print(tableau[:])
    
    cote_pere_read, cote_fils_write=mp.Pipe()
     
    id_fils1 = mp.Process(target=somme,args=(1, tableau, 0, taille // 2, cote_pere_read, cote_fils_write,))
    id_fils2 = mp.Process(target=somme,args=(2, tableau, taille // 2, taille,cote_pere_read, cote_fils_write,))
    id_fils1.start(); id_fils2.start()

    moitie1=cote_fils_write.recv() # Blocks until there is something to receive.
    moitie2=cote_fils_write.recv()
    # On laisser "join" mais inutile dans ce cas car "recv()" est bloquant et les fils terminent 
    # avec send (non bloquants)
    id_fils1.join(); id_fils2.join()
    print("La somme totale du tableau oobtenue : ", moitie1+moitie2)
    print(f"On vérifie que la somme par Python : {sum(tableau)}")
"""
TRACE :
array('i', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Je suis le fils num  1 et je fais la somme du tableau  array('i', [0, 1, 2, 3, 4])
le fils num 1, envoie par send 10
Je suis le fils num  2 et je fais la somme du tableau  array('i', [5, 6, 7, 8, 9])
le fils num 2, envoie par send 35
La somme totale du tableau oobtenue :  45
On vérifie que la somme par Python : 45
"""
"""
if __name__ == "__main__" :
    taille=11
    arr1 = array.array('i', [1 for i in range(taille)])
    #arr2 = array.array('i', [0] * 10)
    cote_pere_read.send_bytes(arr1)
    count = cote_fils_write.recv_bytes_into(arr2)
    assert count == len(arr1) * arr1.itemsize
    arr2
    #array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
    
    from multiprocessing import Process, Pipe
    
    def f(conn):
        conn.send([42, None, 'hello'])
        conn.close()
    
    if __name__ == '__main__':
        parent_conn, child_conn = Pipe()
        p = Process(target=f, args=(child_conn,))
        p.start()
        print(parent_conn.recv())   
        p.join()
"""
