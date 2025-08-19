from flask import Blueprint, request, jsonify
from Dominio import gestor_colas

colas_bp = Blueprint("colas", __name__)

@colas_bp.route("/crear", methods=["POST"])
def crear_cola():
    datos = request.json
    gestor_colas.crear_nueva_cola(datos["nombreCola"], datos["descripcion"])
    return jsonify({"mensaje": "Cola creada exitosamente"}), 201

@colas_bp.route("/<int:id_cola>", methods=["GET"])
def obtener_cola(id_cola):
    cola = gestor_colas.obtener_detalle_cola(id_cola)
    if cola:
        return jsonify({
            "idCola": cola[0],
            "nombreCola": cola[1],
            "descripcion": cola[2]
        })
    return jsonify({"error": "Cola no encontrada"}), 404

@colas_bp.route("/listar", methods=["GET"])
def listar_colas():
    colas = gestor_colas.listar_todas_las_colas()
    return jsonify([
        {"idCola": c[0], "nombreCola": c[1], "descripcion": c[2]}
        for c in colas
    ])