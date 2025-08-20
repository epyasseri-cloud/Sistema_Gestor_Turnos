from flask import Blueprint, request, jsonify
from Dominio import gestor_turnos  
turnos_bp = Blueprint("turnos", __name__)

@turnos_bp.route("/crear", methods=["POST"])
def crear_turno():
    datos = request.json
    try:
        # El idTurno se genera automáticamente en la base de datos
        estado = datos.get("estado", "pendiente")
        prioridad = datos.get("prioridad", 0)
        id_usuario = datos.get("idUsuario")
        id_cola = datos.get("idCola")
        if id_usuario is None or id_cola is None:
            return jsonify({"error": "Faltan datos obligatorios: idUsuario o idCola"}), 400
        from BaseDeDatos import repositorio_turnos
        repositorio_turnos.crear_turno(None, estado, prioridad, id_usuario, id_cola)
        return jsonify({"mensaje": "Turno creado"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@turnos_bp.route("/usuario/<int:id_usuario>", methods=["GET"])
def turnos_usuario(id_usuario):
    turnos = gestor_turnos.consultar_turnos_usuario(id_usuario)
    return jsonify(turnos)

@turnos_bp.route('/turnos', methods=['GET'])
def listar_turnos():
    from BaseDeDatos import repositorio_turnos
    turnos_db = repositorio_turnos.obtener_todos_los_turnos()
    turnos = []
    from BaseDeDatos import repositorio_usuarios, repositorio_colas
    for t in turnos_db:
        usuario = repositorio_usuarios.obtener_usuario_por_id(t[4])
        cola = repositorio_colas.obtener_cola_por_id(t[5])
        nombre_usuario = usuario[1] if usuario else t[4]
        nombre_cola = cola[1] if cola else t[5]
        turnos.append({
            "idTurno": t[0],
            "fechaHora": t[1],
            "estado": t[2],
            "prioridad": t[3],
            "usuario": nombre_usuario,
            "cola": nombre_cola
        })
    return jsonify(turnos), 200

@turnos_bp.route('/turnos', methods=['POST'])
def solicitar_turno():
    datos = request.json
    try:
        usuario_id = datos.get("usuario_id")
        cola_id = datos.get("cola_id")
        estado = datos.get("estado", "pendiente")
        prioridad = datos.get("prioridad", 0)
        if usuario_id is None or cola_id is None:
            return jsonify({"error": "Faltan datos obligatorios: usuario_id o cola_id"}), 400
        from BaseDeDatos import repositorio_turnos, repositorio_usuarios, repositorio_colas
        repositorio_turnos.crear_turno(None, estado, prioridad, usuario_id, cola_id)
        # Obtener el último turno insertado
        conexion = repositorio_turnos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT idTurno, fechaHora, estado, prioridad, idUsuario, idCola FROM Turno ORDER BY idTurno DESC LIMIT 1")
        t = cursor.fetchone()
        conexion.close()
        usuario = repositorio_usuarios.obtener_usuario_por_id(t[4])
        cola = repositorio_colas.obtener_cola_por_id(t[5])
        nombre_usuario = usuario[1] if usuario else t[4]
        nombre_cola = cola[1] if cola else t[5]
        turno = {
            "idTurno": t[0],
            "fechaHora": t[1],
            "estado": t[2],
            "prioridad": t[3],
            "usuario": nombre_usuario,
            "cola": nombre_cola
        }
        return jsonify({"mensaje": "Turno asignado y guardado", "turno": turno}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Endpoint para modificar turno
@turnos_bp.route('/turnos/modificar', methods=['PUT'])
def modificar_turno():
    datos = request.json
    # Aquí deberías implementar la lógica para modificar el turno
    # Ejemplo: gestor_turnos.modificar_turno(datos)
    return jsonify({"mensaje": "Turno modificado"}), 200

# Endpoint para cancelar turno
@turnos_bp.route('/turnos/cancelar', methods=['DELETE'])
def cancelar_turno():
    datos = request.json
    # Aquí deberías implementar la lógica para cancelar el turno
    # Ejemplo: gestor_turnos.cancelar_turno(datos["idTurno"])
    return jsonify({"mensaje": "Turno cancelado"}), 200

# Endpoint para finalizar turno
@turnos_bp.route('/turnos/finalizar', methods=['DELETE'])
def finalizar_turno():
    datos = request.json
    # Aquí deberías implementar la lógica para finalizar y eliminar el turno
    # Ejemplo: gestor_turnos.finalizar_turno(datos["idTurno"])
    return jsonify({"mensaje": "Turno finalizado y eliminado"}), 200