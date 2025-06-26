import ctypes
import time

ctypes.windll.user32.MessageBoxW(0, "⚠️ Se detectó una gran falla en el sistema", "ALERTA DE SEGURIDAD", 0x10)
time.sleep(1)
ctypes.windll.user32.MessageBoxW(0, "🦠 Tu dispositivo ha sido comprometido", "SISTEMA INFECTADO", 0x10)
