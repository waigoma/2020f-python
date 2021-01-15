# 問題[1]

import pygame
from dataclasses import dataclass

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


@dataclass
class Flower:
    x: int
    y: int
    flowerColor: str


def draw_flower_at(pos_x, pos_y, flower):
    flowerLeft_x = flower.x / 2
    flowerLeft_y = flower.y
    flowerRight_x = flower.x * 2
    flowerRight_y = flower.y
    flowerDown_x = (flowerRight_x + flowerLeft_x) / 2
    flowerDown_y = flower.y * 1.75

    flower1Left_x = flowerLeft_x
    flower1Left_y = flower.y
    flower1Right_x = flowerDown_x
    flower1Right_y = flower.y
    flower1Top_x = (flower1Right_x + flower1Left_x) / 2
    flower1Top_y = flower.y / 1.5

    flower2Left_x = flowerDown_x
    flower2Left_y = flower.y
    flower2Right_x = flowerRight_x
    flower2Right_y = flower.y
    flower2Top_x = (flower2Right_x + flower2Left_x) / 2
    flower2Top_y = flower.y / 1.5

    flower3Left_x = flower1Top_x
    flower3Left_y = flower.y
    flower3Right_x = flower2Top_x
    flower3Right_y = flower.y
    flower3Top_x = flowerDown_x
    flower3Top_y = flower.y / 1.5

    list1 = [[flowerDown_x + pos_x, flowerDown_y + pos_y], [flowerLeft_x + pos_x, flowerLeft_y + pos_y], [flowerRight_x + pos_x, flowerRight_y + pos_y]]
    list2 = [[flower1Left_x + pos_x, flower1Left_y + pos_y], [flower1Right_x + pos_x, flower1Right_y + pos_y], [flower1Top_x + pos_x, flower1Top_y + pos_y]]
    list3 = [[flower2Left_x + pos_x, flower2Left_y + pos_y], [flower2Right_x + pos_x, flower2Right_y + pos_y], [flower2Top_x + pos_x, flower2Top_y + pos_y]]
    list4 = [[flower3Left_x + pos_x, flower3Left_y + pos_y], [flower3Right_x + pos_x, flower3Right_y + pos_y], [flower3Top_x + pos_x, flower3Top_y + pos_y]]

    pygame.draw.polygon(screen, flower.flowerColor, list1, width=0)
    pygame.draw.polygon(screen, flower.flowerColor, list2, width=0)
    pygame.draw.polygon(screen, flower.flowerColor, list3, width=0)
    pygame.draw.polygon(screen, flower.flowerColor, list4, width=0)


screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('ex12-1-flowers')

flowers = [Flower(200, 200, "red"), Flower(100, 100, "red"), Flower(50, 50, "red"), Flower(20, 20, "red")]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    screen.fill(WHITE)
    i = 0
    for flower in flowers:
        draw_flower_at(0 + i * 100, 0, flower)
        i += 1

    pygame.display.update()
    clock.tick(FPS)
