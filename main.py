from flask import Flask, request
from flask import jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS
import json

app = Flask(__name__)
pruebas = True #Definir conexión de BD
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mysql = MySQL()

if pruebas:
    print('Endpoint: localhost')
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'ljeans'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
else:
    print('Endpoint: 193.84.177.213')
    app.config['MYSQL_DATABASE_USER'] = 'r237674_vales'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'C3kAhDNmJ9mp'
    app.config['MYSQL_DATABASE_DB'] = 'r237674_vales'
    app.config['MYSQL_DATABASE_HOST'] = '193.84.177.213'

mysql.init_app(app)

# Eliminar vale especifico
@app.route('/api/deleteVales/<id>', methods=['POST'])
def deleteVales(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ljeans.vales WHERE id_vale=%s;",id)
    conn.commit()

    response = {'message': 'Eliminado con exito'}
    return jsonify(response)

# Modificar vale especifico
@app.route('/api/editVales', methods=['POST'])
def editVales():
    if request.method == 'POST':
        # {'id_vale': 5, 'tipo_vale': 'E', 'nombre_distribuidor': 'Mario', 'apellido_distribuidor': 'Mares', 'clave_distribuidor': 3, 'monto_vale': '500', 'fecha_limite': '2022-12-20', 'cantidad': 4}
        # data["tipo_vale"]
        # Decodificar datos
        data = json.loads(request.data.decode())
        print(data)

        conn = mysql.connect()
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
        
        conn = mysql.connect()
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
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT vales.*,distribuidores.nombre_distribuidor,distribuidores.apellidos_distribuidor FROM vales,distribuidores WHERE vales.id_distribuidor = distribuidores.id_distribuidor;")
    data = cursor.fetchall()
    if data != None:
        response = jsonify(data)
    else:
        response = ""
        
    return response

# Mostrar distribuidores activos
@app.route('/api/getDistribuidores', methods=['GET'])
def getDistribuidores():
    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("SELECT distribuidores.id_distribuidor,distribuidores.nombre_distribuidor,distribuidores.apellidos_distribuidor from distribuidores WHERE estado = 'A'")
    data = cursor.fetchall()
    if data != None:
        response = jsonify(data)
    else:
        response = ""
        
    return response

# Home
@app.route('/')
def home():
    response = {
        'Mensaje': 'Backend activo',
    }
    return jsonify(response)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5000)