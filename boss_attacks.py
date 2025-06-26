import threading
import time
import subprocess
import sys
import os
import random

BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

class BossAttacks:
    def __init__(self, game_duration=150):
        self.running = True
        self.game_duration = game_duration
        self.start_time = time.time()
        self.paused = False
        self.terminal_60_done = False
        self.terminal_30_done = False
        self.last_boss_spawn = 0
        self.boss_spawn_interval = 10

    def ventana_boss(self):
        while self.running:
            # Solo lanzar ventanas boss si no está pausado y boss activo
            if not self.paused and (time.time() - self.start_time) >= (self.game_duration - 60):
                if time.time() - self.last_boss_spawn >= self.boss_spawn_interval:
                    subprocess.Popen([sys.executable, os.path.join(BASE_PATH, "ventana_boss.py")])
                    self.last_boss_spawn = time.time()
            time.sleep(1)

    def terminal_60(self):
        # Espera para lanzar la terminal 60s restante
        while self.running:
            elapsed = time.time() - self.start_time
            remaining = self.game_duration - elapsed
            if remaining <= 60 and not self.terminal_60_done:
                self.paused = True
                subprocess.call([sys.executable, os.path.join(BASE_PATH, "terminal_attack_60.py")])
                self.terminal_60_done = True
                self.paused = False
            time.sleep(1)

    def terminal_30(self):
        # Espera para lanzar la terminal 30s restante
        while self.running:
            elapsed = time.time() - self.start_time
            remaining = self.game_duration - elapsed
            if remaining <= 30 and not self.terminal_30_done:
                self.paused = True
                subprocess.call([sys.executable, os.path.join(BASE_PATH, "terminal_attack_30.py")])
                self.terminal_30_done = True
                self.paused = False
            time.sleep(1)

    def cursor_attack(self):
        # Aquí podrías poner el loop para cambiar cursor emojis progresivamente
        # Placeholder: sólo duerme
        while self.running:
            if not self.paused:
                # Cambiar cursor acá (no implementado)
                pass
            time.sleep(0.5)

    def start(self):
        threading.Thread(target=self.ventana_boss, daemon=True).start()
        threading.Thread(target=self.terminal_60, daemon=True).start()
        threading.Thread(target=self.terminal_30, daemon=True).start()
        threading.Thread(target=self.cursor_attack, daemon=True).start()

if __name__ == "__main__":
    boss = BossAttacks()
    boss.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        boss.running = False
