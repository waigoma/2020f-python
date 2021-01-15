# 課題[2]
from tkinter import *
from dataclasses import dataclass
import time

DURATION = 1
GRAVITY = 8.0
REFLECTION = .5

timer = 0.0
count = 0

first = True


@dataclass
class Ball:
    id: int
    x: float
    y: float
    d: float
    vx: float
    vy: float
    c: str


@dataclass
class Border:
    left: float
    right: float
    top: float
    bottom: float


def make_ball(x, y, d, vx, vy, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d, fill=c, outline=c)
    return Ball(id, x, y, d, vx, vy, c)


def move_ball(ball, vy1=0.0):
    ball.x += ball.vx
    ball.y += ball.vy + vy1


def make_wall(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)


def redraw_ball(ball):
    canvas.coords(ball.id, ball.x, ball.y, ball.x + ball.d, ball.y + ball.d)


tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

border = Border(100, 700, 100, 500)

make_wall(border.left, border.top, border.right - border.left, border.bottom - border.top)

ball = make_ball(150, 150, 30, 0, 0, "darkblue")

# 自由落下 v = gt
# 跳ね返り = 1 -> 跳ね返った時に減衰がない
# 下の地面にぶつかった時、そのぶつかった時の速度vを上への加速度とする(マイナス付けて反転)

while True:
    timer += DURATION
    vy = GRAVITY * timer/100

    if ball.x + ball.vx < border.left or ball.x + ball.d >= border.right:
        ball.vx = -ball.vx
    if ball.y + ball.d >= border.bottom:

        if 1 <= count <= 2:
            timer -= (1 * count)
        elif count > 2:
            timer -= 2

        vy = GRAVITY * timer/100

        if first:
            ball.vy = -vy * REFLECTION
            first = False
        else:
            ball.vy = (-vy / 2) * REFLECTION

        vy = 0
        move_ball(ball)
        timer = 0
        count += 1

    if ball.vy > 0:
        ball.y = border.bottom - ball.d

    move_ball(ball, vy)

    redraw_ball(ball)

    tk.update()
    time.sleep(DURATION/100)
