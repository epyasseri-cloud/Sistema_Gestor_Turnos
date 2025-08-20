from flask import Flask, request, jsonify, send_from_directory, send_from_directory
from flask_cors import CORS
from API.rutas_usuarios import usuarios_bp
from API.rutas_turnos import turnos_bp
from API.rutas_notificaciones import notificaciones_bp
from API.rutas_colas import colas_bp

import os
app = Flask(__name__)
CORS(app)  # Permite peticiones desde el navegador

app.register_blueprint(usuarios_bp)
app.register_blueprint(turnos_bp)
app.register_blueprint(notificaciones_bp)
app.register_blueprint(colas_bp)

@app.route("/conocenos")
def conocenos():
    return send_from_directory("../HTML", "index.html")

@app.route('/html/<path:filename>')
def html_static(filename):
    return send_from_directory("../HTML", filename)
    
# Rutas para servir archivos HTML
@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../HTML'), 'index.html')

@app.route('/<path:filename>')
def html_files(filename):
    html_dir = os.path.join(os.path.dirname(__file__), '../HTML')
    return send_from_directory(html_dir, filename)

@app.route("/asignar_turno", methods=["POST"])
def asignar_turno():
    datos = request.json
    cola_id = datos.get("cola_id")
    # Aquí deberías llamar a la lógica para asignar el siguiente turno de la cola
    # Por ejemplo:
    # turno = gestor_turnos.asignar_siguiente_turno(cola_id)
    # return jsonify({"turno": turno}), 200
    return jsonify({"turno": f"Turno asignado para cola {cola_id}"}), 200