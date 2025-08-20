import sqlite3
from conexion.conexion import obtener_conexion  

def crear_tabla_cola():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cola (
            idCola INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreCola TEXT NOT NULL,
            descripcion TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def crear_cola(nombre_cola, descripcion):
    print(f"repositorio_colas.crear_cola: nombre_cola={nombre_cola}, descripcion={descripcion}")
    crear_tabla_cola()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO Cola (nombreCola, descripcion)
        VALUES (?, ?)
    """, (nombre_cola, descripcion))
    conexion.commit()
    conexion.close()
    print("Cola insertada en la base de datos")

def obtener_cola_por_id(id_cola):
    crear_tabla_cola()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idCola, nombreCola, descripcion
        FROM Cola
        WHERE idCola = ?
    """, (id_cola,))
    cola = cursor.fetchone()
    conexion.close()
    return cola

def listar_colas():
    crear_tabla_cola()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idCola, nombreCola, descripcion
        FROM Cola
    """)
    colas = cursor.fetchall()
    conexion.close()
    return colas