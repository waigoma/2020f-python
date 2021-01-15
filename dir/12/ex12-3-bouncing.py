# 問題[3]

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
    global falling, timer, img_rect
    ballY = img_rect.top

    img_rect.left += ball_cl.vx
    img_rect.top += ball_cl.vy + __vy

    x = img_rect.left
    y = img_rect.top

    if img_rect.top - ballY > 0 and not falling:
        falling = True
        timer = 10
        ball_cl.vy = 0

    return __screen.blit(img, img_rect)


screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
pygame.display.set_caption('ex12-3-bouncing')

bg = pygame.image.load("bg1.jpg")
img = pygame.image.load("b.png")
img_rect = img.get_rect()
img_rect.topleft = (100, 400)

ball_c = Ball(100, 100, 2, 0)
timer = -1

while True:
    timer += 1
    vy = GRAVITY * timer/100
    screen.fill(WHITE)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    left = pygame.draw.rect(screen, BLACK, (50, 50, 2, 900), width=0)
    right = pygame.draw.rect(screen, BLACK, (950, 50, 2, 900), width=0)
    top = pygame.draw.rect(screen, BLACK, (50, 50, 900, 2), width=0)
    bottom = pygame.draw.rect(screen, BLACK, (50, 950, 902, 2), width=0)

    ball = draw_ball(screen, ball_c, vy)

    if ball.colliderect(left) or ball.colliderect(right):
        ball_c.vx = -ball_c.vx
        img = pygame.transform.flip(img, True, False)

    if ball.colliderect(top) or ball.colliderect(bottom):
        falling = False
        ball_c.vy = -vy
        timer = 10

    pygame.display.update()
    clock.tick(FPS)
