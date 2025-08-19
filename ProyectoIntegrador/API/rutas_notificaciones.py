from flask import Blueprint, request, jsonify
from Dominio import gestor_notificaciones  # Importa el módulo gestor_notificaciones

notificaciones_bp = Blueprint("notificaciones", __name__)

@notificaciones_bp.route("/enviar", methods=["POST"])
def enviar_notificacion():
    datos = request.json
    try:
        gestor_notificaciones.enviar_notificacion_a_usuario(
            datos["mensaje"], datos["idUsuario"]
        )
        return jsonify({"mensaje": "Notificación enviada"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@notificaciones_bp.route("/usuario/<int:id_usuario>", methods=["GET"])
def historial_notificaciones(id_usuario):
    notificaciones = gestor_notificaciones.obtener_historial_notificaciones(id_usuario)
    return jsonify([
        {"idNotificacion": n[0], "mensaje": n[1], "fechaHora": n[2]}
        for n in notificaciones
    ])

@notificaciones_bp.route('/notificaciones', methods=['POST'])
def crear_notificacion():
    # ...lógica para crear notificación...
    return "Notificación creada", 201