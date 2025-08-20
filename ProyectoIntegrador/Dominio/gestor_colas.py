from BaseDeDatos import repositorio_colas

def crear_nueva_cola(nombre, descripcion):
    print(f"gestor_colas.crear_nueva_cola: nombre={nombre}, descripcion={descripcion}")
    repositorio_colas.crear_cola(nombre, descripcion)
    print("repositorio_colas.crear_cola ejecutado")

def obtener_detalle_cola(id_cola):
    return repositorio_colas.obtener_cola_por_id(id_cola)

def listar_todas_las_colas():
    return repositorio_colas.listar_colas()