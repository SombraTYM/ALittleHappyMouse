import pygame
import random
import time
import sys
import os
import win32api
import win32gui

pygame.init()

# Tamaño real
WIDTH, FINAL_HEIGHT = 400, 300
DURATION = 5
DELAY = 0.1

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
font_base = pygame.font.SysFont("Consolas", 6)

text_color = (255, 255, 255)
outline_color = (0, 0, 0)

fondo_img_original = pygame.image.load(os.path.join(BASE_PATH, "12 sin título_065805.png"))

mensajes = [
    "¡¡¡¿¿¿SISTEM32 SERA IMPOSTANTE???!!!",
    "SOLO MUERETE",
    "ERROR 0x0000B0SS",
    "¿¿¿TE ESTAS ESTRESANDO???",
    "NO TE LIBRARAS DE MI",
    "¡¡ERES UN IDIOTA!!",
    "SOLO RINDETE",
    "*DESTRUYENDO ARCHIVOS*"
]

screen_w = win32api.GetSystemMetrics(0)
screen_h = win32api.GetSystemMetrics(1)

def render_text_with_outline(font, message, text_color, outline_color):
    base = font.render(message, True, text_color)
    outline = font.render(message, True, outline_color)
    surf = pygame.Surface((base.get_width() + 4, base.get_height() + 4), pygame.SRCALPHA)

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surf.blit(outline, (dx + 2, dy + 2))
    surf.blit(base, (2, 2))
    return surf

def mostrar_ventana():
    # Crear ventana inicial de altura 1, ancho fijo
    screen = pygame.display.set_mode((WIDTH, 1), pygame.RESIZABLE)
    pygame.display.set_caption("JAJAJAJA")
    hwnd = pygame.display.get_wm_info()["window"]

    # Posición aleatoria con ancho fijo
    x = random.randint(0, screen_w - WIDTH)
    y = random.randint(0, screen_h - FINAL_HEIGHT)
    win32gui.MoveWindow(hwnd, x, y + FINAL_HEIGHT // 2, WIDTH, 1, True)

    # Animación de crecimiento SOLO EN Y
    for i in range(1, 21):
        h = int(FINAL_HEIGHT * (i / 20))
        screen = pygame.display.set_mode((WIDTH, h), pygame.RESIZABLE)
        win32gui.MoveWindow(hwnd, x, y + (FINAL_HEIGHT - h) // 2, WIDTH, h, True)
        pygame.display.flip()
        time.sleep(0.01)

    # Mostrar contenido
    mensaje = random.choice(mensajes)
    start_time = time.time()
    running = True

    while running and time.time() - start_time < DURATION:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        w, h = pygame.display.get_surface().get_size()
        fondo_scaled = pygame.transform.scale(fondo_img_original, (w, h))
        screen.blit(fondo_scaled, (0, 0))

        font_scaled = pygame.font.SysFont("Consolas", max(12, int(h * 0.08)))
        texto_con_borde = render_text_with_outline(font_scaled, mensaje, text_color, outline_color)
        rect = texto_con_borde.get_rect(center=(w // 2, h // 2))
        screen.blit(texto_con_borde, rect)

        pygame.display.flip()
        time.sleep(0.05)

    # Animación de cierre SOLO EN Y
    for i in range(20, 0, -1):
        h = int(FINAL_HEIGHT * (i / 20))
        screen = pygame.display.set_mode((WIDTH, h), pygame.RESIZABLE)
        win32gui.MoveWindow(hwnd, x, y + (FINAL_HEIGHT - h) // 2, WIDTH, h, True)
        pygame.display.flip()
        time.sleep(0.01)

    pygame.display.quit()

# Bucle principal
try:
    while True:
        mostrar_ventana()
        time.sleep(DELAY)
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()
