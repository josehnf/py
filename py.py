from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos SQLite
DB_FILE = r'C:\Users\USER\Desktop\RENIEC DB\reniec.db'  # Ruta a la base de datos

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/buscar', methods=['GET'])
def buscar():
    dni = request.args.get('dni')
    nombre = request.args.get('nombre')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM mi_tabla WHERE"  # Actualiza el nombre de la tabla aquí
    params = []

    if dni:
        query += " dni = ?"
        params.append(dni)
    elif nombre:
        query += " nombres LIKE ?"
        params.append(f"%{nombre}%")
    else:
        return jsonify({"error": "Debe proporcionar DNI o nombre"}), 400

    cursor.execute(query, params)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([dict(row) for row in resultados])

if __name__ == '__main__':
    app.run(debug=True)
