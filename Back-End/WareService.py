from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
import openpyxl
from openpyxl.utils import get_column_letter
import xlsxwriter
import pyomo.environ as pyo
import copy
from pyomo.opt import SolverFactory
import pyutilib.subprocess.GlobalData
from Rutas import Rutas

## Librería para que pyomo corra dentro de Flask
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

app = Flask(__name__)
cors = CORS(app)




@app.route('/postFile', methods=['POST'])
@cross_origin()
def post():
    
    ## GUARDAR ARCHIVO EXCEL QUE LLEGA DEL SERVICIO
    receivedFile = request.files["myExcelFile"]
    
    
    ## LECTURA DE DATOS OPENPYXL
    param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia = lecturaDatos( receivedFile )
    
    
    ## DECLARAR SOLVER 'GLPK', CREAR UN MODELO ABSTRACTO PYOMO, DECLAR MODELO LINEAL
    opt = SolverFactory('glpk')
    model = pyo.AbstractModel()
    declararModeloLineal( model, param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia )
    
    
    ## CREAR UN INSTANCIA DEL MODELO, RESOLVERLA, IMPRIMIR RESULTADOS POR CONSOLA
    instance = model.create_instance()
    results = opt.solve(instance, timelimit = 2)
    #instance.display()
    imprimirResultadosConsola( instance )
    
    ## GUARDAR JSON RUTAS
    Rutas["distanciaTotal"] = 0
    Rutas["ruta"] = []
    guardarRutas( instance )
    
    
    ## CREAR ARCHIVO EXCEL E IMPRIMIR RESULTADOS CON 'XLSXWRITER'
    ## Crear libro y añadir un hoja
    workbook = xlsxwriter.Workbook('Resultados.xlsx')
    imprimirResultadosXLSX( workbook, instance )
    
    
    return send_file('Resultados.xlsx', as_attachment=True)

#fed
    




@app.route('/rutas', methods = ['GET'])
@cross_origin()
def getRutas():
    print("ahi los estoy mandando")
    return jsonify(Rutas)
#fed
    





################################################################################################################
def imprimirResultadosConsola( instance ):
    print("\n\n")
    print("SOLUCIÓN DEL EJERCICIO")
    print("--------------------------")
    print("\n")
    print("Distancia Total: ",pyo.value(instance.FO))
    print("\n")
    for o in instance.O:
        print("--------- Orden ",o,"----------")
        print("Distancia Recorrida: ",instance.Dist_ORD[o].value)
        print("Ruta: ")
        for i in instance.ORDENES[o]:
            for j in instance.ORDENES[o]:
                if ( instance.x[o,i,j].value == 1):
                    print("Del nodo ",i," al nodo",j)
                #fi
            #rof
        #rof
    #rof
#fed
    
def guardarRutas( instance ):
    
    nueva_ruta = {"id":0, "distanciaRuta": 0, "recorrido": []}
    Rutas["distanciaTotal"] = pyo.value(instance.FO)
    
    for o in instance.O:
        nr = copy.deepcopy( nueva_ruta )
        nr["id"] = o
        nr["distanciaRuta"] = instance.Dist_ORD[o].value
        for i in instance.ORDENES[o]:
            for j in instance.ORDENES[o]:
                if ( instance.x[o,i,j].value == 1):
                    r = [i, j]
                    nr["recorrido"].append(r)
                #fi
            #rof
        #rof
        Rutas["ruta"].append(nr)
    #rof
    print(Rutas)
#fed
########################################################################################################    
    
    
    
########################################################################################################  
def lecturaDatos( receivedFile ):
    ## --------------------- LEER ARCHIVO EXCEL CON OPENPYXL -----------------------------------

    
    ## Abrir el archivo y guardar en la variable archivo
    archivo = openpyxl.load_workbook(receivedFile, data_only = True)

    ## Leer las hojas del archivo, Seleccionar la primera hoja y la columna D
    sheets = archivo.sheetnames
    sheetDatos = archivo[sheets[0]]

    ## NODOS (param_Nodos)
    param_Nodos = []
    column = sheetDatos['A']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            param_Nodos.append(column[x].value)
        #fi
    #rof

    ## Ordenes (param_Ordenes)
    param_Ords = []
    column = sheetDatos['B']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            param_Ords.append(column[x].value)
        #fi
    #rof


    ## Referencias (param_Referencias)
    param_Referencias = []
    column = sheetDatos['C']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            param_Referencias.append(column[x].value)
        #fi
    #rof

    ## Ubicación de cada referencia (param_NOD_REF)
    lect = []
    column = sheetDatos['F']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            lect.append(column[x].value)
        #fi
    #rof
    param_NOD_REF = dict(zip(param_Referencias, lect))


    ## Ordenes y Variable auxiliar (param_ORDENES y param_R)
    lect = []
    for i in range(len(param_Ords)):
        column = sheetDatos[get_column_letter( 8 + i )]
        orden = []
        for x in range(len(column)): 
            if (type(column[x].value) != str and column[x].value != None):
                orden.append(column[x].value)
            #fi
        #rof
        lect.append(orden)
    #rof
    param_Ordenes = dict(zip(param_Ords, lect))

    lectR = copy.deepcopy(lect) ## Esto es demencial
    for x in lectR:
        x.remove(0)
    #rof
    param_R = dict(zip(param_Ords, lectR))


    ## Distancia
    param_Distancia = []
    sheetDistancias = archivo[sheets[1]]
    for i in  range(sheetDistancias.min_row + 1,sheetDistancias.max_row + 1):
        y = []
        for j in range(sheetDistancias.min_column + 1, sheetDistancias.max_column + 1):
            y.append(sheetDistancias.cell(row = i, column = j).value)
        #rof
        param_Distancia.append(y)
    #rof
    ## -------------------------------------------------------------------------------
    
    return( param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia )
#fed
######################################################################################################################################    
    

######################################################################################################################################
def declararModeloLineal( model, param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia ):
    

    ## Conjuntos ------------------------------------------------------------------------
    model.NODOS = pyo.Set( initialize = param_Nodos )
    model.O = pyo.Set( initialize = param_Ords )
    model.REF = pyo.Set( initialize = param_Referencias )
    def setORDENES(model, i):
        return(list(param_Ordenes[i]))
    #fed
    model.ORDENES = pyo.Set(model.O, initialize = setORDENES)
    def setR(model, i):
        return(list(param_R[i]))
    #fed
    model.R = pyo.Set(model.O, initialize = param_R)



    def junte(model):
        return((o,i,j) for o in model.O for i in model.ORDENES[o] for j in model.ORDENES[o] )
    #fed
    model.OROR = pyo.Set(dimen =3, initialize = junte )

    def junte2(model):
        return((o,i) for o in model.O for i in model.ORDENES[o] )
    #fed
    model.OX = pyo.Set(dimen = 2, initialize = junte2 )

    def junte3(model):
        return((o,i,j) for o in model.O for i in model.R[o] for j in model.R[o] )
    #fed
    model.ORR = pyo.Set(dimen = 3, initialize = junte3 )

    def junte4(model):
        return((o,i) for o in model.O for i in model.R[o] )
    #fed
    model.OR  = pyo.Set(dimen = 2, initialize = junte4 )


    ## Parámetros -------------------------------------------------------------------------------
    def paramDistancia(model, i, j):
        return(param_Distancia[i][j])
    #fed
    model.Distancia = pyo.Param(model.NODOS,model.NODOS, initialize = paramDistancia)
    
    def paramNodRef(model, i):
        return(param_NOD_REF[i])
    #fed
    model.Nod_Ref = pyo.Param(model.REF, initialize = paramNodRef) 

    def dinit(model, i ,j):
        return model.Distancia[model.Nod_Ref[i],model.Nod_Ref[j]]
    #fed
    model.Distancia_R = pyo.Param(model.REF, model.REF, initialize = dinit, mutable = True)

    ## Variables ---------------------------------------------------------------------------------
    model.x = pyo.Var(model.OROR, domain = pyo.Binary)
    model.aux = pyo.Var(model.OR)
    model.Dist_ORD = pyo.Var(model.O)


    ## Función Objetivo ---------------------------------------------------------------------------------
    def ObjFunc(model):
        return sum(model.Distancia_R[i,j]*model.x[o,i,j] for o in model.O for i in model.ORDENES[o] for j in model.ORDENES[o])
    #fed
    model.FO = pyo.Objective(rule = ObjFunc)


    ## Restricciones ---------------------------------------------------------------------------------
    def r1(model, o, i):
        return sum( model.x[o,i,j] for j in model.ORDENES[o]) == 1
    #fed
    model.r1 = pyo.Constraint( model.OX, rule = r1 )

    def r2(model, o, j):
        return sum( model.x[o,i,j] for i in model.ORDENES[o]) == 1
    #fed
    model.r2 = pyo.Constraint( model.OX,  rule = r2 )

    def r3(model, o, i):
        return model.x[o,i,i] == 0
    #fed
    model.r3 = pyo.Constraint( model.OX,  rule = r3 )

    def r4(model, o, i, j):
        if ( i != j ):
            return model.aux[o,i] - model.aux[o,j] + len(model.R[o])*model.x[o,i,j] <= len(model.R[o]) - 1 
        return pyo.Constraint.Skip
    #fed
    model.r4 = pyo.Constraint( model.ORR,  rule = r4 )

    def r5(model, o):
        return model.Dist_ORD[o] == sum( model.x[o,i,j]*model.Distancia_R[i,j] for i in model.ORDENES[o] for j in model.ORDENES[o] )
    #fed
    model.r5 = pyo.Constraint( model.O, rule = r5)
#fed
########################################################################################################
    
    
    
    
    
########################################################################################################
def imprimirResultadosXLSX( workbook, instance ):
    ## --------------------- GUARDAR LOS RESULTADOS EN ARCHIVO EXCEL -----------------------------

    ## Formatos
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter'})
    cell_format = workbook.add_format({'align': 'center'})
        
    ## Crear hoja
    worksheet = workbook.add_worksheet('Resultados')
    worksheet.set_column(0, 0, 20)

    #worksheet.merge_range('A1:D1', "SOLUCIÓN DEL EJERCICIO", merge_format)
    worksheet.merge_range(0, 0, 0, 3, "SOLUCIÓN DEL EJERCICIO", merge_format)

    worksheet.write(1, 0, "Distancia Total: ", merge_format)
    worksheet.write(1, 1, pyo.value(instance.FO), cell_format)

    row=3
    col=0
    for o in instance.O:
        worksheet.merge_range(row, col, row, 3, "Orden "+ str(o), merge_format)
        row += 1

        worksheet.write(row, col,"Distancia Recorrida: ", cell_format)
        worksheet.write(row, col + 1,instance.Dist_ORD[o].value, cell_format)
        row += 1
        
        worksheet.write(row, col,"Ruta: ", cell_format)
        row += 1
        
        for i in instance.ORDENES[o]:
            for j in instance.ORDENES[o]:
                if ( instance.x[o,i,j].value == 1):
                    worksheet.write(row, col + 0,"Del nodo ", cell_format)
                    worksheet.write(row, col + 1,i, cell_format)
                    worksheet.write(row, col + 2," al nodo", cell_format)
                    worksheet.write(row, col + 3,j, cell_format)
                #fi
            #rof
            row += 1
        #rof
        row += 1
    #rof
        
        
    # Hay que incluir workbook.close()
    workbook.close()
    ##  -------------------------------------------------------------------------------------
#fed
########################################################################################################
    
    
    
if __name__ == '__main__':
    app.run(debug = False, port=5000)
#fi
