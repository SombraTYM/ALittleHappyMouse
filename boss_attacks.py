import time
import os
import sys
import ctypes

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

cursor_files = [
    os.path.join(BASE_PATH, "cursor.cur"),
    os.path.join(BASE_PATH, "cursor2.cur"),
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
    time.sleep(0.1)
