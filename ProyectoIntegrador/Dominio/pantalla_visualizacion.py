class PantallaVisualizacion:
    def __init__(self, id_pantalla, ubicacion):
        self.id_pantalla = id_pantalla
        self.ubicacion = ubicacion

    def mostrar_turno_actual(self, turno):
        print(f"Turno actual: {turno.id_turno} - Estado: {turno.estado}")

    def mostrar_proximos(self, lista_turnos):
        print("Próximos turnos:")
        for turno in lista_turnos:
            print(f"- {turno.id_turno} (Prioridad: {turno.prioridad})")