# 問題[4]
from tkinter import *
from dataclasses import dataclass
import time

DURATION = 1
GRAVITY = 8.0

timer = 0
count = 0

bouncingTop = False
falling = True
lefting = True

left = False
right = False

first = True

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
    x: float
    y: float
    width: float
    height: float
    c: str


# make
def make_ball(x, y, d, vx, vy, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d, fill=c, outline=c)
    return Ball(id, x, y, d, vx, vy, c)


def make_paddle(x, y, width, height, c="black"):
    id = canvas.create_rectangle(x, y, x + width, y + height, fill=c, outline=c)
    return Paddle(id, x, y, width, height, c)


# move
def move_ball(ball, vy):
    global falling, timer, lefting, first
    ballY = ball.y
    ballX = ball.x

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
    if first:
        first = False
        if ball.x - ballX > 0 and lefting:
            lefting = False
        elif ball.x - ballX < 0 and not lefting:
            lefting = True


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


# Collision Detection
def box_collision(ball):
    global lefting, exiting
    # もしボールが左右の壁に当たったら
    if ball.x + ball.vx < border.left or ball.x + ball.d >= border.right:
        # ボールのx方向の速度を反転し跳ね返ったかのように見せる
        lefting = not lefting
        ball.vx = -ball.vx

    # もし天井に当たったら
    if ball.y + ball.vy < border.top:
        # 天井に当たった時の処理
        bouncingY(ball, True, 1)

    # もし床に当たったら
    if ball.y + ball.d >= border.bottom:
        # ボールが床についても下に行こうとしていたら止める
        if ball.vy > 0:
            ball.y = border.bottom - ball.d

        # 床に当たった時の処理
        print("Game Over!")
        exiting = True
        bouncingY(ball, False, 1)


def paddle_collision(ball, paddle, obj):
    if paddle.x + paddle.width >= obj.x and paddle.x <= obj.x + obj.width:
        # obj左壁の当たり判定
        if paddle.x + paddle.width >= obj.x > paddle.x:
            paddle.x = obj.x - paddle.width - 1
        # obj右壁の当たり判定
        elif obj.x + obj.width >= paddle.x > obj.x:
            paddle.x = obj.x + obj.width + 1

    if paddle.x + paddle.width > border.right:
        paddle.x = border.right - paddle.width - 1
    if paddle.x < border.left:
        paddle.x = border.left + 1

    if paddle.x + paddle.width > ball.x + ball.vx > paddle.x and paddle.y + paddle.height > ball.y + ball.d >= paddle.y:
        bouncingY(ball, False, 1.1)


def obj_collision(ball, obj):
    global falling, lefting, count
    if (obj.x <= ball.x <= obj.x + obj.width or obj.x <= ball.x + ball.d <= obj.x + obj.width) and (obj.y <= ball.y <= obj.y + obj.height or obj.y <= ball.y + ball.d <= obj.y + obj.height):
        # obj上壁の当たり判定
        if ball.y + ball.d >= obj.y and falling:
            print("ue")
            bouncingY(ball, False, .9)
        # obj下壁の当たり判定
        elif obj.y + obj.height < ball.y and not falling:
            print("shita")
            bouncingY(ball, True, .9)
        # obj左壁の当たり判定
        elif ball.x + ball.d >= obj.x and not lefting and count > 10:
            print("hidari")
            ball.vx = -ball.vx
            lefting = True
            count = 0
        # obj右壁の当たり判定
        elif ball.x <= obj.x + obj.width and lefting and count > 10:
            print("migi")
            ball.vx = -ball.vx
            lefting = False
            count = 0


# draw wall and objects
def make_wall(ox, oy, width, height, c=None):
    canvas.create_rectangle(ox, oy, ox + width, oy + height, fill=c)


def redraw_ball(ball, paddle):
    canvas.coords(ball.id, ball.x, ball.y, ball.x + ball.d, ball.y + ball.d)
    canvas.coords(paddle.id, paddle.x, paddle.y, paddle.x + paddle.width, paddle.y + paddle.height)


# register key press/release
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


# create canvas
tk = Tk()
canvas = Canvas(tk, width=800, height=800, bd=0)
canvas.pack()
tk.update()

# Key Binds
tk.bind_all('<KeyPress-Left>', press_left)
tk.bind_all('<KeyRelease-Left>', release_left)

tk.bind_all('<KeyPress-Right>', press_right)
tk.bind_all('<KeyRelease-Right>', release_right)

tk.bind_all('<KeyPress-Escape>', press_escape)

# add objects
ball = make_ball(250, 150, 20, 5, 0, "black")

paddle = make_paddle(390, 650, 80, 20, "darkblue")

border = Border(150, 700, 50, 750)
make_wall(border.left, border.top, border.right - border.left, border.bottom - border.top)

walls = [Object(150, 660, 150, 10, "black"), Object(550, 660, 150, 10, "black")]
for obj in walls:
    if obj.c == "none":
        make_wall(obj.x, obj.y, obj.width, obj.height)
        continue
    make_wall(obj.x, obj.y, obj.width, obj.height, obj.c)

objects = [Object(150, 660, 150, 10, "black"), Object(550, 660, 150, 10, "black"),
           Object(500, 200, 50, 50, "darkgreen"), Object(200, 100, 50, 50, "darkgreen"),
           Object(600, 300, 70, 50, "darkgreen"), Object(200, 500, 100, 100, "darkgreen")]
for obj in objects:
    if obj.c == "none":
        make_wall(obj.x, obj.y, obj.width, obj.height)
        continue
    make_wall(obj.x, obj.y, obj.width, obj.height, obj.c)

# main loop
while not exiting:
    count += 1
    timer += DURATION  # timerにDURATIONを足す。DURATIONが整数なのは、誤差を減らすため
    vy = GRAVITY * timer / 100  # 自由落下の公式に当てはめて、その時間の下方向の力を計算

    if not falling and ball.vy > 0:
        ball.y = border.bottom - ball.d

    move_ball(ball, vy)  # ボールを実際に動かす
    move_paddle(paddle)  # パドルを動かす

    # 当たり判定処理係
    box_collision(ball)
    for wall in walls:
        paddle_collision(ball, paddle, wall)
    for obj in objects:
        obj_collision(ball, obj)

    # 再描写
    redraw_ball(ball, paddle)

    tk.update()
    time.sleep(DURATION / 100)

tk.mainloop()
