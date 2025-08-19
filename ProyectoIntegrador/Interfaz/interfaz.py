import tkinter as tk
from tkinter import ttk
import requests

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Turnos")
        self.geometry("600x400")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.frame_registro = ttk.Frame(self.notebook)
        self.frame_turnos = ttk.Frame(self.notebook)
        self.frame_admin = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_registro, text="Registro")
        self.notebook.add(self.frame_turnos, text="Turnos")
        self.notebook.add(self.frame_admin, text="Administrador")

        self.crear_panel_registro()
        self.crear_panel_turnos()
        self.crear_panel_admin()

    def crear_panel_registro(self):
        ttk.Label(self.frame_registro, text="Nombre").pack()
        self.entry_nombre = ttk.Entry(self.frame_registro)
        self.entry_nombre.pack()

        ttk.Label(self.frame_registro, text="Teléfono").pack()
        self.entry_telefono = ttk.Entry(self.frame_registro)
        self.entry_telefono.pack()

        ttk.Label(self.frame_registro, text="Email").pack()
        self.entry_email = ttk.Entry(self.frame_registro)
        self.entry_email.pack()

        ttk.Button(self.frame_registro, text="Registrar", command=self.registrar_usuario).pack()
        self.label_resultado = ttk.Label(self.frame_registro, text="")
        self.label_resultado.pack()

    def registrar_usuario(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "telefono": self.entry_telefono.get(),
            "email": self.entry_email.get()
        }
        try:
            r = requests.post("http://localhost:5000/usuarios", json=datos)
            if r.status_code == 201:
                self.label_resultado.config(text=" Usuario registrado")
            else:
                self.label_resultado.config(text=" Error al registrar")
        except requests.exceptions.ConnectionError:
            self.label_resultado.config(text=" No se puede conectar al servidor")

    def crear_panel_turnos(self):
        ttk.Label(self.frame_turnos, text="Turnos activos").pack()
        self.lista_turnos = tk.Listbox(self.frame_turnos)
        self.lista_turnos.pack(fill="both", expand=True)

        ttk.Button(self.frame_turnos, text="Actualizar", command=self.obtener_turnos).pack()
        ttk.Button(self.frame_turnos, text="Solicitar turno", command=self.solicitar_turno).pack()

    def obtener_turnos(self):
        try:
            r = requests.get("http://localhost:5000/turnos")
            self.lista_turnos.delete(0, tk.END)
            if r.status_code == 200:
                try:
                    for turno in r.json():
                        self.lista_turnos.insert(tk.END, f"{turno['usuario']} - {turno['cola']}")
                except requests.exceptions.JSONDecodeError:
                    self.lista_turnos.insert(tk.END, " Respuesta no es JSON")
            else:
                self.lista_turnos.insert(tk.END, " Error al obtener turnos")
        except requests.exceptions.ConnectionError:
            self.lista_turnos.insert(tk.END, " No se puede conectar al servidor")

    def solicitar_turno(self):
        datos = {
            "usuario_id": 1,  # ejemplo
            "cola_id": 2      # ejemplo
        }
        try:
            r = requests.post("http://localhost:5000/turnos", json=datos)
            if r.status_code == 201:
                self.obtener_turnos()
            else:
                self.lista_turnos.insert(tk.END, " Error al solicitar turno")
        except requests.exceptions.ConnectionError:
            self.lista_turnos.insert(tk.END, " No se puede conectar al servidor")

    def crear_panel_admin(self):
        ttk.Label(self.frame_admin, text="Panel de administrador").pack()
        ttk.Button(self.frame_admin, text="Asignar siguiente turno", command=self.asignar_turno).pack()

    def asignar_turno(self):
        try:
            r = requests.post("http://localhost:5000/asignar_turno", json={"cola_id": 2})
            if r.status_code == 200:
                ttk.Label(self.frame_admin, text=f" Turno asignado: {r.json()['turno']}").pack()
            else:
                ttk.Label(self.frame_admin, text=" Error al asignar turno").pack()
        except requests.exceptions.ConnectionError:
            ttk.Label(self.frame_admin, text=" No se puede conectar al servidor").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()