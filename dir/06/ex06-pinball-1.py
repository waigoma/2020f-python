# 問題[1]

from tkinter import *
from dataclasses import dataclass, field
import time

# 定数定義
GRAVITY = 2

BOX_LEFT = 100  # ゲーム領域の左端
BOX_TOP = 100  # ゲーム領域の上位置
BOX_WIDTH = 300  # ゲーム領域の幅
BOX_HEIGHT = 300  # ゲーム領域の高さ

BALL_INITIAL_X = BOX_LEFT + 100  # ボールの最初のX位置
BALL_INITIAL_Y = BOX_TOP + 20  # ボールの最初のY位置
BALL_DIAMETER = 10  # ボールの直径
BALL_X_SPEED = 0  # ボールのスピード
BALL_Y_SPEED = 0  # ボールのスピード

DURATION = 0.05  # アニメーションのスピード

PADDLE_WIDTH = 50  # パドルの幅
PADDLE_HEIGHT = 20  # パドルの高さ
PADDLE_START_POS = 278  # パドルの最初の位置

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 100  # キャンバスの大きさ
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT + 100

timing = 0


@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vx: int
    vy: int
    timer: int
    falling: bool

    def move(self, vy):  # ボールを動かす
        ball_y = self.y
        self.vy += vy
        self.y += self.vy

        if self.y - ball_y > 0 and not self.falling:
            self.falling = True
            self.timer = 0
            self.vy = 0
        elif self.y - ball_y < 0 and self.falling:
            self.falling = False

    def redraw(self):  # ボールの再描画
        canvas.coords(self.id, self.x, self.y, self.x + self.d, self.y + self.d)


@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    dx: int = field(init=False, default=0)

    def move(self):  # パドルを動かす
        self.x += self.dx

    def redraw(self):  # パドルの再描画
        canvas.coords(self.id, self.x, self.y, self.x + self.w, self.y + self.h)

    def collision(self, __box, ball):
        global timing
        if ((ball.x + ball.d >= self.x) and (ball.x < self.x + self.w)) and (self.y + self.h > ball.y + ball.d >= self.y) and timing > 2:
            timing = 0
            ball.vy = -ball.vy
            ball.timer = 20
            ball.falling = False


@dataclass
class Box:
    id: int
    west: int
    north: int
    east: int
    south: int
    balls: list
    duration: float
    paddle: Paddle

    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.duration = duration
        self.paddle = None
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")

    def create_ball(self, x, y, d, vx, vy, timer, falling):  # ボールを生成し、初期描画する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vx, vy, timer, falling)

    def set_balls(self, n):
        for x in range(n):
            ball = self.create_ball(BALL_INITIAL_X, BALL_INITIAL_Y + 20 * x + BALL_DIAMETER, BALL_DIAMETER, BALL_X_SPEED, BALL_Y_SPEED, 0, True)
            self.balls.append(ball)

    def create_paddle(self, x, y, w, h):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")
        return Paddle(id, x, y, w, h)

    def set_paddle(self):
        self.paddle = self.create_paddle(
            self.east - PADDLE_WIDTH - 168,
            self.north + PADDLE_START_POS,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )

    def check_wall(self, ball):
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = - ball.vx
        if ball.y + ball.d >= self.south:
            ball.vy = -ball.vy
            ball.timer = 20
            ball.falling = False

    def animate(self):
        global timing
        for x in range(1000):  # iterate 100 times
            for ball in self.balls:
                ball.timer += 1
                vy = GRAVITY * ball.timer / 100
                ball.move(vy)
                self.check_wall(ball)
                self.paddle.collision(box, ball)
                ball.redraw()
            timing += 1
            self.paddle.move()
            self.paddle.redraw()
            time.sleep(self.duration)
            tk.update()


# main
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)

box.set_balls(1)
box.set_paddle()
box.animate()
tk.mainloop()
