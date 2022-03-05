# -*- coding: utf-8 -*-
import random
from multiprocessing import Array
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore

NPROD = random.randint(2,10)
NCONS = 1
N = [random.randint(3,10) for i in range(NPROD)]

def menor(lista): 
    # Obtiene el menor valor entre los valores de los consumidores
    minimo = max(lista) + 1
    for i in range(len(lista)):
        if lista[i] < minimo and lista[i] != -1:
            minimo = lista[i]
            index = i     
    return minimo, index

def productor(lista, buffer, index, lim):
     v = 0
     for k in range(lim):
         v += random.randint(0,5)
         print('Productor:', index, 'Iteracion:', k, 'Valor:', v)
         lista[2*index].acquire() # wait empty
         buffer[index] = v
         lista[2*index+1].release() # signal nonEmpty
     v = -1
     lista[2*index].acquire() # wait empty
     buffer[index] = v
     lista[2*index+1].release() # signal nonEmpty

def consumidor(lista, buffer):  
    numeros = []
    for i in range(NPROD):
        lista[2*i+1].acquire() # wait nonEmpty
    while [-1]*NPROD != list(buffer):
        v, index = menor(buffer) 
        print('Anyade:', v, 'de Prod', index)
        numeros.append(v)
        print (f"Numeros: {numeros}")
        lista[2*index].release() # signal empty
        lista[2*index + 1].acquire() # wait nonEmpty
    print ('Valor final de la lista:', numeros)
    
def main():
     print(N)
     buffer = Array('i', NPROD)
     lista_sem = []
     for i in range(NPROD):
         lista_sem.append(BoundedSemaphore(1))# empty valdria Lock()
         lista_sem.append(Semaphore(0)) # nonEmpty para poder hacer un signal primero
     lp = []#lista procesos
     for index in range(NPROD):
         lp.append(Process(target=productor, args=(lista_sem, buffer, index, N[index])))
     lp.append(Process(target=consumidor, args=(lista_sem, buffer)))    
     for p in lp:
         p.start()
     for p in lp:
         p.join()

if __name__ == "__main__":
 main()    
           

        