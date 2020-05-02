import sys
import copy

def funcion_objetivo( distancias, ruta ):
    acum = 0
    for k in range(len(ruta)-1):
        acum = acum + distancias[ruta[k]][ruta[k + 1]]
    #rof
    
    return( acum )
#fed

def incersion( orden, distancias):
    solucion = [0, 0]
    verifica = [False]*(len(distancias) - 1)
    
    for k in range(len(orden)):
        minimo = 1000000000000
        print("=========================================================")
        for i in range(1,len(solucion)):
            x = copy.deepcopy( solucion )
            print("----------------------")
            for ref in orden:
                y = copy.deepcopy( x )
                y.insert(i, ref)
                fo = funcion_objetivo( distancias, y)
                print( y, fo)
                if ( fo < minimo and verifica[ref-1] == False ):
                    minimo = fo
                    escogido = ref
                    z = copy.deepcopy( y )
                #fi
            #rof
        #rof
        verifica[escogido-1]  = True
        solucion = copy.deepcopy( z )
        print("=========================================================")
        print( solucion, funcion_objetivo( distancias, solucion ))
    #rof
    return( solucion, funcion_objetivo( distancias, solucion ))
#fed

def principal( argv ):
    distancias = [
        [0, 30, 33, 35, 28, 44, 49, 29, 48, 32, 37, 43, 22, 40, 27, 39, 43, 29, 38],
        [30, 0, 43, 43, 43, 44, 48, 29, 28, 22, 44, 49, 29, 45, 42, 45, 31, 22, 38],
        [33, 43, 0, 45, 47, 30, 50, 45, 40, 33, 21, 30, 38, 32, 40, 39, 32, 35, 43],
        [35, 43, 45, 0, 45, 33, 46, 29, 47, 41, 32, 41, 45, 44, 43, 33, 43, 34, 42],
        [28, 43, 47, 45, 0, 37, 32, 31, 28, 35, 21, 44, 21, 42, 43, 25, 33, 38, 41],
        [44, 44, 30, 33, 37, 0, 44, 32, 31, 32, 29, 21, 21, 41, 29, 35, 42, 20, 43],
        [49, 48, 50, 46, 32, 44, 0, 46, 20, 49, 38, 44, 37, 42, 45, 50, 35, 29, 27],
        [29, 29, 45, 29, 31, 32, 46, 0, 29, 50, 36, 34, 29, 25, 42, 43, 25, 24, 37],
        [48, 28, 40, 47, 28, 31, 20, 29, 0, 38, 38, 26, 32, 43, 47, 31, 28, 30, 35],
        [32, 22, 33, 41, 35, 32, 49, 50, 38, 0, 30, 38, 35, 22, 26, 35, 22, 43, 37],
        [37, 44, 21, 32, 21, 29, 38, 36, 38, 30, 0, 48, 42, 27, 31, 36, 50, 39, 28],
        [43, 49, 30, 41, 44, 21, 44, 34, 26, 38, 48, 0, 33, 49, 37, 40, 28, 49, 32],
        [22, 29, 38, 45, 21, 21, 37, 29, 32, 35, 42, 33, 0, 45, 31, 21, 39, 45, 30],
        [40, 45, 32, 44, 42, 41, 42, 25, 43, 22, 27, 49, 45, 0, 26, 40, 29, 37, 50],
        [27, 42, 40, 43, 43, 29, 45, 42, 47, 26, 31, 37, 31, 26, 0, 47, 46, 38, 36],
        [39, 45, 39, 33, 25, 35, 50, 43, 31, 35, 36, 40, 21, 40, 47, 0, 29, 25, 38],
        [43, 31, 32, 43, 33, 42, 35, 25, 28, 22, 50, 28, 39, 29, 46, 29, 0, 47, 34],
        [29, 22, 35, 34, 38, 20, 29, 24, 30, 43, 39, 49, 45, 37, 38, 25, 47, 0, 20],
        [38, 38, 43, 42, 41, 43, 27, 37, 35, 37, 28, 32, 30, 50, 36, 38, 34, 20, 0]
    ]
    orden = [5, 2, 1, 18, 7, 5, 6, 14, 8, 3]
    ruta, fo = incersion( orden, distancias)
    print(ruta, fo)
#fed


if __name__ == "__main__":
    principal( sys.argv )
#fi