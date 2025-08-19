class Administrador:
    def __init__(self, id_admin, nombre, credenciales):
        self.id_admin = id_admin
        self.nombre = nombre
        self.credenciales = credenciales

    def gestionar_colas(self):
        # Lógica para gestionar colas
        pass

    def asignar_turnos(self, cola):
        # Lógica para asignar turnos en una cola
        pass

    def llamar_siguiente(self, cola):
        # Lógica para llamar al siguiente turno
        pass