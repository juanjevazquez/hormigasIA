import random


def crea_ficheros():
    for i in range(5):
        outfile = open("prueba"+str(i+1)+".txt", 'w') # Indicamos el valor 'w'.
        for i in range(40):
            outfile.write(str(random.randrange(1,10))+","+str(random.randrange(1,10))+"\n")
        outfile.close()

if __name__ == "__main__":
    crea_ficheros()

