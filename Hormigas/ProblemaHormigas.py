'''
Created on 19 oct. 2016

@author: jjoli

'''
#encoding: utf-8

from Objetos import *
import random
from time import time

"""Este metodo lee de un archivo de texto y devuelve una lista de Objetos"""
def lee_archivo():

    n = raw_input("Introduzca el numero del archivo de conjunto de pruebas:")
        
    #Abrimos el archivo y leemos por lineas
    archivo = open("prueba"+str(n)+".txt")
    contenido = archivo.readlines()
    
    lista = []
    objetos = []
    
    #Cortamos por linea 
    for linea in contenido:
        linea.split(",")
        lista.append(linea.strip("\n"))
    
    #Creamos los objetos y los anadimos a la lista dandole los valores del fichero
    for l in range(len(lista)):
        indice = l
        peso = int(lista[l][0])
        valor = int(lista[l][2])
        
        objetos.append(Objeto(indice, peso, valor))
        
    return objetos
        
"""Esta funcion recibe por paramenotro una lista de tuplas (objeto, probabilidad), una lista de objetos y un objeto
Lo que se hace basicamente es anadir el objeto a la solucion y quitarlo de los posibles seleccionables"""
def add_objeto(objetos,solucion,obj):
        solucion.append(obj[0])
        objetos.remove(obj)

"""Esta funcion recibe dos tuplas compuestas por (objeto, probabilidad), en ella se compara cual de esos objetos
tiene mayor su probabilidad
"""
def compara_objetos( x, y ) :
    
    if x[1] < y[1] :
        rst = -1
    elif x[1] > y[1] :
        rst = 1
    else :
        rst = 0
    return rst

"""Esta funcion recibe dos objetos Solucion. Se comparan dos soluciones, siendo mayor la que cuya diferencia entre valor y peso
sea mayor, es decir, la mas valiosa.
"""
def compara_soluciones( x, y ) :
    if (x.valor_total) < (y.valor_total) :
        rst = -1
    elif (x.valor_total) > (y.valor_total) :
        rst = 1
    else :
        rst = 0
    return rst


"""Esta funcion recibe como parametros capacidad(de la mochila), una lista de tuplas(objeto, probabilidad) y una lista de feromonas

    en cada iteracion, si existe algun objeto en la lista objs_prob, cuyo peso sea menor o igual a al peso restante,
    se seleccionan tres objetos aleatorios, y entre esos se escoge al que mayor probabilidad tenga.
    si este objeto cabe, se anade, y se premia el valor de feromona correspondiente
    en el caso de no caber, se penaliza el valor de su feromona.
    
    La funcion devuelve un objeto solucion, junto con la lista de feromonas actualizadas.
"""
def lanza_hormiga(capacidad, objs_prob, feromonasSalida):
    
    solucion = []
    peso_total = 0
    valor_total = 0
        
    while existe_objetos_que_caben(objs_prob, capacidad, peso_total):
        objeto = selecciona_objeto(objs_prob, capacidad, peso_total)  

        if (peso_total+ objeto[0].peso)> capacidad:
            feromonasSalida[objeto[0].indice] = feromonasSalida[objeto[0].indice] * 0.98 # 0.98 valor experimental de penalizacion
        else:
            add_objeto(objs_prob, solucion, objeto)  
            feromonasSalida[objeto[0].indice] = feromonasSalida[objeto[0].indice] * 1.02  # 1.02 valor experimental para actualizacion de las feromonas
            peso_total = peso_total+objeto[0].peso
            valor_total = valor_total + objeto[0].valor
            
    for o in objs_prob:
        #Penalizamos todos los nodos no elegidos
        feromonasSalida[o[0].indice] = feromonasSalida[o[0].indice] * 0.97
        
    result = Solucion(solucion, peso_total, valor_total)
    return (result, feromonasSalida)

"""Esta funcion recibe lista de tuplas (nodo, probabilidad), capacidad y peso total.
Lo que se hace aqui es filtrar todos los objetos sin elegir, eligiendose como preseleccionados, solo aquellos que caben.
Una vez filtrado, se eligen 3 al azar, si hubiera menos de 3 se eligen los que hubiera (1 o 2),
y de estos nodos escogidos al azar, se selecciona el que mayor probabilidad tiene
"""
def selecciona_objeto(objs_prob, capacidad, peso_total):
    preseleccionados = []
    seleccionados = []
    numb1 = 0
    for o in objs_prob:
        if o[0].peso<=(capacidad-peso_total):
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

        
    seleccionados.sort(compara_objetos)
    result = seleccionados[len(seleccionados)-1]
        
    return result     
        
"""Esta funcion recibe una lista de tuplas (objeto, probabilidad), capacidad y peso total. Aqui se comprueban si de los nodos que aun no han sido elegidos
hay alguno que pueda cogerse para anadirlo a la solucion.
"""
def existe_objetos_que_caben(objs, capacidad, peso_total):
    result = False
    for o in objs:
        if o[0].peso <= (capacidad-peso_total):
            result = True
            break
    return result

"""Esta funcion recibe una capacidad, un numero de hormigas, y una lista de feromonas.

primero se calculan los valores de probabilidad para cada objeto, y se crea la lista de tuplas (objeto, probabilidad)

despues, se hacen las iteraciones correspondientes al numero de hormigas introducido, actualizandose en cada paso una lista 
de feromonas, que sera, al terminar, la referencaia para la siguiente colonia de hormigas

una vez obtenidas todas las soluciones se devuelve la mejor, junto con la lista de feromonas actualizadas.
"""
def lanza_colonia(capacidad, numbHormigas, feromonasEntrada):
    soluciones=[]
    lista = []
    objs_prob = []
    
    for x in range(len(objetos)):
        f = feromonasEntrada[x] * (1.0/objetos[x].peso) * (1-(1.0/objetos[x].valor))
        lista.append(f)
    total = sum(lista)
        
    for i in range(len(lista)):
            objs_prob.append((objetos[i], lista[i]/total)) #Se anade a una lista una tupla con el objeto y la probabilidad
        
    for i in range(numbHormigas):
        objetos2 = [x[:] for x in objs_prob]
        cosa = lanza_hormiga(capacidad, objetos2, feromonasEntrada)
        soluciones.append(cosa[0])
        feromonasEntrada = cosa[1]
        
    soluciones.sort(compara_soluciones)
#    
    return soluciones[len(soluciones)-1], feromonasEntrada

"""Esta funcion recibe una capacidad, un numero de iteraciones, y un numero de hormigas.

primero se calculan los valores iniciales de las feromonas y se meten en una lista. Una vez hecho esto
se llama a la funcion lanza_colonia tantas veces como numero de iteraciones se quieran hacer.
Para cada colonia que se laza se muestra la mejor solucion obtenida.

"""
def lanza_colonias(capacidad, numbIteraciones, numbHormigas):
    
    soluciones= []
    feromonasEntrada = [100]*len(objetos) #50 es el valor experimental para el arranque del valor de las feromonas
    
    for i in range(numbIteraciones):
        cosa = lanza_colonia(capacidad, numbHormigas, feromonasEntrada)
        soluciones.append(cosa[0])
        feromonasEntrada = cosa[1]
        
        print "////////Iteracion" + str(i+1) + "////////"
        print soluciones[i].muestra()
        print feromonasEntrada
        

"""Esta funcion es la principal. En ella se leen los datos por pantalla especificos para la ejecucion, que son
la capacidad, el numero de hormigas por colonia y el numero de iteraciones deseados.

"""
def ejecuta():
    capacidad = raw_input("Introduzca la capacidad deseada: ")
    numbHormigas = raw_input("Introduzca el numero de hormigas por Colonia (mayor que 0. Entre 20 y 100): ")
    numbIteraciones = raw_input("Introduzca el numero de iteraciones (1 o mas): ")
    
    start_time = time()
    lanza_colonias(int(capacidad), int(numbIteraciones), int(numbHormigas))
    elapsed_time = time() - start_time
    print("Tiempo de ejecucuion: %0.10f segundos." % elapsed_time)
    

if __name__=="__main__":
    objetos = lee_archivo()
    ejecuta()