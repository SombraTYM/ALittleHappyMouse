import time
import os
import sys
import ctypes

# Agregar la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import get_cursor_path  # Asegúrate de que main.py esté en la carpeta padre

# Lista de cursores alternables
cursor_files = [
    get_cursor_path("cursor.cur"),
    get_cursor_path("cursor2.cur"),
]

def set_cursor(cur_path):
    try:
        cursor = ctypes.windll.user32.LoadImageW(
            0, cur_path, 2, 0, 0, 0x00000010
        )
        if cursor:
            ctypes.windll.user32.SetSystemCursor(cursor, 32512)
    except Exception as e:
        print(f"Error cambiando cursor: {e}")

cursor_index = 0
last_change = 0

running = True
while running:
    current_time = time.time()
    if current_time - last_change > 0.5:
        cursor_index = (cursor_index + 1) % len(cursor_files)
        set_cursor(cursor_files[cursor_index])
        last_change = current_time
