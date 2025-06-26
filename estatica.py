import pygame
import random
import time
import os
import sys

pygame.init()
pygame.mixer.init()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
python_path = sys.executable

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
pygame.display.set_caption("Estática")

clock = pygame.time.Clock()

# Carga y reproduce el audio
audio_path = os.path.join(BASE_PATH, "sonido-de-microondas-saturado-.mp3")
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    for y in range(0, info.current_h, 4):
        for x in range(0, info.current_w, 4):
            color = (255, 255, 255) if random.random() > 0.5 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x, y, 4, 4))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
