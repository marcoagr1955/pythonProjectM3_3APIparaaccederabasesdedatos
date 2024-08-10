from flask import Flask, jsonify, request
import mysql.connector
from config import db_config

app = Flask(__name__)


# Conectar a la base de datos
def connect_db():
    return mysql.connector.connect(**db_config)


# Ruta para obtener todos los registros de la tabla "Curso"
@app.route('/api/v1/cursos', methods=['GET'])
def get_cursos():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM curso")
        cursos = cursor.fetchall()
        return jsonify(cursos)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    finally:
        cursor.close()
        conn.close()


# Ruta para obtener un curso por su ID
@app.route('/api/v1/cursos/<int:id>', methods=['GET'])
def get_curso(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM curso WHERE idCurso = %s", (id,))
        curso = cursor.fetchone()
        if curso:
            return jsonify(curso)
        else:
            return jsonify({"error": "Curso no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
