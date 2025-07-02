import pygame
import time
import os
import win32api
import win32gui
import random

pygame.init()
pygame.mixer.init()

# Tamaño ventana
WIDTH, HEIGHT = 250, 150
COLOR = (0, 255, 0)  # Verde 

# Sonido de rebote
rebote_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "rebote de coso ese.mp3"))

# Crear ventana sin marco
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
hwnd = pygame.display.get_wm_info()["window"]

# Tamaño de la pantalla
screen_w = win32api.GetSystemMetrics(0)
screen_h = win32api.GetSystemMetrics(1)

# Posición inicial random
x = random.randint(0, screen_w - WIDTH)
y = random.randint(0, screen_h - HEIGHT)
dx = 3
dy = 3

def dibujar():
    screen.fill(COLOR)
    pygame.display.flip()

# Bucle
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        reboto = False

        x += dx
        y += dy

        if x <= 0 or x + WIDTH >= screen_w:
            dx *= -1
            reboto = True
        if y <= 0 or y + HEIGHT >= screen_h:
            dy *= -1
            reboto = True

        if reboto:
            rebote_sound.play()

        win32gui.MoveWindow(hwnd, x, y, WIDTH, HEIGHT, True)
        dibujar()
        time.sleep(0.01)

except KeyboardInterrupt:
    pygame.quit()
