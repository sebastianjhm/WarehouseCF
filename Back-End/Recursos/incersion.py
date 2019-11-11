import sys
import random
import copy

def aleatorio( inf, sup ):
    result = int( inf + ( sup - inf + 1 ) * random.random() )
    return( result )
#fed
    
def inicializar_matriz():
    mat  = []
    for i in range(10):
        y = []
        for j in range(10):
            if ( i != j ):
                y.append( aleatorio( 20, 50) )
            else:
                y.append(0)
            #fi
        #rof
        mat.append(y)
    #rof
    return( mat, 9)
#fed

def funcion_objetivo( distancias, sol ):
    acum = 0
    for k in range(len(sol)-1):
        acum = acum + distancias[sol[k]][sol[k + 1]]
    #rof
    
    return( acum )
#fed
    
def incersion(distancias, n_nodos):
    sol = [0]*(n_nodos + 2)
    verifica = [0]*(n_nodos)
    i = 0
    sol[i] = 0
    sol[i+2] = 0
    
    minimo = 1000000
    for j in range(1,n_nodos + 1):
        sol[1] = j
        fo = funcion_objetivo(distancias, sol)
        if ( fo < minimo):
            minimo = fo
            nodo_escogido = j
        #fi
    #rof
    

    verifica[nodo_escogido - 1] = 1
    
    pos = 1
    for i in range(2,n_nodos + 1):
        ## Opcion 1
        min1 = 1000000
        for j in range(1,n_nodos + 1):
            sol[pos] = nodo_escogido
            sol[pos + 1] = j
            fo1 = funcion_objetivo(distancias, sol)
            if ( fo1 < min1 and verifica[j-1] != 1 ):
                min1 = fo1
                nodo_escogido1 = copy.copy(j)
                solucion_f1 = copy.deepcopy(sol)
            #fi
        #fi
        
        
        ## Opcion 2
        min2 = 1000000
        for j in range(1,n_nodos + 1):
            sol[pos] = j
            sol[pos + 1] = nodo_escogido
            fo2 = funcion_objetivo(distancias, sol)
            if ( fo2 < min2 and verifica[j-1] != 1 ):
                min2 = fo2
                nodo_escogido2 = copy.copy(j)
                solucion_f2 = copy.deepcopy(sol)
            #fi
        #fi
        
        
        ## --------------------------------------------------------------
        sol = [0]*(n_nodos + 2)
        if (i <= n_nodos - 1):
            if ( min1 <= min2 ):
                for p in range(pos + 1):
                    sol[p] = solucion_f1[p]
                #rof
                for p in range(pos + 2, i + 2):
                    sol[p + 1]= solucion_f1[p]
                #rof
                nodo_escogido = copy.copy(nodo_escogido1)
                verifica[nodo_escogido - 1] = 1
                pos = pos + 1
            #fi
        
            if ( min2 < min1 ):
                for p in range(0, pos):
                    sol[p] = solucion_f2[p]
                #rof
                for p in range(pos + 1, i + 2):
                    sol[p + 1] = solucion_f2[p]
                #rof
                nodo_escogido = copy.copy(nodo_escogido2)
                verifica[nodo_escogido - 1] = 1
                pos = pos
            #fi
        else:
            if( min1 <= min2):
                for p in range(i + 2):
                    sol[p] = solucion_f1[p]
                #rof
            else:
                for p in range(i + 2):
                    sol[p] = solucion_f2[p]
                #rof
            #fi
        #fi
    #rof
    
    solucion = sol
    fo_final = funcion_objetivo(distancias, sol)
    return(solucion, fo_final)
#fed

def principal( argv ):
    
    # distancias, n_nodos = inicializar_matriz()
    distancias = [
        [0, 51, 30, 27, 44, 25, 42],
        [28, 0, 31, 35, 47, 20, 31],
        [29, 22, 0, 48, 36, 23, 38],
        [21, 44, 43, 0, 38, 26, 31],
        [46, 31, 40, 45, 0, 21, 34],
        [38, 38, 24, 26, 45, 0, 22],
        [32, 32, 29, 39, 27, 21, 0]
    ]
    
    ## Solo hay que llamar la función incersion mandandole una matriz y el número de nodos sin incluir el inicial
    ## La funcion devuelve el recorrido y la fo del recorrido
    solucion, fo_incersion = incersion(distancias, 6)
    print("Ruta: ", solucion)
    print("FO: ", fo_incersion)
    
#fed


if __name__ == "__main__":
    principal( sys.argv )
#fi