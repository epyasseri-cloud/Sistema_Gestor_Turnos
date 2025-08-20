import sqlite3
from conexion.conexion import obtener_conexion
import os

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Tabla de Usuario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )
    """)

    # Tabla de Administrador
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Administrador (
            idAdmin TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            credenciales TEXT NOT NULL
        )
    """)

    # Tabla de Cola
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cola (
            idCola INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreCola TEXT NOT NULL,
            descripcion TEXT,
            tiempoEspera INTEGER DEFAULT 0
        )
    """)

    # Tabla de Turno
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Turno (
            idTurno INTEGER PRIMARY KEY AUTOINCREMENT,
            fechaHora TEXT NOT NULL,
            estado TEXT NOT NULL,
            prioridad INTEGER DEFAULT 0,
            idUsuario INTEGER,
            idCola TEXT,
            FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
            FOREIGN KEY (idCola) REFERENCES Cola(idCola)
        )
    """)

    # Tabla de Notificacion
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notificacion (
            idNotificacion TEXT PRIMARY KEY,
            mensaje TEXT NOT NULL,
            fechaHora TEXT NOT NULL,
            idUsuario INTEGER,
            FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
        )
    """)

    # Tabla de Pantalla de Visualizacion
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PantallaVisualizacion (
            idPantalla TEXT PRIMARY KEY,
            ubicacion TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()