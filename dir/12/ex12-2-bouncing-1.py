# 問題[2-1]

import pygame
from dataclasses import dataclass

FPS = 60
GRAVITY = 9

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

falling = True


@dataclass
class Ball:
    x: int
    y: int
    vx: int
    vy: int


def draw_ball(__screen, ball_cl, __vy):
    global falling, timer
    ballY = ball_cl.y

    ball_cl.x += ball_cl.vx
    ball_cl.y += ball_cl.vy + __vy

    x = ball_cl.x
    y = ball_cl.y

    if ball_cl.y - ballY > 0 and not falling:
        falling = True
        timer = -1
        ball_cl.vy = 0

    return pygame.draw.circle(__screen, BLACK, [x, y], 10, width=0)


screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('ex12-2-bouncing-1')

ball_c = Ball(100, 100, 2, 0)
timer = -1

while True:
    timer += 1
    vy = GRAVITY * timer/100
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    left = pygame.draw.rect(screen, BLACK, (50, 50, 2, 500), width=0)
    right = pygame.draw.rect(screen, BLACK, (550, 50, 2, 500), width=0)
    top = pygame.draw.rect(screen, BLACK, (50, 50, 500, 2), width=0)
    bottom = pygame.draw.rect(screen, BLACK, (50, 550, 502, 2), width=0)

    ball = draw_ball(screen, ball_c, vy)

    if ball.colliderect(left) or ball.colliderect(right):
        ball_c.vx = -ball_c.vx

    if ball.colliderect(top) or ball.colliderect(bottom):
        falling = False
        ball_c.vy = -vy
        timer = -1

    pygame.display.update()
    clock.tick(FPS)
