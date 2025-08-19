from API.app import app

if __name__ == "__main__":
    import threading

    def run_flask():
        app.run(debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    from Interfaz.interfaz import App

    app_interfaz = App()
    app_interfaz.mainloop()