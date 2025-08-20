from flask import Blueprint, request, jsonify
from Dominio import gestor_usuarios

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/registrar", methods=["POST"])
def registrar_usuario():
    datos = request.json
    gestor_usuarios.registrar_nuevo_usuario(
        datos["nombre"], datos["telefono"], datos["email"]
    )
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@usuarios_bp.route("/<int:id_usuario>", methods=["GET"])
def obtener_usuario(id_usuario):
    usuario = gestor_usuarios.obtener_info_usuario(id_usuario)
    if usuario:
        return jsonify({
            "idUsuario": usuario[0],
            "nombre": usuario[1],
            "telefono": usuario[2],
            "email": usuario[3]
        })
    return jsonify({"error": "Usuario no encontrado"}), 404

@usuarios_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.json
    gestor_usuarios.registrar_nuevo_usuario(
        datos["nombre"], datos["telefono"], datos["email"]
    )
    return jsonify({"mensaje": "Usuario registrado"}), 201

# Nuevo endpoint para listar todos los usuarios
@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    from BaseDeDatos import repositorio_usuarios
    conexion = repositorio_usuarios.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT idUsuario, nombre, telefono, email FROM Usuario")
    usuarios = cursor.fetchall()
    conexion.close()
    lista = [
        {"idUsuario": u[0], "nombre": u[1], "telefono": u[2], "email": u[3]}
        for u in usuarios
    ]
    return jsonify(lista), 200