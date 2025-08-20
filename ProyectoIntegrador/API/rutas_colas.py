from flask import Blueprint, request, jsonify
from Dominio import gestor_colas

colas_bp = Blueprint("colas", __name__)

@colas_bp.route("/colas/crear", methods=["POST"])
def crear_cola():
    datos = request.json
    nombre = datos.get("nombreCola", "").strip()
    descripcion = datos.get("descripcion", "")
    if not nombre:
        return jsonify({"error": "El nombre de la cola es obligatorio"}), 400
    try:
        print(f"Recibido para crear cola: nombre={nombre}, descripcion={descripcion}")
        gestor_colas.crear_nueva_cola(nombre, descripcion)
        print("gestor_colas.crear_nueva_cola ejecutado")
        return jsonify({"mensaje": "Cola creada exitosamente"}), 201
    except Exception as e:
        print(f"Error al crear cola: {e}")
        return jsonify({"error": str(e)}), 500

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