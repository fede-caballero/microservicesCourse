import logging
from flask import Flask
from resources.data_generator import random_data, execute_queries

app = Flask(__name__)

@app.route('/crear_registros')
def create_profiles():
    try:
        execute_queries(random_data(),"INSERT")
        return {"message":"Registros creados correctamente"}
    except Exception as ex:
        logging.debug(ex)
        return {"message":"Error al crear registros"}

@app.route('/obtener_registros')
def get_profiles():
    querie_data = 'SELECT * FROM profile;'
    try:
        results_querie = execute_queries([querie_data],"SELECT")
        return results_querie
    except:
        return {"message":"Error al obtener registros"}
    
@app.route('/borrar_registros')
def delete_profiles():
    querie_data = 'DELETE FROM profile;'
    try:
        results_querie = execute_queries([querie_data],"DELETE")
        return results_querie
    except Exception as ex:
        logging.error(ex)
        return {"message": "Error al borrar registros"}

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)