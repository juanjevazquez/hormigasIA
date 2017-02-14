'''
Created on 19 oct. 2016

@author: jjoli
'''
class Objeto(object):
    
    def __init__(self, indice, peso, valor):
        self.indice = indice
        self.peso = peso
        self.valor = valor
    
    def muestra(self):
        print "Objeto "+ str(self.indice) +",   Peso = "+ str(self.peso) + "   Valor = " + str(self.valor) 
    
class Solucion(object):
    
    def __init__(self, objetos, peso_total, valor_total):
        self.objetos = objetos
        self.peso_total = peso_total
        self.valor_total = valor_total
    
    def muestra(self):
        for objeto in self.objetos:
            objeto.muestra()
        print "Peso total = " + str(self.peso_total)   
        print "Valor total = " + str(self.valor_total)
    