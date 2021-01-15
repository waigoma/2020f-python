# 問題[3]
from tkinter import *
from dataclasses import dataclass
import time

DURATION = 1
GRAVITY = 8.0

timer = 0

bouncingTop = False
falling = True

left = False
right = False
exiting = False


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
class Paddle:
    id: int
    x: float
    y: float
    width: float
    height: float
    c: str


@dataclass
class Border:
    left: float
    right: float
    top: float
    bottom: float


@dataclass
class Object:
    left: float
    right: float
    top: float
    bottom: float
    color: str


def make_ball(x, y, d, vx, vy, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d, fill=c, outline=c)
    return Ball(id, x, y, d, vx, vy, c)


def make_paddle(x, y, width, height, c="black"):
    id = canvas.create_rectangle(x, y, x + width, y + height, fill=c, outline=c)
    return Paddle(id, x, y, width, height, c)


def move_ball(ball, vy):
    global falling, timer
    ballY = ball.y

    ball.x += ball.vx
    ball.y += ball.vy + vy

    # ボールを動かす前と動かす後を比較して、今現在落下しているのかを判断
    # boolで落ちていなくて、比較では落ちていたら
    if ball.y - ballY > 0 and not falling:
        falling = True
        timer = -1
        ball.vy = 0
    # boolで落ちていて、比較では上昇していたら(多分いらない)
    elif ball.y - ballY < 0 and falling:
        falling = False
        print(falling)


def move_paddle(paddle):
    if left:
        paddle.x -= 5
    elif right:
        paddle.x += 5


def bouncingY(ball, top, reflection):
    global falling, timer, bouncingTop
    vy = GRAVITY * timer/100

    # 落ちてて床だったら
    if falling and not top:
        # 自由落下なら
        if not bouncingTop:
            ball.vy = -vy * reflection
            timer = -1
            falling = False
        # 天井反射なら
        else:
            ball.vy = -(ball.vy + vy) * reflection
            timer = -1
            falling = False
            bouncingTop = False

    # 上昇してて天井だったら
    elif not falling and top:
        ball.vy = -((ball.vy + vy) * reflection)
        timer = -1
        falling = True
        bouncingTop = True


def box_collision(ball):
    # もしボールが左右の壁に当たったら
    if ball.x + ball.vx < border.left or ball.x + ball.d >= border.right:
        # ボールのx方向の速度を反転し跳ね返ったかのように見せる
        ball.vx = -ball.vx

    # もし天井に当たったら
    if ball.y + ball.vy < border.top:
        # 天井に当たった時の処理
        bouncingY(ball, True, .9)

    # もし床に当たったら
    if ball.y + ball.d >= border.bottom:
        # ボールが床についても下に行こうとしていたら止める
        if ball.vy > 0:
            ball.y = border.bottom - ball.d

        # 床に当たった時の処理
        bouncingY(ball, False, .9)


def paddle_collision(ball, paddle):
    global falling
    if paddle.x + paddle.width >= border.right:
        paddle.x = border.right - paddle.width - 1
    if paddle.x < border.left:
        paddle.x = border.left + 1

    if paddle.x + paddle.width > ball.x + ball.vx > paddle.x and paddle.y + paddle.height > ball.y + ball.d >= paddle.y:
        bouncingY(ball, False, 1.2)


def obj_collision(ball, vy):
    # もしボールが左右の壁に当たったら
    if ball.x + ball.vx < border.left or ball.x + ball.d >= border.right:
        # ボールのx方向の速度を反転し跳ね返ったかのように見せる
        ball.vx = -ball.vx

    # もし天井に当たったら
    if ball.y + ball.vy < border.top:
        # 天井に当たった時の処理
        bouncingY(ball, vy, True, .8)

    # もし床に当たったら
    if ball.y + ball.d >= border.bottom:
        # ボールが床についても下に行こうとしていたら止める
        if ball.vy > 0:
            ball.y = border.bottom - ball.d

        # 床に当たった時の処理
        bouncingY(ball, vy, False, 1)


def make_wall(ox, oy, width, height, c=None):
    canvas.create_rectangle(ox, oy, ox + width, oy + height, fill=c)


def redraw_ball(ball, paddle):
    canvas.coords(ball.id, ball.x, ball.y, ball.x + ball.d, ball.y + ball.d)
    canvas.coords(paddle.id, paddle.x, paddle.y, paddle.x + paddle.width, paddle.y + paddle.height)


def press_left(e):
    global left
    left = True


def press_right(e):
    global right
    right = True


def release_left(e):
    global left
    left = False


def release_right(e):
    global right
    right = False


def press_escape(e):
    global exiting
    exiting = True


tk = Tk()
canvas = Canvas(tk, width=800, height=800, bd=0)
canvas.pack()
tk.update()

tk.bind_all('<KeyPress-Left>', press_left)
tk.bind_all('<KeyRelease-Left>', release_left)

tk.bind_all('<KeyPress-Right>', press_right)
tk.bind_all('<KeyRelease-Right>', release_right)

tk.bind_all('<KeyPress-Escape>', press_escape)

ball = make_ball(250, 150, 20, 3, 0, "black")

paddle = make_paddle(550, 650, 100, 30, "darkblue")

border = Border(150, 700, 50, 750)
make_wall(border.left, border.top, border.right - border.left, border.bottom - border.top)

objects = []
for obj in objects:
    if obj.color == "none":
        make_wall(obj.left, obj.top, obj.right - obj.left, obj.bottom - obj.top)
        continue

# 自由落下 v = gt
# 跳ね返り = 1 -> 跳ね返った時に減衰がない
# 下の地面にぶつかった時、そのぶつかった時の速度vを上への加速度とする(マイナス付けて反転)

while True:
    timer += DURATION  # timerにDURATIONを足す。DURATIONが整数なのは、誤差を減らすため
    vy = GRAVITY * timer / 100  # 自由落下の公式に当てはめて、その時間の下方向の力を計算

    if not falling and ball.vy > 0:
        ball.y = border.bottom - ball.d

    move_ball(ball, vy)  # ボールを実際に動かす
    move_paddle(paddle)

    box_collision(ball)
    paddle_collision(ball, paddle)
    # obj_collision(ball, vy)

    redraw_ball(ball, paddle)

    tk.update()
    time.sleep(DURATION / 100)

    if exiting:
        break

tk.mainloop()
