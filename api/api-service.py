from flask import Flask
import requests
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    try:
        url = f"http://faker-service:{3000}/obtener_registros"
        resp = requests.get(url).json()
        return json.dumps(resp)
    except Exception as ex:
        logging.debug(ex)
        return {"message":"error en consulta de datos en servicio API"}
    
@app.route("/admin/borrar_registros")
def delete_records():
    try:
        url = f"http://faker-service:{3000}/borrar_registros"
        resp = requests.get(url).json()
        return json.dumps(resp)
    except Exception as ex:
        logging.debug(ex)
        return {"message":"error al borrar registros en servicio API"}

@app.route("/admin/crear_registros")
def create_records():
    try:
        url = f"http://faker-service:{3000}/crear_registros"
        resp = requests.get(url).json()
        return json.dumps(resp)
    except Exception as ex:
        logging.debug(ex)
        return {"message":"error al crear registros en servicio API"}
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81, debug=True)
