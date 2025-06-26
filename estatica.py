import pygame
import random
import time

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
pygame.display.set_caption("Estática")

clock = pygame.time.Clock()

start_time = time.time()
duration = 3

while time.time() - start_time < duration:
    for y in range(0, info.current_h, 4):
        for x in range(0, info.current_w, 4):
            color = (255, 255, 255) if random.random() > 0.5 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x, y, 4, 4))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
