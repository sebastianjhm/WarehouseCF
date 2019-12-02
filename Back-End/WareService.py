from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
import xlsxwriter
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pyutilib.subprocess.GlobalData
from Rutas import Rutas
from Racks import Racks
import FunctionsAllocation as fa
import FunctionPicking as fp

## Librería para que pyomo corra dentro de Flask
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

app = Flask(__name__)
cors = CORS(app)

@app.route('/postFileAllocation', methods=['POST'])
@cross_origin()
def post_allocation():
    
    ## SAVE EXCEL FILE THAT ARRIVE OF THE FRONT
    receivedFile = request.files["myExcelFileAlloc"]
    time_limit = request.form.get("timeLimit") ## Time execution
    
    ## READ DATA OPENPYXL
    set_REF , param_AnchoCaja, param_TipoDist, param_Espacios, param_Demanda, param_Frecuencia, set_RACKS, param_TipoRack, param_Pared, param_Utilizacion, param_Costo = fa.read_data_XLSX_Alloc( receivedFile )
    
    ## DECLARE SOLVER, CREATE A PYOMO ABSTRACT MODEL, DECLARE LINEAR MODEL
    opt = SolverFactory('cplex', executable="C:\\Program Files\\IBM\\ILOG\\CPLEX_Studio128\\cplex\\bin\\x64_win64\\cplex")
    model = pyo.AbstractModel()
    fa.create_lineal_model_Alloc( model, set_REF , param_AnchoCaja, param_TipoDist, param_Espacios, param_Demanda, param_Frecuencia, set_RACKS, param_TipoRack, param_Pared, param_Utilizacion, param_Costo )
    
    ## CREATE AN INSTANCE OF THE MODEL, SOLVE PRINT RESULTS BY CONSOLE
    instance = model.create_instance()
    opt.options['timelimit'] = float(time_limit)
    results = opt.solve(instance, tee = False)
    #instance.display()
    
    ## SAVE JSON ROUTES
    Racks["fo"] = 0
    Rutas["racks"] = []
    fa.save_racks_Alloc( instance )
    
    ## PRINT RESULTS IN CONSOLE
    fa.print_results_in_console_Alloc( instance )
    
    ## CREATE EXCEL FILE AND PRINT RESULTS WITH 'XLSXWRITER'
    workbook = xlsxwriter.Workbook('Results_Allocation.xlsx')
    fa.print_results_XLSX_Alloc( workbook, instance )
     
    return send_file('Results_Allocation.xlsx', as_attachment=True)
#fed
    
@app.route('/racks', methods = ['GET'])
@cross_origin()
def get_racks_Alloc():
    return jsonify(Racks)
#fed
    
@app.route('/resultsAllocation', methods = ['GET'])
@cross_origin()
def get_results_Alloc():
    return send_file('Results_Allocation.xlsx', as_attachment=True)
#fed







@app.route('/postFilePicking', methods=['POST'])
@cross_origin()
def post_picking():
    
    ## SAVE EXCEL FILE THAT ARRIVE OF THE FRONT
    receivedFile = request.files["myExcelFile"]
    time_limit = request.form.get("timeLimit") ## Time execution
    print("------", time_limit)
    
    ## READ DATA OPENPYXL
    set_Nodos, set_Ords, set_Referencias, param_NOD_REF, set_Ordenes, set_R, param_Distancia = fp.read_data_XLSX_Picking( receivedFile )
    
    
    ## DECLARE SOLVER, CREATE A PYOMO ABSTRACT MODEL, DECLARE LINEAR MODEL
    opt = SolverFactory('cplex', executable="C:\\Program Files\\IBM\\ILOG\\CPLEX_Studio128\\cplex\\bin\\x64_win64\\cplex")
    #opt = SolverFactory('glpk')
    model = pyo.AbstractModel()
    fp.create_lineal_model_Picking( model, set_Nodos, set_Ords, set_Referencias, param_NOD_REF, set_Ordenes, set_R, param_Distancia )
    
    
    ## CREATE AN INSTANCE OF THE MODEL, SOLVE PRINT RESULTS BY CONSOLE
    instance = model.create_instance()
    opt.options['timelimit'] = float(time_limit)
    results = opt.solve(instance, tee=False)
    #instance.display()
    
    ## PRINT RESULTS IN CONSOLE
    fp.print_results_in_console_Picking( instance )
    
    ## SAVE JSON ROUTES
    Rutas["distanciaTotal"] = 0
    Rutas["ruta"] = []
    fp.save_routes_Picking( instance )
    
    
    ## CREATE EXCEL FILE AND PRINT RESULTS WITH 'XLSXWRITER'
    workbook = xlsxwriter.Workbook('Results_Picking.xlsx')
    fp.print_results_XLSX_Picking( workbook )
    
    
    return send_file('Results_Picking.xlsx', as_attachment=True)

#fed


@app.route('/rutas', methods = ['GET'])
@cross_origin()
def get_routes_picking():
    return jsonify(Rutas)
#fed
    
@app.route('/resultsPicking', methods = ['GET'])
@cross_origin()
def results_picking():
    return send_file('Results_Picking.xlsx', as_attachment=True)
#fed
    


    
if __name__ == '__main__':
    app.run(debug = False, port=5000)
#fi