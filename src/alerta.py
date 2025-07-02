import ctypes
import time

ctypes.windll.user32.MessageBoxW(0, "⚠️ Se detectó una gran falla en el sistema", "PROTECTOR DE WINDOWS", 0x10) # Mensaje 1
time.sleep(1)
ctypes.windll.user32.MessageBoxW(0, "🦠 Tu dispositivo ha sido comprometido", "FALLA FATAL EN EL SISTEMA", 0x10) #mensaje 2
