from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import os
import json

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)
pruebas = False  # Definir conexión de BD
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'db': os.getenv('MYSQL_DB', 'ljeans'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """Crear una conexión a la base de datos."""
    return pymysql.connect(**DB_CONFIG)

# Endpoints
@app.route('/api/deleteVales/<id>', methods=['POST'])
def deleteVales(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ljeans.vales WHERE id_vale = %s;", (id,))
            connection.commit()
        return jsonify({'message': 'Eliminado con éxito'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/editVales', methods=['POST'])
def editVales():
    try:
        data = json.loads(request.data.decode())
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE ljeans.vales 
                SET tipo_vale = %s, id_distribuidor = %s, monto_vale = %s, fecha_limite = %s, cantidad = %s 
                WHERE id_vale = %s;
            """, (data["tipo_vale"], data["clave_distribuidor"], data["monto_vale"], data["fecha_limite"], data["cantidad"], data["id_vale"]))
            connection.commit()
        return jsonify({'message': 'Modificado con éxito'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/addVales', methods=['POST'])
def addVales():
    try:
        data = json.loads(request.data.decode())
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO ljeans.vales (tipo_vale, id_distribuidor, monto_vale, fecha_limite, cantidad) 
                VALUES (%s, %s, %s, %s, %s);
            """, (data["tipo_vale"], data["id_ditribuidor"], data["monto_vale"], data["fecha_limite"], data["cantidad"]))
            connection.commit()
        return jsonify({'message': 'Agregado con éxito'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/getVales', methods=['GET'])
def getVales():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT vales.*, distribuidores.nombre_distribuidor, distribuidores.apellidos_distribuidor 
                FROM vales 
                INNER JOIN distribuidores ON vales.id_distribuidor = distribuidores.id_distribuidor;
            """)
            data = cursor.fetchall()
        return jsonify(data if data else [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/getDistribuidores', methods=['GET'])
def getDistribuidores():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_distribuidor, nombre_distribuidor, apellidos_distribuidor 
                FROM distribuidores 
                WHERE estado = 'A';
            """)
            data = cursor.fetchall()
        return jsonify(data if data else [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/')
def home():
    return jsonify({'message': 'Backend activo'})

if __name__ == '__main__':
    app.run(debug=bool(os.getenv('FLASK_DEBUG', True)), port=os.getenv('PORT', 5000))
