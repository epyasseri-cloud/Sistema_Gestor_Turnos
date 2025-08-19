class Cola:
    def __init__(self, id_cola, nombre, descripcion):
        self.id_cola = id_cola
        self.nombre = nombre
        self.descripcion = descripcion
        self.tiempo_espera = 0
        self.turnos = []

    def agregar_turno(self, turno):
        self.turnos.append(turno)

    def siguiente_turno(self):
        if self.turnos:
            return self.turnos.pop(0)
        return None