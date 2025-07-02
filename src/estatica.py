import pygame
import random
import os
import time
import sys

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Agregar la ruta al main
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_PATH, "..")))
from main import get_audio_path

# Pantalla completa sin bordes
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
pygame.display.set_caption("Estática")

clock = pygame.time.Clock()

# Cargar audio usando la función del main
audio_path = get_audio_path("sonido-de-microondas-saturado-.mp3")
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()

# Bucle visual de la estática
while pygame.mixer.music.get_busy():
    for y in range(0, info.current_h, 4):
        for x in range(0, info.current_w, 4):
            color = (255, 255, 255) if random.random() > 0.5 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x, y, 4, 4))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
