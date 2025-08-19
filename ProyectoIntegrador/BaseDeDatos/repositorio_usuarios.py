import sqlite3
from conexion.conexion import obtener_conexion

def crear_tabla_usuario():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def registrar_usuario(nombre, telefono, email):
    crear_tabla_usuario()  # Asegura que la tabla existe antes de insertar
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO Usuario (nombre, telefono, email)
        VALUES (?, ?, ?)
    """, (nombre, telefono, email))
    conexion.commit()
    conexion.close()

def obtener_usuario_por_id(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idUsuario, nombre, telefono, email
        FROM Usuario
        WHERE idUsuario = ?
    """, (id_usuario,))
    usuario = cursor.fetchone()
    conexion.close()
    return usuario