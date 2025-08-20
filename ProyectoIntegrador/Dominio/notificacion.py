from datetime import datetime

class Notificacion:
    def __init__(self, id_notificacion, mensaje):
        self.id_notificacion = id_notificacion
        self.mensaje = mensaje
        self.fecha_hora = datetime.now()

    def enviar_sms(self, telefono):
        print(f"SMS a {telefono}: {self.mensaje}")

    def enviar_push(self, dispositivo_id):
        print(f"Push a {dispositivo_id}: {self.mensaje}")