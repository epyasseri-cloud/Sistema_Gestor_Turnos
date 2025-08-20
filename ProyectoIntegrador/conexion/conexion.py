import sqlite3
import os

def obtener_conexion():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta_datos = os.path.join(raiz, "Datos")
    os.makedirs(carpeta_datos, exist_ok=True) 
    ruta_db = os.path.join(carpeta_datos, "sistema_turnos.db")
    conexion = sqlite3.connect(ruta_db)
    return conexion