from flask import Flask, render_template, request, redirect
import requests
import logging
import json

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    try:
        url = f"http://api-service:{81}/"
        resp = requests.get(url).json()
        return render_template("table-with-pagination.html", profiles = resp)
    except Exception as ex:
        logging.debug(ex)
        return {"message":"error en consulta de datos en servicio web"}

@app.route("/admin")
def admin():
    return render_template("/admin.html", context={})

@app.route("/admin/delete_records")
def delete_records():
    try:
        url = f"http://api-service:{81}/admin/borrar_registros"
        resp = requests.get(url).json()
        return redirect("/admin")
    except Exception as ex:
        logging.debug(ex)
        return {"message":"error al borrar registros en servicio web"}

@app.route("/admin/create_records")
def create_records():
    try:
        url = f"http://api-service:{81}/admin/crear_registros"
        resp = requests.get(url).json()
        return redirect("/admin")
    except Exception as ex:
        logging.debug(ex)
        return {"message":"error al crear registros en servicio web"}
    



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=82, debug=True)