from API.app import app
from Interfaz.interfaz import App, PanelTurnos

if __name__ == "__main__":
    import threading

    def run_flask():
        app.run(debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    app_interfaz = App()

    # Botón para abrir el panel de manejo de turnos
    import tkinter as tk
    btn_panel_turnos = tk.Button(app_interfaz, text="Abrir Panel de Turnos", command=lambda: PanelTurnos(master=app_interfaz), font=("Segoe UI", 12), bg="#00a8ff", fg="white")
    btn_panel_turnos.pack(pady=20)

    app_interfaz.mainloop()