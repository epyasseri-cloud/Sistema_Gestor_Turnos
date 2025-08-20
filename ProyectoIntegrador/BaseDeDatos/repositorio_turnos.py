def modificar_turno(id_turno, id_cola=None, estado=None, prioridad=None, numero=None, email=None, nombre=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    campos = []
    valores = []
    if id_cola is not None:
        campos.append('idCola = ?')
        valores.append(id_cola)
    if estado is not None:
        campos.append('estado = ?')
        valores.append(estado)
    if prioridad is not None:
        campos.append('prioridad = ?')
        valores.append(prioridad)
    if numero is not None:
        campos.append('prioridad = ?')  # Usar prioridad como "número de turno" si no hay otro campo
        valores.append(numero)
    if campos:
        consulta = f"UPDATE Turno SET {', '.join(campos)} WHERE idTurno = ?"
        valores.append(id_turno)
        cursor.execute(consulta, valores)
        conexion.commit()
    # Modificar email del usuario si se proporciona
    if email is not None:
        cursor.execute("UPDATE Usuario SET email = ? WHERE idUsuario = (SELECT idUsuario FROM Turno WHERE idTurno = ?)", (email, id_turno))
        conexion.commit()
    # Modificar nombre del usuario si se proporciona
    if nombre is not None:
        cursor.execute("UPDATE Usuario SET nombre = ? WHERE idUsuario = (SELECT idUsuario FROM Turno WHERE idTurno = ?)", (nombre, id_turno))
        conexion.commit()
    conexion.close()
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

def eliminar_turno(id_turno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Turno WHERE idTurno = ?", (id_turno,))
    conexion.commit()
    conexion.close()