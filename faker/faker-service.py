from flask import Flask
from faker import Faker
import itertools
from sqlalchemy import create_engine, text
import logging
import json

app = Flask(__name__)
faker = Faker()

logging.basicConfig(level=logging.DEBUG)

def random_data():
    insert_queries = []
    profiles = [dict(itertools.islice(faker.profile().items(), 6)) for data in range(13)]
    for profile in profiles:
        sql = ""
        for llave, valor in profile.items():
            if llave == 'current_location':
                coordinates = [str(coordinate) for coordinate in valor]
                profile.update(current_location = json.dumps({"coordinates":coordinates}))
        values = (str(list(profile.values())).replace("\\","")[1:-1])
        sql = f""" 
        INSERT INTO profile (
            job, 
            company, 
            ssn, 
            residence, 
            current_location, 
            blood_group)
        VALUES ({values});""".replace("\n","")
        insert_queries.append(sql)
    logging.debug(insert_queries[0])
    return insert_queries


def execute_queries(list_queries_string=[], querie_type=''):
    db_name = 'rainbow_database'
    db_user = 'unicorn_user'
    db_pass = 'magical_password'
    db_host = 'database-service'
    db_port = '5432'

    try:
        db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
        logging.debug(f"DB Connection String: {db_string}")
        engine = create_engine(db_string)
        logging.debug(f"Engine Object Type: {type(engine)}")
        
        # Create a connection
        with engine.connect() as conn:
            if querie_type == 'INSERT':
                for querie in list_queries_string:
                    logging.debug(f"Executing query: {querie}")
                    result = conn.execute(text(querie))
                conn.commit()  # Commit the transaction
                return {"message": "Data inserted successfully."}
            elif querie_type == 'SELECT':
                data_profiles = []
                for querie in list_queries_string:
                    logging.debug(f"Executing query: {querie}")
                    result = conn.execute(text(querie))
                    column_names = result.keys()
                    for row in result.fetchall():
                        data_profiles.append(dict(zip(column_names, row)))
                return data_profiles
            elif querie_type == 'DELETE':
                for querie in list_queries_string:
                    logging.debug(f"Executing query: {querie}")
                    result = conn.execute(text(querie))
                conn.commit()
                return {"message": "Data deleted successfully."}
    except Exception as ex:
        logging.error(ex)
        return {"message": "Error al ejecutar la consulta"}


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