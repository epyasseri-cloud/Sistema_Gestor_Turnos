import tkinter as tk
from tkinter import ttk
import requests

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Turnos")
        self.geometry("900x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_registro = ttk.Frame(self.notebook)
        self.frame_turnos = ttk.Frame(self.notebook)
        self.frame_admin = ttk.Frame(self.notebook)
        self.frame_admin.columnconfigure(0, weight=1)
        self.frame_admin.columnconfigure(1, weight=1)

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
        ttk.Label(self.frame_turnos, text="Usuarios registrados").pack()
        self.lista_usuarios = tk.Listbox(self.frame_turnos)
        self.lista_usuarios.pack(fill="both", expand=True)

        ttk.Button(self.frame_turnos, text="Actualizar", command=self.obtener_usuarios).pack()
        ttk.Button(self.frame_turnos, text="Solicitar turno", command=self.solicitar_turno).pack()

    def obtener_usuarios(self):
        try:
            r = requests.get("http://localhost:5000/usuarios")
            self.lista_usuarios.delete(0, tk.END)
            if r.status_code == 200:
                try:
                    for usuario in r.json():
                        self.lista_usuarios.insert(tk.END, f"{usuario['idUsuario']} - {usuario['nombre']} - {usuario['telefono']} - {usuario['email']}")
                except Exception:
                    self.lista_usuarios.insert(tk.END, " Respuesta no es JSON")
            else:
                self.lista_usuarios.insert(tk.END, " Error al obtener usuarios")
        except requests.exceptions.ConnectionError:
            self.lista_usuarios.insert(tk.END, " No se puede conectar al servidor")

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
        ttk.Label(self.frame_admin, text="Panel de administrador", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Crear Cola
        ttk.Label(self.frame_admin, text="Nombre de la cola").grid(row=1, column=0, sticky="w", padx=5)
        self.entry_nombre_cola = ttk.Entry(self.frame_admin)
        self.entry_nombre_cola.grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Label(self.frame_admin, text="Descripción").grid(row=2, column=0, sticky="w", padx=5)
        self.entry_desc_cola = ttk.Entry(self.frame_admin)
        self.entry_desc_cola.grid(row=2, column=1, sticky="ew", padx=5)
        ttk.Button(self.frame_admin, text="Crear cola", command=self.crear_cola_admin).grid(row=3, column=0, columnspan=2, pady=5)
        self.label_cola_resultado = ttk.Label(self.frame_admin, text="")
        self.label_cola_resultado.grid(row=4, column=0, columnspan=2)

        # Listar colas y usuarios para selección
        ttk.Label(self.frame_admin, text="Colas disponibles").grid(row=5, column=0, sticky="w", padx=5)
        self.combobox_colas = ttk.Combobox(self.frame_admin, state="readonly")
        self.combobox_colas.grid(row=5, column=1, sticky="ew", padx=5)
        ttk.Button(self.frame_admin, text="Actualizar colas", command=self.actualizar_colas_admin).grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Label(self.frame_admin, text="Usuarios disponibles").grid(row=7, column=0, sticky="w", padx=5)
        self.combobox_usuarios = ttk.Combobox(self.frame_admin, state="readonly")
        self.combobox_usuarios.grid(row=7, column=1, sticky="ew", padx=5)
        ttk.Button(self.frame_admin, text="Actualizar usuarios", command=self.actualizar_usuarios_admin).grid(row=8, column=0, columnspan=2, pady=5)

        # Asignar turno a cola
        ttk.Button(self.frame_admin, text="Asignar turno", command=self.asignar_turno_admin).grid(row=9, column=0, columnspan=2, pady=5)
        self.label_asignar_resultado = ttk.Label(self.frame_admin, text="")
        self.label_asignar_resultado.grid(row=10, column=0, columnspan=2)

        # Listar turnos para selección
        ttk.Label(self.frame_admin, text="Turnos activos").grid(row=11, column=0, sticky="w", padx=5)
        self.listbox_turnos = tk.Listbox(self.frame_admin, height=8)
        self.listbox_turnos.grid(row=12, column=0, columnspan=2, sticky="ew", padx=5)
        ttk.Button(self.frame_admin, text="Actualizar turnos", command=self.actualizar_turnos_admin).grid(row=13, column=0, columnspan=2, pady=5)

        # Modificar turno
        ttk.Label(self.frame_admin, text="Modificar turno seleccionado").grid(row=16, column=0, columnspan=2, pady=10)
        ttk.Label(self.frame_admin, text="Nuevo nombre").grid(row=17, column=0, sticky="w", padx=5)
        self.entry_modificar_nombre = ttk.Entry(self.frame_admin)
        self.entry_modificar_nombre.grid(row=17, column=1, sticky="ew", padx=5)
        ttk.Label(self.frame_admin, text="Nuevo ID Cola").grid(row=18, column=0, sticky="w", padx=5)
        self.entry_modificar_cola_id = ttk.Entry(self.frame_admin)
        self.entry_modificar_cola_id.grid(row=18, column=1, sticky="ew", padx=5)
        ttk.Label(self.frame_admin, text="Nuevo email").grid(row=19, column=0, sticky="w", padx=5)
        self.entry_modificar_email = ttk.Entry(self.frame_admin)
        self.entry_modificar_email.grid(row=19, column=1, sticky="ew", padx=5)
        ttk.Button(self.frame_admin, text="Modificar turno", command=self.modificar_turno_admin).grid(row=20, column=0, columnspan=2, pady=5)
        self.label_modificar_resultado = ttk.Label(self.frame_admin, text="")
        self.label_modificar_resultado.grid(row=21, column=0, columnspan=2)

        # Cancelar turno
        ttk.Button(self.frame_admin, text="Cancelar turno seleccionado", command=self.cancelar_turno_admin).grid(row=22, column=0, columnspan=2, pady=5)
        self.label_cancelar_resultado = ttk.Label(self.frame_admin, text="")
        self.label_cancelar_resultado.grid(row=23, column=0, columnspan=2)

        # Finalizar turno
        ttk.Button(self.frame_admin, text="Finalizar turno seleccionado", command=self.finalizar_turno_admin).grid(row=24, column=0, columnspan=2, pady=5)
        self.label_finalizar_resultado = ttk.Label(self.frame_admin, text="")
        self.label_finalizar_resultado.grid(row=25, column=0, columnspan=2)

        # Inicializar listas
        self.actualizar_colas_admin()
        self.actualizar_usuarios_admin()
        self.actualizar_turnos_admin()

    def actualizar_colas_admin(self):
        try:
            r = requests.get("http://localhost:5000/listar")
            if r.status_code == 200:
                colas = r.json()
                self.combobox_colas['values'] = [f"{c['idCola']} - {c['nombreCola']}" for c in colas]
            else:
                self.combobox_colas['values'] = []
        except:
            self.combobox_colas['values'] = []

    def actualizar_usuarios_admin(self):
        try:
            r = requests.get("http://localhost:5000/usuarios")
            if r.status_code == 200:
                usuarios = r.json()
                self.combobox_usuarios['values'] = [f"{u['idUsuario']} - {u['nombre']}" for u in usuarios]
            else:
                self.combobox_usuarios['values'] = []
        except:
            self.combobox_usuarios['values'] = []

    def actualizar_turnos_admin(self):
        try:
            r = requests.get("http://localhost:5000/turnos")
            self.listbox_turnos.delete(0, tk.END)
            if r.status_code == 200:
                turnos = r.json()
                if isinstance(turnos, list):
                    for turno in turnos:
                        # Mostrar información relevante de la asignación actual
                        id_turno = turno.get('idTurno', '')
                        usuario = turno.get('usuario', turno.get('idUsuario', ''))
                        cola = turno.get('cola', turno.get('idCola', ''))
                        estado = turno.get('estado', '')
                        self.listbox_turnos.insert(tk.END, f"---Turno: {id_turno}, ---Usuario: {usuario}, ---Cola: {cola}, ---Estado: {estado}")
                else:
                    self.listbox_turnos.insert(tk.END, "No hay turnos activos")
            else:
                self.listbox_turnos.insert(tk.END, "Error al obtener turnos")
        except Exception as e:
            self.listbox_turnos.delete(0, tk.END)
            self.listbox_turnos.insert(tk.END, f"Error: {e}")

    def asignar_turno_admin(self):
        usuario = self.combobox_usuarios.get().split(' - ')[0] if self.combobox_usuarios.get() else ''
        cola = self.combobox_colas.get().split(' - ')[0] if self.combobox_colas.get() else ''
        datos = {
            "usuario_id": usuario,
            "cola_id": cola
        }
        try:
            r = requests.post("http://localhost:5000/turnos", json=datos)
            if r.status_code == 201:
                self.label_asignar_resultado.config(text="Turno asignado")
            else:
                self.label_asignar_resultado.config(text="Error al asignar turno")
        except requests.exceptions.ConnectionError:
            self.label_asignar_resultado.config(text="No se puede conectar al servidor")

    def llamar_siguiente_turno_admin(self):
        cola = self.combobox_colas.get().split(' - ')[0] if self.combobox_colas.get() else ''
        datos = {"cola_id": cola}
        try:
            r = requests.post("http://localhost:5000/asignar_turno", json=datos)
            if r.status_code == 200:
                turno = r.json().get('turno', {})
                if turno:
                    mensaje = (
                        f"Turno asignado:\n"
                        f"---Turno: {turno.get('idTurno', '')}, "
                        f"---Usuario: {turno.get('usuario', '')}, "
                        f"---Cola: {turno.get('cola', '')}, "
                        f"---Estado: {turno.get('estado', '')}"
                    )
                    self.label_llamar_resultado.config(text=mensaje)
                else:
                    self.label_llamar_resultado.config(text="Turno asignado, pero no se pudo obtener los datos completos.")
            else:
                self.label_llamar_resultado.config(text="Error al llamar siguiente turno")
        except requests.exceptions.ConnectionError:
            self.label_llamar_resultado.config(text="No se puede conectar al servidor")

    def modificar_turno_admin(self):
        seleccion = self.listbox_turnos.get(tk.ACTIVE)
        # Extraer el idTurno del formato ---Turno: 1, ---Usuario: ...
        id_turno = ''
        if seleccion:
            partes = seleccion.split(',')
            for parte in partes:
                if '---Turno:' in parte:
                    id_turno = parte.replace('---Turno:', '').strip()
                    break
        datos = {
            "idTurno": id_turno,
            "idCola": self.entry_modificar_cola_id.get(),
            "nombre": self.entry_modificar_nombre.get(),
            "email": self.entry_modificar_email.get()
        }
        try:
            r = requests.put("http://localhost:5000/turnos/modificar", json=datos)
            if r.status_code == 200:
                self.label_modificar_resultado.config(text="Turno modificado")
            else:
                self.label_modificar_resultado.config(text="Error al modificar turno")
        except requests.exceptions.ConnectionError:
            self.label_modificar_resultado.config(text="No se puede conectar al servidor")

    def cancelar_turno_admin(self):
        seleccion = self.listbox_turnos.get(tk.ACTIVE)
        id_turno = ''
        if seleccion:
            partes = seleccion.split(',')
            for parte in partes:
                if '---Turno:' in parte:
                    id_turno = parte.replace('---Turno:', '').strip()
                    break
        datos = {"idTurno": id_turno}
        try:
            r = requests.delete("http://localhost:5000/turnos/cancelar", json=datos)
            if r.status_code == 200:
                self.label_cancelar_resultado.config(text="Turno cancelado")
            else:
                self.label_cancelar_resultado.config(text="Error al cancelar turno")
        except requests.exceptions.ConnectionError:
            self.label_cancelar_resultado.config(text="No se puede conectar al servidor")

    def finalizar_turno_admin(self):
        seleccion = self.listbox_turnos.get(tk.ACTIVE)
        id_turno = ''
        if seleccion:
            partes = seleccion.split(',')
            for parte in partes:
                if '---Turno:' in parte:
                    id_turno = parte.replace('---Turno:', '').strip()
                    break
        datos = {"idTurno": id_turno}
        try:
            r = requests.delete("http://localhost:5000/turnos/finalizar", json=datos)
            if r.status_code == 200:
                self.label_finalizar_resultado.config(text="Turno finalizado y eliminado")
            else:
                self.label_finalizar_resultado.config(text="Error al finalizar turno")
        except requests.exceptions.ConnectionError:
            self.label_finalizar_resultado.config(text="No se puede conectar al servidor")

    def crear_cola_admin(self):
        nombre = self.entry_nombre_cola.get().strip()
        descripcion = self.entry_desc_cola.get().strip()
        if not nombre:
            self.label_cola_resultado.config(text="El nombre de la cola es obligatorio")
            return
        datos = {
            "nombreCola": nombre,
            "descripcion": descripcion
        }
        try:
            r = requests.post("http://localhost:5000/colas/crear", json=datos)
            if r.status_code == 201:
                self.label_cola_resultado.config(text="Cola creada exitosamente")
            else:
                try:
                    mensaje = r.json().get("mensaje") or r.json().get("error") or "Error al crear cola"
                except Exception:
                    mensaje = "Error al crear cola"
                self.label_cola_resultado.config(text=mensaje)
        except requests.exceptions.ConnectionError:
            self.label_cola_resultado.config(text="No se puede conectar al servidor")

    def asignar_turno_admin(self):
        usuario = self.combobox_usuarios.get().split(' - ')[0] if self.combobox_usuarios.get() else ''
        cola = self.combobox_colas.get().split(' - ')[0] if self.combobox_colas.get() else ''
        datos = {
            "usuario_id": usuario,
            "cola_id": cola
        }
        try:
            r = requests.post("http://localhost:5000/turnos", json=datos)
            if r.status_code == 201:
                self.label_asignar_resultado.config(text="Turno asignado")
            else:
                self.label_asignar_resultado.config(text="Error al asignar turno")
        except requests.exceptions.ConnectionError:
            self.label_asignar_resultado.config(text="No se puede conectar al servidor")


    def modificar_turno_admin(self):
        seleccion = self.listbox_turnos.get(tk.ACTIVE)
        id_turno = ''
        if seleccion:
            partes = seleccion.split(',')
            for parte in partes:
                if '---Turno:' in parte:
                    id_turno = parte.replace('---Turno:', '').strip()
                    break
        datos = {
            "idTurno": id_turno,
            "idCola": self.entry_modificar_cola_id.get(),
            "nombre": self.entry_modificar_nombre.get(),
            "email": self.entry_modificar_email.get()
        }
        try:
            r = requests.put("http://localhost:5000/turnos/modificar", json=datos)
            if r.status_code == 200:
                self.label_modificar_resultado.config(text="Turno modificado")
            else:
                self.label_modificar_resultado.config(text="Error al modificar turno")
        except requests.exceptions.ConnectionError:
            self.label_modificar_resultado.config(text="No se puede conectar al servidor")

    def cancelar_turno_admin(self):
        seleccion = self.listbox_turnos.get(tk.ACTIVE)
        id_turno = ''
        if seleccion:
            partes = seleccion.split(',')
            for parte in partes:
                if '---Turno:' in parte:
                    id_turno = parte.replace('---Turno:', '').strip()
                    break
        datos = {"idTurno": id_turno}
        try:
            r = requests.delete("http://localhost:5000/turnos/cancelar", json=datos)
            if r.status_code == 200:
                self.label_cancelar_resultado.config(text="Turno cancelado")
            else:
                self.label_cancelar_resultado.config(text="Error al cancelar turno")
        except requests.exceptions.ConnectionError:
            self.label_cancelar_resultado.config(text="No se puede conectar al servidor")

    def finalizar_turno_admin(self):
        datos = {"idTurno": self.entry_finalizar_turno_id.get()}
        try:
            r = requests.delete("http://localhost:5000/turnos/finalizar", json=datos)
            if r.status_code == 200:
                self.label_finalizar_resultado.config(text="Turno finalizado y eliminado")
            else:
                self.label_finalizar_resultado.config(text="Error al finalizar turno")
        except requests.exceptions.ConnectionError:
            self.label_finalizar_resultado.config(text="No se puede conectar al servidor")

class PanelTurnos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Panel de Manejo de Turnos")
        self.geometry("600x500")
        self.configure(bg="#f5f6fa")
        self.turnos = []
        self.turno_actual = None

        # Título destacado
        self.label_titulo = tk.Label(self, text="Gestión de Turnos", font=("Segoe UI", 22, "bold"), bg="#f5f6fa", fg="#273c75")
        self.label_titulo.pack(pady=(20,10))

        # Turno actual destacado
        self.frame_actual = tk.Frame(self, bg="#dff9fb", bd=2, relief="groove")
        self.frame_actual.pack(pady=10, padx=30, fill="x")
        self.label_actual = tk.Label(self.frame_actual, text="Turno actual", font=("Segoe UI", 18, "bold"), bg="#dff9fb", fg="#192a56", height=2)
        self.label_actual.pack(pady=10)

        # Botón moderno
        self.btn_siguiente = tk.Button(self, text="Llamar siguiente turno", command=self.llamar_siguiente_turno, font=("Segoe UI", 14), bg="#00a8ff", fg="white", activebackground="#0097e6", activeforeground="white", relief="flat", bd=0)
        self.btn_siguiente.pack(pady=15)

        # Lista de turnos en espera
        self.label_lista = tk.Label(self, text="Turnos en espera:", font=("Segoe UI", 14, "bold"), bg="#f5f6fa", fg="#353b48")
        self.label_lista.pack(pady=(10,0))
        self.frame_lista = tk.Frame(self, bg="#f5f6fa")
        self.frame_lista.pack(pady=5, padx=30, fill="both", expand=True)
        self.listbox_turnos = tk.Listbox(self.frame_lista, font=("Segoe UI", 13), height=10, width=50, bg="#f1f2f6", fg="#353b48", bd=0, highlightthickness=0, selectbackground="#00a8ff", selectforeground="white")
        self.listbox_turnos.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.listbox_turnos.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox_turnos.config(yscrollcommand=self.scrollbar.set)

        self.actualizar_turnos()

    def actualizar_turnos(self):
        try:
            r = requests.get("http://localhost:5000/turnos")
            if r.status_code == 200:
                self.turnos = r.json()
                self.listbox_turnos.delete(0, tk.END)
                for turno in self.turnos:
                    texto = f"Turno: {turno.get('idTurno','')}, Usuario: {turno.get('usuario','')}, Cola: {turno.get('cola','')}, Estado: {turno.get('estado','')}"
                    self.listbox_turnos.insert(tk.END, texto)
                self.mostrar_turno_actual()
        except Exception as e:
            self.listbox_turnos.delete(0, tk.END)
            self.listbox_turnos.insert(tk.END, f"Error: {e}")

    def llamar_siguiente_turno(self):
        if self.turnos:
            self.turno_actual = self.turnos.pop(0)
            # Cambiar estado a 'Atendiendo' en la base de datos
            try:
                id_turno = self.turno_actual.get('idTurno', None)
                if id_turno:
                    r_estado = requests.put("http://localhost:5000/turnos/modificar", json={"idTurno": id_turno, "estado": "Atendiendo"})
                    if r_estado.status_code == 200:
                        self.turno_actual['estado'] = "Atendiendo"
                    r = requests.delete("http://localhost:5000/turnos/finalizar", json={"idTurno": id_turno})
                    if r.status_code == 200:
                        self.label_actual.config(text="Turno finalizado y eliminado")
                    else:
                        self.label_actual.config(text="Error al eliminar turno")
            except Exception as e:
                self.label_actual.config(text=f"Error eliminando turno: {e}")
            self.actualizar_turnos()
        else:
            self.label_actual.config(text="No hay turnos en espera")

    def mostrar_turno_actual(self):
        if self.turno_actual:
            texto = f"Turno: {self.turno_actual.get('idTurno','')}, Usuario: {self.turno_actual.get('usuario','')}, Cola: {self.turno_actual.get('cola','')}, Estado: {self.turno_actual.get('estado','')}"
            self.label_actual.config(text=texto)
        elif self.turnos:
            self.turno_actual = self.turnos[0]
            texto = f"Turno: {self.turno_actual.get('idTurno','')}, Usuario: {self.turno_actual.get('usuario','')}, Cola: {self.turno_actual.get('cola','')}, Estado: {self.turno_actual.get('estado','')}"
            self.label_actual.config(text=texto)
        else:
            self.label_actual.config(text="No hay turnos en espera")

# Para abrir el panel desde la interfaz principal:
# panel = PanelTurnos(master=self)
# panel.grab_set()

if __name__ == "__main__":
    app = App()
    app.mainloop()