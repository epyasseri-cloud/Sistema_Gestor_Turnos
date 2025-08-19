from flask import Blueprint, request, jsonify
from Dominio import gestor_turnos  
turnos_bp = Blueprint("turnos", __name__)

@turnos_bp.route("/crear", methods=["POST"])
def crear_turno():
    datos = request.json
    try:
        gestor_turnos.generar_turno(
            datos["idTurno"], datos["estado"], datos["prioridad"],
            datos["idUsuario"], datos["idCola"]
        )
        return jsonify({"mensaje": "Turno creado"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@turnos_bp.route("/usuario/<int:id_usuario>", methods=["GET"])
def turnos_usuario(id_usuario):
    turnos = gestor_turnos.consultar_turnos_usuario(id_usuario)
    return jsonify(turnos)

@turnos_bp.route('/turnos', methods=['GET'])
def listar_turnos():
    turnos = [
        {"usuario": "cris", "cola": "Caja 1"},
        {"usuario": "jesus", "cola": "Caja 2"}
    ]
    return jsonify(turnos), 200

@turnos_bp.route('/turnos', methods=['POST'])
def solicitar_turno():
    datos = request.json
    try:
        # Ajusta los nombres de los campos según lo que envía la interfaz
        usuario_id = datos.get("usuario_id")
        cola_id = datos.get("cola_id")
        # Aquí deberías llamar a la lógica para crear el turno
        # Por ejemplo:
        # turno = gestor_turnos.solicitar_turno(usuario_id, cola_id)
        # return jsonify({"turno": turno}), 201
        return jsonify({"mensaje": f"Turno solicitado para usuario {usuario_id} en cola {cola_id}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400