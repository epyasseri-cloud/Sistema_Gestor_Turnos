from datetime import datetime

class Turno:
    def __init__(self, id_turno, prioridad=0):
        self.id_turno = id_turno
        self.fecha_hora = datetime.now()
        self.estado = "pendiente"
        self.prioridad = prioridad
        self.usuario = None

    def asignar_usuario(self, usuario):
        self.usuario = usuario

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado