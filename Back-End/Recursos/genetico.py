import sys
import random
import numpy as np
import copy
import math

class Individuo:
    def __init__(self, fo = None, ruta = None, probabilidad = None):
        self.fo = fo
        self.ruta = ruta
        self.probabilidad = probabilidad
    #fed
    def __str__(self):
        return "{fo: %s, ruta: %s, probabilidad: %s}"% (self.fo, self.ruta, self.probabilidad)
    #fed
#ssalc


def aleatorio( inf, sup ):
    result = int( inf + ( sup - inf + 1 ) * random.random() )
    return( result )
#fed
    
def inicializar_matriz( nodos ):
    mat  = []
    for i in range( nodos ):
        y = []
        for j in range( nodos ):
            if ( i != j ):
                y.append( aleatorio( 20, 1000) )
            else:
                y.append(0)
            #fi
        #rof
        mat.append(y)
    #rof
    return( mat )
#fed
    
def funcion_objetivo( distancias, ruta ):
    acum = 0
    for k in range(len(ruta)-1):
        x = ruta[k] - 1
        y = ruta[k+1] - 1
        acum = acum + distancias[x][y]
    #rof
    return( acum )
#fed
    
def poblacion_inicial( num_soluciones, nodos, distancias ):
    pob = []
    indiv = {"fo": 0, "ruta": []}
    for i in range(num_soluciones):
        verifica = [False for i in range(nodos)]
        sol = []
        #ind = copy.deepcopy(indiv)
        for j in range(nodos):
            x = aleatorio(1, nodos)
            while( verifica[x-1] == True ):
                x = aleatorio(1, nodos)
            #elihw
            sol.append(x)
            verifica[x-1] = True
        #rof
        #ind["fo"] = copy.deepcopy(funcion_objetivo( distancias, sol))
        #ind["ruta"] = copy.deepcopy(sol)
        ind = Individuo(funcion_objetivo( distancias, sol), sol)
        pob.append(ind)
    #rof
    
    return(pob)
#fed
    
def asignacion_probabilidades( poblacion ):
    
    ## Ordenar poblacion de menor a mayor
    for i in range(len(poblacion)):
        for j in range(len(poblacion)):
            if ( poblacion[i].fo <= poblacion[j].fo ):
                aux = poblacion[i]
                poblacion[i] = poblacion[j]
                poblacion[j] = aux
            #fi
        #rof
    #rof
    
    ## Sumatorias de las funciones objetivo
    suma_fo = 0
    for i in range(len(poblacion)):
        suma_fo = suma_fo + poblacion[i].fo
    #rof
    
    ## Probabilidades contextuales
    probabilidades = []
    for i in range(len(poblacion)):
        #x = poblacion[len(poblacion) - i - 1].fo/suma_fo
        x  = ( 1 - (poblacion[i].fo/suma_fo) ) * ( 1/( len(poblacion) - 1 ) )
        probabilidades.append(x)
    #rof
    
    print(probabilidades)
    
    ## Probabilidad acumulada
    prob_acum = 0
    for i in range(len(poblacion)):
        prob_acum = prob_acum + probabilidades[i]
        poblacion[i].probabilidad = prob_acum
    #rof
    
    return( poblacion )
#fed
    
def escoger_individuos( poblacion ):
    lanzamiento = random.random()
    print(lanzamiento)
    for i in range(len(poblacion)):
        if ( i == 0 ):
            if ( lanzamiento <= poblacion[i].probabilidad ):
                indice_1 = i
            #fi
        elif ( i == len(poblacion) - 1):
            if ( lanzamiento >= poblacion[i-1].probabilidad ):
                indice_1 = i
            #fi
        else:
            if ( lanzamiento > poblacion[i-1].probabilidad and lanzamiento <= poblacion[i].probabilidad ):
                indice_1 = i
            #fi
        #fi
    #rof
    print(indice_1)
    
    indice_2 = copy.copy(indice_1)
    while( indice_2 == indice_1 ):
        lanzamiento = random.random()
        print(lanzamiento)
        for i in range(len(poblacion)):
            if ( i == 0 ):
                if ( lanzamiento <= poblacion[i].probabilidad ):
                    indice_2 = i
                #fi
            elif ( i == len(poblacion) - 1):
                if ( lanzamiento > poblacion[i-1].probabilidad ):
                    indice_2 = i
                #fi
            else:
                if ( lanzamiento > poblacion[i-1].probabilidad and lanzamiento <= poblacion[i].probabilidad ):
                    indice_2 = i
                #fi
            #fi
        #rof
    #elihw
    print(indice_2)
    
    return(indice_1, indice_2)
#fed
    
def cruze( poblacion, ind_1, ind_2, corte, nodos ):
    gen1 = []
    for i in range(corte):
        gen1.append(poblacion[ind_1].ruta[i])
    #rof
    
    gen2 = []
    posiciones = []
    for i in range(corte, nodos):
        gen2.append(poblacion[ind_1].ruta[i])
        for j in range(nodos):
            if (poblacion[ind_1].ruta[i] == poblacion[ind_2].ruta[j]):
                posiciones.append(j)
            #fi
        #rof
    #rof
    
    for i in range(len(posiciones)):
        for j in range(len(posiciones)):
            if ( posiciones[i] <= posiciones[j] ):
                aux = posiciones[i]
                posiciones[i] = posiciones[j]
                posiciones[j] = aux
                
                aux = gen2[i]
                gen2[i] = gen2[j]
                gen2[j] = aux
            #fi
        #rof
    #rof
    
    nuevo_individuo = gen1
    nuevo_individuo = nuevo_individuo + gen2
    print("----------------")
    print(nuevo_individuo)
    
    return(nuevo_individuo)
#fed
    
def insertar_individuo( poblacion, ind ):
    if ( ind.fo > poblacion[len(poblacion)-1].fo ):
        print("es peor")
    else:
        for i in range(len(poblacion)):
            if ( i == 0 ):
                if ( ind.fo <= poblacion[i].fo ):
                    indice = i
                #fi
            else:
                if ( ind.fo > poblacion[i-1].fo and ind.fo <= poblacion[i].fo ):
                    indice = i
                #fi
            #fi
        #rof
        poblacion.insert(indice, ind)
        print(*poblacion)
        poblacion.pop(-1)
        print("-------------------")
        print(*poblacion)
    #fi
    
    return(poblacion)
#fed
    
def principal( argv ):
    
    ## Parámetros
    num_soluciones = 10
    nodos = 10
    
    ## Matriz de distancias
    distancias = inicializar_matriz( nodos )
    print(np.array(distancias))
    
    ## Población inicial
    poblacion = poblacion_inicial( num_soluciones, nodos, distancias )
    print(*poblacion)
    
    ## Asignacion de probabilidades y ordenar
    poblacion = asignacion_probabilidades( poblacion )
    k = copy.copy(poblacion[0].fo)
    
    for iteracion in range(100):
        
        print("-------------- Iteración ", iteracion, "------------------")
    
        ## Obtener padres
        indice_1, indice_2 = escoger_individuos( poblacion )
        
        ## Cruze de dos individuos
        corte = math.ceil( nodos/2 )
        nuevo_individuo = cruze( poblacion, indice_1, indice_2, corte, nodos )
        
        print(funcion_objetivo( distancias, nuevo_individuo))
        print("--------------------")
        ## Insertar 
        ind = Individuo(funcion_objetivo( distancias, nuevo_individuo), nuevo_individuo)
        poblacion = insertar_individuo( poblacion, ind )
        
        ## Asignacion de probabilidades y ordenar
        poblacion = asignacion_probabilidades( poblacion )
        
    #rof
    print("--------------------")
    print(k)
    
#fed1

if __name__ == "__main__":
    principal( sys.argv )
#fi