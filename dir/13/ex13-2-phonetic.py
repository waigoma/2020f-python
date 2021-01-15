# 13-問題[2]

import pygame
from dataclasses import dataclass

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.font.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('ex13-2-phonetic')

font = pygame.font.SysFont("Consolas.tff", 24)

text = font.render("Default", True, BLACK)

phonetic_code = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOXTROT", "GOLF", "HOTEL"]

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                text = font.render(phonetic_code[0], True, BLACK)
            if event.key == pygame.K_b:
                text = font.render(phonetic_code[1], True, BLACK)
            if event.key == pygame.K_c:
                text = font.render(phonetic_code[2], True, BLACK)
            if event.key == pygame.K_d:
                text = font.render(phonetic_code[3], True, BLACK)
            if event.key == pygame.K_e:
                text = font.render(phonetic_code[4], True, BLACK)
            if event.key == pygame.K_f:
                text = font.render(phonetic_code[5], True, BLACK)
            if event.key == pygame.K_g:
                text = font.render(phonetic_code[6], True, BLACK)
            if event.key == pygame.K_h:
                text = font.render(phonetic_code[7], True, BLACK)

    text_rect = text.get_rect()
    text_rect.center = (600/2, 600/2)
    screen.blit(text, text_rect)

    # screen.blit(text, (265, 280))

    pygame.display.update()
    clock.tick(FPS)
