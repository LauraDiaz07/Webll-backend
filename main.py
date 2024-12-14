from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import json
import os

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuración de MySQL desde variables de entorno
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'ljeans')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Eliminar vale especifico
@app.route('/api/deleteVales/<id>', methods=['POST'])
def deleteVales(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM ljeans.vales WHERE id_vale=%s;",id)
        mysql.connection.commit()
        response = {'message': 'Eliminado con éxito'}
        return jsonify(response)
    except OperationalError as e:
        return jsonify({"error": str(e)}), 500

# Modificar vale especifico
@app.route('/api/editVales', methods=['POST'])
def editVales():
    if request.method == 'POST':
        # {'id_vale': 5, 'tipo_vale': 'E', 'nombre_distribuidor': 'Mario', 'apellido_distribuidor': 'Mares', 'clave_distribuidor': 3, 'monto_vale': '500', 'fecha_limite': '2022-12-20', 'cantidad': 4}
        # data["tipo_vale"]
        # Decodificar datos
        data = json.loads(request.data.decode())
        print(data)

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("UPDATE ljeans.vales SET tipo_vale=%s, id_distribuidor=%s, monto_vale=%s, fecha_limite=%s, cantidad=%s WHERE id_vale=%s;",(data["tipo_vale"],data["clave_distribuidor"],data["monto_vale"],data["fecha_limite"],data["cantidad"],data["id_vale"]))
        conn.commit()
        
        response = {'message': 'Modificado con exito'}
    else:
        response = {'message': 'No se pudo modificar'}
    
    return jsonify(response)

# Insertar vales
@app.route('/api/addVales', methods=['POST'])
def addVales():
    if request.method == 'POST':
        # {'tipo_vale': 'L', 'id_ditribuidor': '1', 'monto_vale': 1500, 'fecha_limite': '2022-12-20', 'cantidad': 5}
        # data["tipo_vale"]
        # Decodificar datos
        data = json.loads(request.data.decode())
        
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ljeans.vales (tipo_vale, id_distribuidor, monto_vale, fecha_limite, cantidad) VALUES(%s, %s, %s, %s, %s);",(data["tipo_vale"],data["id_ditribuidor"],data["monto_vale"],data["fecha_limite"],data["cantidad"]))
        conn.commit()
        
        response = {'message': 'Agregado con exito'}
    else:
        response = {'message': 'No se pudo agregar'}
    
    return jsonify(response)

# Mostrar vales activos
@app.route('/api/getVales', methods=['GET'])
def getVales():
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute("SELECT vales.*,distribuidores.nombre_distribuidor,distribuidores.apellidos_distribuidor FROM vales,distribuidores WHERE vales.id_distribuidor = distribuidores.id_distribuidor;")
        data = cursor.fetchall()
        cursor.close()
        if data != None:
            response = jsonify(data)
        else:
            response = ""
            
        return response
    except OperationalError as e:
        return jsonify({"error": str(e)}), 500

# Mostrar distribuidores activos
@app.route('/api/getDistribuidores', methods=['GET'])
def getDistribuidores():
    try:

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT distribuidores.id_distribuidor,distribuidores.nombre_distribuidor,distribuidores.apellidos_distribuidor from distribuidores WHERE estado = 'A'")
        data = cursor.fetchall()
        cursor.close()
        if data != None:
            response = jsonify(data)
        else:
            response = ""
            
        return response
    except OperationalError as e:
        return jsonify({"error": str(e)}), 500

# Home
@app.route('/')
def home():
    response = {
        'Mensaje': 'Backend activo',
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=bool(os.getenv('FLASK_DEBUG', True)), port=os.getenv('PORT', 5000))
