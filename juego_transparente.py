import pygame
import random
import math
import time
import os
import ctypes
import win32con
import win32gui
import subprocess
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
python_path = sys.executable

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Virus Bichito Game - Transparente")

hwnd = pygame.display.get_wm_info()["window"]
extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extended_style | 0x80000 | 0x20)
win32gui.SetLayeredWindowAttributes(hwnd, 0x000000, 255, win32con.LWA_COLORKEY)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 36)  # Fuente para cronómetro

player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
player_size = 20
enemies = []
spawn_interval = 2
last_spawn_time = time.time()
bullet_speed = 3
speed_increase = 0.3
bullets_per_wave = 3
max_bullets = 9
start_time = time.time()
duration = 70  # Cambiar a 150 para versión final
showing_bsod = False

class Enemy:
    def __init__(self, target_pos, speed):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 15
        self.spawn_time = time.time()
        self.state = "waiting"
        self.offscreen_time = None
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        dist = math.hypot(dx, dy)
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def update(self):
        if self.state == "waiting":
            if time.time() - self.spawn_time >= 1:
                self.state = "moving"
        elif self.state == "moving":
            self.x += self.vx
            self.y += self.vy
            if not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT):
                if self.offscreen_time is None:
                    self.offscreen_time = time.time()
                elif time.time() - self.offscreen_time >= 1:
                    return False
        return True

def show_bsod():
    bsod_path = os.path.join(BASE_PATH, "bsod.png")
    if not os.path.exists(bsod_path):
        return
    bsod_image = pygame.image.load(bsod_path)
    bsod_image = pygame.transform.scale(bsod_image, (WIDTH, HEIGHT))
    bsod_screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("BSOD")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        bsod_screen.blit(bsod_image, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

paused = False
terminal_60 = False
terminal_30 = False
boss_started = False
running = True

while running:
    elapsed = time.time() - start_time
    remaining = duration - elapsed

    if remaining <= 60 and not terminal_60:
        paused = True
        subprocess.call([python_path, os.path.join(BASE_PATH, "ventana_alerta.py"), "60"])
        terminal_60 = True
        paused = False
        subprocess.Popen([python_path, os.path.join(BASE_PATH, "boss_attacks.py")])

    if remaining <= 30 and not terminal_30:
        paused = True
        subprocess.call([python_path, os.path.join(BASE_PATH, "ventana_alerta.py"), "30"])
        terminal_30 = True
        paused = False

    if remaining <= 0:
        showing_bsod = True

    if showing_bsod:
        show_bsod()
        running = False
        break

    if paused:
        continue

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos[1] -= player_speed
    if keys[pygame.K_s]: player_pos[1] += player_speed
    if keys[pygame.K_a]: player_pos[0] -= player_speed
    if keys[pygame.K_d]: player_pos[0] += player_speed
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    pygame.draw.rect(screen, (0, 255, 0), (*player_pos, player_size, player_size))

    if time.time() - last_spawn_time >= spawn_interval:
        bullet_speed += speed_increase
        bullets_per_wave = min(bullets_per_wave + 1, max_bullets)
        for _ in range(bullets_per_wave):
            enemies.append(Enemy(player_pos[:], bullet_speed))
        last_spawn_time = time.time()

    new_enemies = []
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for enemy in enemies:
        if enemy.update():
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
            if enemy.state == "moving" and player_rect.colliderect(enemy_rect):
                showing_bsod = True
                break
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, enemy.size, enemy.size))
            new_enemies.append(enemy)
    enemies = new_enemies

    # ⏱ Cronómetro visible
    minutos = int(remaining // 60)
    segundos = int(remaining % 60)
    tiempo_texto = f"{minutos:02d}:{segundos:02d}"
    texto_surface = font.render(tiempo_texto, True, (255, 255, 255))
    screen.blit(texto_surface, (WIDTH - 120, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
