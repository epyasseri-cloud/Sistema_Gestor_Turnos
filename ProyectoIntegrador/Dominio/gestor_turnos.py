from BaseDeDatos import repositorio_turnos
from Dominio import gestor_usuarios

def generar_turno(id_turno, estado, prioridad, id_usuario, id_cola):
    usuario = gestor_usuarios.obtener_info_usuario(id_usuario)
    if usuario is None:
        raise ValueError("El usuario no existe.")
    repositorio_turnos.crear_turno(id_turno, estado, prioridad, id_usuario, id_cola)

def consultar_turnos_usuario(id_usuario):
    return repositorio_turnos.obtener_turnos_por_usuario(id_usuario)