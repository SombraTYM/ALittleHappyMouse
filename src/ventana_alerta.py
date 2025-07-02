import ctypes
import sys
import threading
import time
import win32gui
import win32con

MB_OK = 0x0
MB_ICONERROR = 0x10  # Icono rojo de error

def mensaje_alerta_auto_cierre(titulo, mensaje, duracion=3000):
    def show_message():
        ctypes.windll.user32.MessageBoxW(0, mensaje, titulo, MB_OK | MB_ICONERROR)

    def close_message(timer_event):
        time.sleep(duracion / 1000)
        try:
            hwnd = win32gui.FindWindow(None, titulo)
            if hwnd:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            print(f"⚠️ No se pudo cerrar ventana: {e}")
        timer_event.set()

    timer_event = threading.Event()
    threading.Thread(target=show_message, daemon=True).start()
    threading.Thread(target=close_message, args=(timer_event,), daemon=True).start()
    timer_event.wait()

def mostrar_alertas(tipo):
    mensajes = []

    if tipo == "60":
        mensajes = [
            "¿Pensabas que esto era un simple juego?",
            "Tu sistema está siendo observado.",
            "No puedes escapar.",
            "Demasiado tarde para detenerme..."
        ]
    elif tipo == "30":
        mensajes = [
            "¡NO PUEDO!",
            "¡NO PUEDO PERDER!"
        ]

    for msg in mensajes:
        mensaje_alerta_auto_cierre("ALERTA DEL SISTEMA", msg, duracion=2000)

if __name__ == "__main__":
    tipo = sys.argv[1] if len(sys.argv) > 1 else "60"
    mostrar_alertas(tipo)
