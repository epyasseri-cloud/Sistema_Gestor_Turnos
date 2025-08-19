from BaseDeDatos import repositorio_notificaciones
from Dominio import gestor_usuarios

def enviar_notificacion_a_usuario(mensaje, id_usuario):
    usuario = gestor_usuarios.obtener_info_usuario(id_usuario)
    if usuario is None:
        raise ValueError("Usuario no encontrado.")
    repositorio_notificaciones.crear_notificacion(mensaje, id_usuario)

def obtener_historial_notificaciones(id_usuario):
    return repositorio_notificaciones.obtener_notificaciones_por_usuario(id_usuario)