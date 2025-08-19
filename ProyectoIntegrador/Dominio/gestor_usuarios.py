from BaseDeDatos import repositorio_usuarios

def registrar_nuevo_usuario(nombre, telefono, email):
    repositorio_usuarios.registrar_usuario(nombre, telefono, email)

def obtener_info_usuario(id_usuario):
    return repositorio_usuarios.obtener_usuario_por_id(id_usuario)