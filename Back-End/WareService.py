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
def post_picking():
    
    ## SAVE EXCEL FILE THAT ARRIVE OF THE FRONT
    receivedFile = request.files["myExcelFile"]
    
    
    ## READ DATA OPENPYXL
    param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia = read_data_XLSX( receivedFile )
    
    
    ## DECLARE SOLVER 'GLPK', CREATE A PYOMO ABSTRACT MODEL, DECLARE LINEAR MODEL
    opt = SolverFactory('cplex', executable="C:\\Program Files\\IBM\\ILOG\\CPLEX_Studio128\\cplex\\bin\\x64_win64\\cplex")
    #opt = SolverFactory('glpk')
    model = pyo.AbstractModel()
    create_lineal_model( model, param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia )
    
    
    ## CREATE AN INSTANCE OF THE MODEL, SOLVE, PRINT RESULTS BY CONSOLE
    instance = model.create_instance()
    opt.options['timelimit'] = 2
    results = opt.solve(instance, tee=False)
    #instance.display()
    
    ## PRINT RESULTS IN CONSOLE
    print_results_in_console( instance )
    
    ## SAVE JSON ROUTES
    Rutas["distanciaTotal"] = 0
    Rutas["ruta"] = []
    save_routes( instance )
    
    
    ## CREATE EXCEL FILE AND PRINT RESULTS WITH 'XLSXWRITER'
    workbook = xlsxwriter.Workbook('Resultados.xlsx')
    print_results_XLSX( workbook, instance )
    
    
    return send_file('Resultados.xlsx', as_attachment=True)

#fed
    




@app.route('/rutas', methods = ['GET'])
@cross_origin()
def get_routes_picking():
    return jsonify(Rutas)
#fed
    





################################################################################################################
def print_results_in_console( instance ):
    
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
    
def save_routes( instance ):
    
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
################################################################################################################   
    
    
    
######################################################################################################################################  
def read_data_XLSX( receivedFile ):
    
    ## --------------------- READ DATA EXCEL WHIT OPENPYXL -----------------------------------
    
    ## OPEN FILE AND SAVE IN VARIABLE (archivo)
    archivo = openpyxl.load_workbook(receivedFile, data_only = True)

    ## READ SHEETS OF FILE AND SELECT THE THE FIRST SHEET
    sheets = archivo.sheetnames
    sheetDatos = archivo[sheets[0]]

    ## NODES (param_Nodos)
    param_Nodos = []
    column = sheetDatos['A']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            param_Nodos.append(column[x].value)
        #fi
    #rof

    ## ORDERS (param_Ordenes)
    param_Ords = []
    column = sheetDatos['B']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            param_Ords.append(column[x].value)
        #fi
    #rof


    ## REFERENCES (param_Referencias)
    param_Referencias = []
    column = sheetDatos['C']
    for x in range(len(column)): 
        if (type(column[x].value) != str and column[x].value != None):
            param_Referencias.append(column[x].value)
        #fi
    #rof

    ## LOCATION OF EACH REFERENCE (param_NOD_REF)
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


    ## DISTANCE MATRIX
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
def create_lineal_model( model, param_Nodos, param_Ords, param_Referencias, param_NOD_REF, param_Ordenes, param_R, param_Distancia ):
    

    ## ------------------- SETS --------------------------------
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


    ## --------------------- PARAMETERS -------------------------------------
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

    ## ----------------------- VARIABLES ---------------------------------------
    model.x = pyo.Var(model.OROR, domain = pyo.Binary)
    model.aux = pyo.Var(model.OR)
    model.Dist_ORD = pyo.Var(model.O)


    ## -------------------------- OBJECTIVE FUNCTION ------------------------------------
    def ObjFunc(model):
        return sum(model.Distancia_R[i,j]*model.x[o,i,j] for o in model.O for i in model.ORDENES[o] for j in model.ORDENES[o])
    #fed
    model.FO = pyo.Objective(rule = ObjFunc)


    ## --------------------------- RESTRICTIONS ----------------------------------------------
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
#########################################################################################################################################
    
    
    
    
    
#########################################################################################################################################
def print_results_XLSX( workbook, instance ):
    ## -------------------------- SAVE RESULTS IN EXCEL FILE -------------------------------------

    ## STYLES
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter'})
    cell_format = workbook.add_format({'align': 'center'})
        
    ## CREATE SHEET
    worksheet = workbook.add_worksheet('Resultados')
    worksheet.set_column(0, 0, 20)

    worksheet.merge_range(0, 0, 0, 3, "SOLUCIÓN DEL EJERCICIO", merge_format)
    worksheet.write(1, 0, "Distancia Total: ", merge_format)
    worksheet.write(1, 1, pyo.value(instance.FO), cell_format)

    ## PRINT RESULTS
    row=3
    col=0
    for o in instance.O:
        worksheet.merge_range(row, col, row, 3, "Ruta "+ str(o), merge_format)
        row += 1

        worksheet.write(row, col,"Distancia Recorrida: ", cell_format)
        worksheet.write(row, col + 1,instance.Dist_ORD[o].value, cell_format)
        row += 1
        
        worksheet.write(row, col,"Recorrido: ", cell_format)
        row += 1
        
        for i in instance.ORDENES[o]:
            for j in instance.ORDENES[o]:
                if ( instance.x[o,i,j].value == 1):
                    worksheet.write(row, col + 0,"Del rack ", cell_format)
                    worksheet.write(row, col + 1,i, cell_format)
                    worksheet.write(row, col + 2," al rack", cell_format)
                    worksheet.write(row, col + 3,j, cell_format)
                #fi
            #rof
            row += 1
        #rof
        row += 1
    #rof
        
        
    ## CLOSE THE BOOK
    workbook.close()
#fed
##########################################################################################################################################
    
    
    
if __name__ == '__main__':
    app.run(debug = False, port=5000)
#fi
