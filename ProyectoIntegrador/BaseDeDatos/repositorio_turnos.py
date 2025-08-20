# Obtener todos los turnos
def obtener_todos_los_turnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idTurno, fechaHora, estado, prioridad, idUsuario, idCola
        FROM Turno
        ORDER BY fechaHora DESC
    """)
    turnos = cursor.fetchall()
    conexion.close()
    return turnos
import sqlite3
from datetime import datetime
from conexion.conexion import obtener_conexion

def crear_turno(id_turno, estado, prioridad, id_usuario, id_cola):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    fecha_hora = datetime.now().isoformat()
    if id_turno is None:
        cursor.execute("""
            INSERT INTO Turno (fechaHora, estado, prioridad, idUsuario, idCola)
            VALUES (?, ?, ?, ?, ?)
        """, (fecha_hora, estado, prioridad, id_usuario, id_cola))
    else:
        cursor.execute("""
            INSERT INTO Turno (idTurno, fechaHora, estado, prioridad, idUsuario, idCola)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_turno, fecha_hora, estado, prioridad, id_usuario, id_cola))
    conexion.commit()
    conexion.close()

def obtener_turnos_por_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idTurno, fechaHora, estado, prioridad, idCola
        FROM Turno
        WHERE idUsuario = ?
        ORDER BY fechaHora DESC
    """, (id_usuario,))
    turnos = cursor.fetchall()
    conexion.close()
    return turnos

def crear_tabla_turno():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Turno (
            idTurno INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT,
            prioridad TEXT,
            idUsuario INTEGER,
            idCola INTEGER,
            FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
            FOREIGN KEY (idCola) REFERENCES Cola(idCola)
        )
    """)
    conexion.commit()
    conexion.close()