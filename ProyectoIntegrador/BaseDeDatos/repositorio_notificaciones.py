import sqlite3
from datetime import datetime
from conexion.conexion import obtener_conexion

def crear_notificacion(mensaje, id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    fecha_hora = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO Notificacion (mensaje, fechaHora, idUsuario)
        VALUES (?, ?, ?)
    """, (mensaje, fecha_hora, id_usuario))
    conexion.commit()
    conexion.close()

def obtener_notificaciones_por_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idNotificacion, mensaje, fechaHora
        FROM Notificacion
        WHERE idUsuario = ?
        ORDER BY fechaHora DESC
    """, (id_usuario,))
    notificaciones = cursor.fetchall()
    conexion.close()
    return notificaciones