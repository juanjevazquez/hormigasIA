'''
Created on 9 nov. 2016

@author: jjoli
'''
import random

"""Esta funcion recibe como parametros una lista de tuplas(nodo, probabilidad) y una lista de feromonas

    en cada iteracion, si existe algun nodo en la lista nodos_prob, que pueda seleccionarse,
    se seleccionan tres de ellos aleatorios, y entre esos se escoge al que mayor probabilidad tenga.
    si este nodo puede incluirse, se anade, y se premia el valor de feromona correspondiente
    en el caso de no caber, se penaliza el valor de su feromona.
    Una vez terminado se penalizan las feromonas correspondientes a los nodos no seleccionados
    
    La funcion devuelve un listado de nodos, junto con la lista de feromonas actualizadas.
"""
def lanza_hormiga(nodos_prob, feromonasSalida):
    
    solucion = []
    condicion = True #A modifiar. Esto es para comprobar si el objeto puede seleccionarse
        
    while existe_nodos_posibles(nodos_prob, condicion):
        nodo = selecciona_nodo(nodos_prob, condicion)  
        
        condicion = False #Aqui debe comprobarse si el nodo seleccionado se puede anadir
        if condicion:
            feromonasSalida[nodo[0].indice] = feromonasSalida[nodo[0].indice] * 0.98 # 0.98 valor experimental de penalizacion
        else:
            add_nodo(nodos_prob, solucion, nodo)  
            feromonasSalida[nodo[0].indice] = feromonasSalida[nodo[0].indice] * 1.02  # 1.2 valor experimental para actualizacion de las feromonas
            #Aqui se deben actualizar los valores de cada iteracion. Por ejemplo Peso total y valor total, en el caso de la mochuila
            
    for o in nodos_prob:
        #Penalizamos todos los nodos no elegidos
        feromonasSalida[o[0].indice] = feromonasSalida[o[0].indice] * 0.98
        
    return (solucion, feromonasSalida)

def add_nodo(nodos,solucion,nodo):
        solucion.append(nodo[0])
        nodos.remove(nodo)

"""Esta funcion recibe una lista de tuplas (nodo, probabilidad), y una condicion. Aqui se comprueban si de los nodos que aun no han sido elegidos
hay alguno que pueda cogerse para anadirlo a la solucion.
"""
def existe_nodos_posibles(nodos_prob, condicion):
    result = False
    for o in nodos_prob:
        if condicion:
            result = True
            break
    return result

"""Esta funcion recibe lista de tuplas (nodo, probabilidad) y una condicion, la misma que en existe_nodos_posibles.
Lo que se hace aqui es filtrar todos los nodos sin elegir, por los que aun se pueden elegir segun la condicion
una vez filtrado, se eligen 3 al azar, si hubiera menos de 3 se eligen los que hubiera (1 o 2),
y de estos nodos escogidos al azar, se selecciona el que mayor probabilidad tiene
"""
def selecciona_nodo(nodos_prob, condicion):
    preseleccionados = []
    seleccionados = []
    numb1 = 0
    for o in nodos_prob:
        if condicion:
            preseleccionados.append(o)

    if len(preseleccionados)>=3:    
        numb1 = random.randrange(len(preseleccionados))
        numb2 = random.randrange(len(preseleccionados))
        while(numb2==numb1):
            numb2 = random.randrange(len(preseleccionados))
        numb3 = random.randrange(len(preseleccionados))    
        while(numb3==numb1 or numb3==numb2):
            numb3 = random.randrange(len(preseleccionados))
        seleccionados.append(preseleccionados[numb1])
        seleccionados.append(preseleccionados[numb2])
        seleccionados.append(preseleccionados[numb3])
    elif len(preseleccionados)>=2:
        numb1 = random.randrange(len(preseleccionados))
        numb2 = random.randrange(len(preseleccionados))
        while(numb2==numb1):
            numb2 = random.randrange(len(preseleccionados))
        seleccionados.append(preseleccionados[numb1])
        seleccionados.append(preseleccionados[numb2])
    elif len(preseleccionados)>=1:
        numb1 = random.randrange(len(preseleccionados))
        seleccionados.append(preseleccionados[numb1])

        


"""Esta funcion recibe dos tuplas compuestas por (objeto, probabilidad), en ella se compara cual de esos objetos
tiene mayor su probabilidad
"""
def compara_nodos(x,y):
    if x[1] < y[1] :
        rst = -1
    elif x[1] > y[1] :
        rst = 1
    else :
        rst = 0
    return rst

"""Implementar basandose en compara nodos. Dependiendo del problema las soluciones seran mejor o peor dependiendo de diferentes cosas"""
def compara_soluciones( x, y ) :
    #TODO
    return 0

nodos = [] #Aqui han de meterse los nodos iniciales del problema.

"""Esta funcion recibe un numero de hormigas, y una lista de feromonas.

primero se calculan los valores de probabilidad para cada objeto, y se crea la lista de tuplas (objeto, probabilidad)

despues, se hacen las iteraciones correspondientes al numero de hormigas introducido, actualizandose en cada paso una lista 
de feromonas, que sera, al terminar, la referencaia para la siguiente colonia de hormigas

una vez obtenidas todas las soluciones se devuelve la mejor, junto con la lista de feromonas actualizadas.
"""
def lanza_colonia(numbHormigas, feromonasEntrada):
    soluciones=[]
    lista = []
    nodos_prob = []
    
    #En este caso, para calcular las probabilidades
    for x in range(len(nodos)):
        f = feromonasEntrada[x] * (1.0/nodos[x].peso) * (1-(1.0/nodos[x].valor))
        lista.append(f)
    total = sum(lista)
    #Par calcular los niceles de f, habria que usar otra formula distinta. esta es para el vaso de la mochila
        
    for i in range(len(lista)):
            nodos_prob.append((nodos[i], lista[i]/total)) #Se anade a una lista una tupla con el objeto y la probabilidad
        
    for i in range(numbHormigas):
        objetos2 = [x[:] for x in nodos_prob]
        cosa = lanza_hormiga(objetos2, feromonasEntrada)
        soluciones.append(cosa[0])
        feromonasEntrada = cosa[1]
        
    soluciones.sort(compara_soluciones)
   
    return soluciones[len(soluciones)-1], feromonasEntrada

"""Esta funcion recibe una capacidad, un numero de iteraciones, y un numero de hormigas.

primero se calculan los valores iniciales de las feromonas y se meten en una lista. Una vez hecho esto
se llama a la funcion lanza_colonia tantas veces como numero de iteraciones se quieran hacer.
Para cada colonia que se laza se muestra la mejor solucion obtenida.

"""
def lanza_colonias(numbIteraciones, numbHormigas):
    
    soluciones= []
    feromonasEntrada = [50]*len(nodos) #50 es el valor experimental para el arranque del valor de las feromonas
    
    for i in range(numbIteraciones):
        cosa = lanza_colonia(numbHormigas, feromonasEntrada)
        soluciones.append(cosa[0])
        feromonasEntrada = cosa[1]
        
        print "////////Iteracion" + str(i+1) + "////////"
        print soluciones[i]
        print feromonasEntrada