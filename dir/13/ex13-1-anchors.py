# 13-問題[1]

import pygame
from dataclasses import dataclass

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.font.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('ex13-1-anchors')

font = pygame.font.SysFont("Consolas.tff", 24)

texts = [
    [font.render("NW", True, BLACK), (5, 5)],
    [font.render("N", True, BLACK), (280, 5)],
    [font.render("NE", True, BLACK), (575, 5)],
    [font.render("W", True, BLACK), (5, 280)],
    [font.render("Center", True, BLACK), (265, 280)],
    [font.render("E", True, BLACK), (580, 280)],
    [font.render("SW", True, BLACK), (5, 580)],
    [font.render("S", True, BLACK), (280, 580)],
    [font.render("SE", True, BLACK), (575, 580)],
]

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    for text in texts:
        screen.blit(text[0], text[1])

    pygame.display.update()
    clock.tick(FPS)
