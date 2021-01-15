# 問題[4]

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

BLOCK_WIDTH = 40   # ブロックの幅
BLOCK_HEIGHT = 10  # ブロックの高さ
BLOCK_GAP = 20     # ブロックの間隔
BLOCK_LEFT = 80     # 最初のブロックの位置(左)
BLOCK_TOP = 75      # 最初のブロックの位置(上)

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 100  # キャンバスの大きさ
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT + 100

BLOCK_ROWS = 3   # ブロックの列数
BLOCK_COLS = 1   # １列のブロックの数

timing = 0


@dataclass
class MovingObject:
    id: int
    x: int
    y: int
    w: int
    h: int
    d: int
    vx: int
    vy: int
    timer: int
    falling: bool

    def redraw(self):
        canvas.coords(self.id, self.x, self.y, self.x + self.d, self.y + self.d)

    def moveP(self, lefting, righting):  # パドルを動かす
        if lefting:
            self.x -= self.vx
        if righting:
            self.x += self.vx

    def moveB(self, vy):  # ボールを動かす
        ball_y = self.y
        self.vy += vy
        self.x += self.vx
        self.y += self.vy

        if self.y - ball_y > 0 and not self.falling:
            self.falling = True
            self.timer = 0
            self.vy = 0
        elif self.y - ball_y < 0 and self.falling:
            self.falling = False


class Ball(MovingObject):
    def __init__(self, id, x, y, d, vx, vy, timer, falling):
        super().__init__(id, x, y, 0, 0, d, vx, vy, timer, falling)


class Paddle(MovingObject):
    def __init__(self, id, x, y, w, h, dx):
        super().__init__(id, x, y, w, h, 0, dx, 0, 0, False)

    def redraw(self):
        canvas.coords(self.id, self.x, self.y, self.x + self.w, self.y + self.h)


@dataclass
class Block:
    id: int
    x: int
    y: int
    w: int
    h: int

    def delete(self):
        canvas.delete(self.id)


@dataclass
class Box:
    id: int
    west: int
    north: int
    east: int
    south: int
    balls: list
    blocks: list
    duration: float
    paddle: Paddle
    lefting: bool = field(init=False, default=False)
    righting: bool = field(init=False, default=False)

    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.blocks = []
        self.duration = duration
        self.paddles = []
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")

    def create_ball(self, x, y, d, vx, vy, timer, falling):  # ボールを生成し、初期描画する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vx, vy, timer, falling)

    def set_balls(self, n):
        for x in range(n):
            ball = self.create_ball(BALL_INITIAL_X, BALL_INITIAL_Y + 20 * x + BALL_DIAMETER, BALL_DIAMETER,
                                    BALL_X_SPEED, BALL_Y_SPEED, 0, True)
            self.balls.append(ball)

    def create_block(self, x, y, w, h):   # ブロックを初期表示し、戻す。
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="red", outline="red")
        return Block(id, x, y, w, h)

    def set_blocks(self, rows, cols):    # ブロックを生成し、属性値を保持
        for row in range(rows):
            for col in range(cols):
                block = self.create_block(
                    self.west + BLOCK_LEFT + col * (BLOCK_WIDTH + BLOCK_GAP),
                    self.north + BLOCK_TOP + row * (BLOCK_HEIGHT + BLOCK_GAP),
                    BLOCK_WIDTH, BLOCK_HEIGHT
                )
                self.blocks.append(block)

    def create_paddle(self, x, y, w, h):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")
        return Paddle(id, x, y, w, h, 10)

    def set_paddle(self):
        paddle = self.create_paddle(
            self.east - PADDLE_WIDTH - 168,
            self.north + PADDLE_START_POS,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )
        self.paddles.append(paddle)

    def check_wall(self, ball):
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = - ball.vx
        if ball.y + ball.d >= self.south:
            ball.vy = -ball.vy
            ball.timer = 20
            ball.falling = False

    def check_blocks(self, ball):  # ブロックを消す
        center = ball.y + ball.d/2
        for block in self.blocks:
            if block.y <= center <= block.y + block.h:
                if ball.x <= block.x + block.w:
                    ball.vx = - ball.vx
                    block.delete()
                    ball.vy = -ball.vy
                    ball.timer = 20
                    ball.falling = False
                    self.blocks.remove(block)

    def check_paddle(self, ball):
        global timing
        for paddle in self.paddles:
            if ((ball.x + ball.d >= paddle.x) and (ball.x < paddle.x + paddle.w)) and (paddle.y + paddle.h > ball.y + ball.d >= paddle.y) and timing > 2:
                timing = 0
                ball.vy = -ball.vy
                ball.timer = 20
                ball.falling = False

    def animate(self):
        global timing
        for x in range(1000):
            for ball in self.balls:
                ball.timer += 1
                vy = GRAVITY * ball.timer / 100
                ball.moveB(vy)
                self.check_wall(ball)
                self.check_blocks(ball)
                self.check_paddle(ball)
                ball.redraw()

            for paddle in self.paddles:
                paddle.moveP(self.lefting, self.righting)
                paddle.redraw()
            time.sleep(self.duration)
            timing += 1
            tk.update()

    def press_left(self, e):
        self.lefting = True

    def press_right(self, e):
        self.righting = True

    def release_left(self, e):
        self.lefting = False

    def release_right(self, e):
        self.righting = False


# main
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)

# Left
tk.bind_all('<KeyPress-Left>', box.press_left)
tk.bind_all('<KeyRelease-Left>', box.release_left)

# Right
tk.bind_all('<KeyPress-Right>', box.press_right)
tk.bind_all('<KeyRelease-Right>', box.release_right)

box.set_balls(1)
box.set_paddle()
box.set_blocks(BLOCK_ROWS, BLOCK_COLS)
box.animate()
tk.mainloop()
