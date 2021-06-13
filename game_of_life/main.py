from multiprocessing import Process, Value, Lock, Pool
import os, time,math, random, sys
from array import array  
import SharedArray as sadef 

if __name=='__main__':
    condition=multiprocessing.Condition()
    s1=multiprocessing.Process(name='cadrant haut gauche',target=process_cellules_1,args=(condition,))
    s2=multiprocessing.Process(name='cadrant haut droit',target=process_cellules_2,args=(condition,)) 
    s3=multiprocessing.Process(name='cadrant bas gauche',target=process_cellules_3,args=(condition,)) 
    s4=multiprocessing.Process(name='cadrant bas droit',target=process_cellules_4,args=(condition,)) 
    
    for c in s2:
        c.start()
        time.sleep(1)
    s1.start()

    s1.join()
    for c in s2:
        c.join()

