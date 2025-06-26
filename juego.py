import pygame
import random
import math
import time
import os
import subprocess
import sys
import win32api

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
python_path = sys.executable

try:
    import win32gui
except ImportError:
    win32gui = None

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus Bichito Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 30)

player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
player_size = 20

enemies = []
spawn_interval = 2
last_spawn_time = time.time()
bullet_speed = 3
speed_increase = 0.3
max_speed = 12  # límite velocidad
bullets_per_wave = 3
max_bullets = 12

start_time = time.time()
duration = 150  # 3 minutos

ventana_pos_original = None
last_move = 0
last_invert_time = 0  # cooldown para inversión colores

def mover_ventana_random():
    if not win32gui:
        return
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    x = random.randint(0, screen_width - WIDTH)
    y = random.randint(0, screen_height - HEIGHT)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.MoveWindow(hwnd, x, y, WIDTH, HEIGHT, True)
    return (x, y)

def aplicar_vibracion(hwnd, base_pos, intensidad=5):
    dx = random.randint(-intensidad, intensidad)
    dy = random.randint(-intensidad, intensidad)
    x = base_pos[0] + dx
    y = base_pos[1] + dy
    win32gui.MoveWindow(hwnd, x, y, WIDTH, HEIGHT, True)

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

running = True
hwnd = None
if win32gui:
    hwnd = pygame.display.get_wm_info()["window"]

while running:
    elapsed = time.time() - start_time
    remaining = duration - elapsed

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos[1] -= player_speed
    if keys[pygame.K_s]: player_pos[1] += player_speed
    if keys[pygame.K_a]: player_pos[0] -= player_speed
    if keys[pygame.K_d]: player_pos[0] += player_speed

    pygame.draw.rect(screen, (0, 255, 0), (*player_pos, player_size, player_size))

    if time.time() - last_spawn_time >= spawn_interval:
        bullet_speed = min(bullet_speed + speed_increase, max_speed)
        bullets_per_wave = min(bullets_per_wave + 1, max_bullets)

        espacio_disponible = max_bullets - len(enemies)
        nuevos_a_crear = min(bullets_per_wave, espacio_disponible)

        for _ in range(nuevos_a_crear):
            enemies.append(Enemy(player_pos[:], bullet_speed))

        last_spawn_time = time.time()

    new_enemies = []
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for enemy in enemies:
        if enemy.update():
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
            if enemy.state == "moving" and player_rect.colliderect(enemy_rect):
                pygame.quit()
                time.sleep(0.5)
                subprocess.call([python_path, os.path.join(BASE_PATH, "alerta.py")])
                subprocess.call([python_path, os.path.join(BASE_PATH, "estatica.py")])
                subprocess.call([python_path, os.path.join(BASE_PATH, "juego_transparente.py")])
                exit()
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, enemy.size, enemy.size))
            new_enemies.append(enemy)
    enemies = new_enemies

    # Cronómetro visual
    min_rest = int(remaining // 60)
    seg_rest = int(remaining % 60)
    tiempo_txt = f"{min_rest:02}:{seg_rest:02}"
    tiempo_surface = font.render(tiempo_txt, True, (255, 255, 255))
    screen.blit(tiempo_surface, (WIDTH - 110, 20))

    # Mover ventana aleatoriamente cada 2 seg si quedan menos de 2 min
    if win32gui and remaining <= 130:
        if time.time() - last_move >= 2:
            ventana_pos_original = mover_ventana_random()
            last_move = time.time()

    # Aplicar vibración suave en la ventana si quedan menos de 2 minutos
    if win32gui and remaining <= 120 and hwnd and ventana_pos_original:
        aplicar_vibracion(hwnd, ventana_pos_original, intensidad=5)

    # Invertir colores si quedan menos de 1:10, con cooldown de 1 seg
    if remaining <= 110:
        if time.time() - last_invert_time >= 1:
            inverted_surface = pygame.Surface((WIDTH, HEIGHT))
            for x in range(WIDTH):
                for y in range(HEIGHT):
                    pixel = screen.get_at((x, y))
                    inverted_color = pygame.Color(255 - pixel.r, 255 - pixel.g, 255 - pixel.b, pixel.a)
                    inverted_surface.set_at((x, y), inverted_color)
            screen.blit(inverted_surface, (0, 0))
            last_invert_time = time.time()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
