# 問題[2]
import random
import time
from dataclasses import dataclass
from tkinter import *

# 定数
DURATION = 1
GRAVITY = 8.0

# 自由落下計算用(1フレーム += 1)
timer = 0
# 壁あての時のバグ削減用
count = 0

# ポイント
points = 0
adpoints = 0

# エネルギーバーの左右幅
energy_width = 0

# 上から跳ね返ったか否か
bouncingTop = False
# 現在落ちているか
falling = True
# 現在左に行っているか
lefting = True

# left, right, spaceキーが押されているか
left = False
right = False
space = False

# 最初かどうか(1回処理のため), 最初に左右どちらに動いているか用
first = True

# 最初かどうか(1回処理のため), 固定メッセージ用
firstMessage = True
# メッセージに変更があるかどうか
changeMessage = True

# プランジャーを使用中かどうか
plungerMode = True

# 終了するかどうか
exiting = False


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
    id: int
    x: float
    y: float
    width: float
    height: float
    bounce: int
    point: int
    c: str


class Ball:
    def __init__(self, id, x, y, d, vx, vy, c="black"):
        self.id = id
        self.x = x
        self.y = y
        self.d = d
        self.vx = vx
        self.vy = vy
        self.c = c

    def move_ball(self, vy):
        global falling, timer, lefting, first
        ballY = self.y
        ballX = self.x
    
        self.x += self.vx
        self.y += self.vy + vy
    
        # ボールを動かす前と動かす後を比較して、今現在落下しているのかを判断
        # boolで落ちていなくて、比較では落ちていたら
        if self.y - ballY > 0 and not falling:
            falling = True
            timer = -1
            self.vy = 0
        # boolで落ちていて、比較では上昇していたら(多分いらない)
        elif self.y - ballY < 0 and falling:
            falling = False
            print(falling)
        if first:
            first = False
            if self.x - ballX > 0 and lefting:
                lefting = False
            elif self.x - ballX < 0 and not lefting:
                lefting = True
                
    def redraw_ball(self):
        canvas.coords(self.id, self.x, self.y, self.x + self.d, self.y + self.d)


# make
# draw wall and objects
def make_wall(ox, oy, width, height, c=None):
    canvas.create_rectangle(ox, oy, ox + width, oy + height, fill=c)


# draw wall and objects
def make_object(ox, oy, width, height, bounce, point, c=None):
    id = canvas.create_rectangle(ox, oy, ox + width, oy + height, fill=c)
    return Object(id, ox, oy, width, height, bounce, point, c="none")


def make_ball(x, y, d, vx, vy, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d, fill=c, outline=c)
    return Ball(id, x, y, d, vx, vy, c)


def make_paddle(x, y, width, height, c="black"):
    id = canvas.create_rectangle(x, y, x + width, y + height, fill=c, outline=c)
    return Paddle(id, x, y, width, height, c)


# move
def move_paddle(paddle):
    if left:
        paddle.x -= 5
    elif right:
        paddle.x += 5


def bouncingY(ball, top, reflection):
    global falling, timer, bouncingTop
    vy = GRAVITY * timer / 100

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

    if ((ball.x + ball.d >= paddle.x) and (ball.x < paddle.x + paddle.width)) and (paddle.y + paddle.height > ball.y + ball.d >= paddle.y):
        bouncingY(ball, False, 1.1)


def obj_collision(ball, obj, plunger=False):
    global falling, lefting, count, points, changeMessage, plungerMode
    # objの当たり判定
    if (obj.x <= ball.x <= obj.x + obj.width or obj.x <= ball.x + ball.d <= obj.x + obj.width) and (obj.y <= ball.y <= obj.y + obj.height or obj.y <= ball.y + ball.d <= obj.y + obj.height):
        if (obj.x < ball.x or obj.x < ball.x + ball.d) and (obj.x + obj.width > ball.x + ball.d or obj.x + obj.width > ball.x):
            # obj上壁の当たり判定
            if ball.y + ball.d >= obj.y and falling and count > 2:
                if plunger:
                    plungerMode = True
                # print("ue")
                bouncingY(ball, False, .9)
                count = 0
                add_point(obj)
            # obj下壁の当たり判定
            elif ball.y <= obj.y + obj.height and not falling and count > 2:
                # print("shita")
                bouncingY(ball, True, .9)
                count = 0
                add_point(obj)
        # obj左壁の当たり判定
        elif ball.x + ball.d >= obj.x and not lefting and count > 2:
            # print("hidari")
            ball.vx = -ball.vx
            lefting = True
            count = 0
            add_point(obj)
        # obj右壁の当たり判定
        elif ball.x <= obj.x + obj.width and lefting and count > 2:
            # print("migi")
            ball.vx = -ball.vx
            lefting = False
            count = 0
            add_point(obj)


# add point
def add_point(obj):
    global points, changeMessage, objects_class, adpoints
    # ポイント加算
    if obj.bounce > 0:
        obj.bounce -= 1
        if obj.bounce == 1:
            obj.c = "dark red"
        elif obj.bounce == 0:
            objects_class.remove(obj)
            canvas.delete(obj.id)
            if len(objects_class) - 3 == 0:
                adpoints += 1
                points += 1000 * adpoints
                canvas.itemconfigure(advance_point_text, text=str(adpoints) + "回")
                objects_class.clear()
                for obje in objects:
                    objects_class.append(make_object(obje[0], obje[1], obje[2], obje[3], obje[4], obje[5], obje[6]))
        else:
            obj.c = random.choice(colors)
    points += obj.point
    changeMessage = True
    if not obj.c == "none": canvas.itemconfigure(obj.id, fill=obj.c)
    canvas.coords(obj.id, obj.x, obj.y, obj.x + obj.width, obj.y + obj.height)


def redraw_paddle(paddle):
    canvas.coords(paddle.id, paddle.x, paddle.y, paddle.x + paddle.width, paddle.y + paddle.height)


def showMessage(points):
    global changeMessage
    if changeMessage:
        canvas.itemconfigure(point_text, text=points)
        changeMessage = False


def mode_plunger():
    global firstMessage, energy_width, points, plungerMode, falling
    if firstMessage:
        canvas.create_text(10, 20, text="スコア:", anchor=W, font=("UD デジタル 教科書体 NK-R", 14))
        canvas.create_text(10, 40, text="全消し:", anchor=W, font=("UD デジタル 教科書体 NK-R", 14))
        canvas.create_text(750, 715, text="エネルギーバー\n(←弱 - 強→)", anchor=W, font=("UD デジタル 教科書体 NK-R", 14), justify=CENTER)
        showMessage(points)
        firstMessage = False
    if left and energy_width > 0:
        energy_width -= 1
    if right and energy_width < 130:
        energy_width += 1
    if space:
        ball.vy = -2 * energy_width / 15
        falling = False
        plungerMode = False
    canvas.coords(energy_bar, 750, 740, 750 + energy_width, 760)


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


def press_space(e):
    global space
    space = True


def release_space(e):
    global space
    space = False


def press_escape(e):
    global exiting
    exiting = True


# create canvas
tk = Tk()
canvas = Canvas(tk, width=900, height=800, bd=0)
canvas.pack()
tk.update()

# create text
point_text = canvas.create_text(75, 20, anchor=W, font=("UD デジタル 教科書体 NK-R", 12))
advance_point_text = canvas.create_text(87, 40, anchor=W, font=("UD デジタル 教科書体 NK-R", 12))

# Key Binds
# Left
tk.bind_all('<KeyPress-Left>', press_left)
tk.bind_all('<KeyRelease-Left>', release_left)

# Right
tk.bind_all('<KeyPress-Right>', press_right)
tk.bind_all('<KeyRelease-Right>', release_right)

# Space
tk.bind_all('<KeyPress-space>', press_space)
tk.bind_all('<KeyRelease-space>', release_space)

# Escape
tk.bind_all('<KeyPress-Escape>', press_escape)

# add objects
# ボール
ball = make_ball(665, 720, 20, 5, 0, "black")

# パドル
paddle = make_paddle(390, 650, 80, 20, "darkblue")

# 外枠
border = Border(150, 700, 50, 750)
plunger = Object(10000, 640, 735, 60, 15, -1, 0, "black")

make_wall(border.left, border.top, border.right - border.left, border.bottom - border.top)
make_wall(plunger.x, plunger.y, plunger.width, plunger.height, plunger.c)


# 中のオブジェクト群
walls = [[150, 660, 150, 10, -1, 0, "black"], [550, 660, 90, 10, -1, 0, "black"]]
objects = [[640, 350, 5, 400, -1, 0, "black"], [150, 660, 150, 10, -1, 0, "black"], [550, 660, 90, 10, -1, 0, "black"],
           [500, 200, 50, 50, 2, 100, "darkgreen"], [200, 100, 50, 50, 3, 100, "darkgreen"],
           [550, 300, 70, 50, 2, 100, "darkgreen"], [250, 400, 100, 100, 4, 100, "darkgreen"]]

walls_class = []
plungers_class = []
objects_class = []
# draw objects
for obj in walls:
    walls_class.append(make_object(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6]))
for obj in objects:
    objects_class.append(make_object(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6]))


# energy bar objects
canvas.create_rectangle(750, 740, 880, 760)
energy_bar = canvas.create_rectangle(750, 740, 750 + energy_width, 760, fill="lightgreen")

# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
colors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
          'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
          'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
          'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
          'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
          'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
          'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
          'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
          'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
          'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
          'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
          'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
          'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
          'indian red', 'saddle brown', 'sandy brown',
          'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
          'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
          'pale violet red', 'maroon', 'medium violet red', 'violet red',
          'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
          'thistle', 'snow2', 'snow3',
          'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
          'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
          'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
          'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
          'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
          'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
          'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
          'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
          'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
          'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
          'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
          'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
          'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
          'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
          'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
          'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
          'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
          'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
          'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
          'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
          'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
          'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
          'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
          'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
          'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
          'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
          'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
          'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
          'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
          'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
          'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
          'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
          'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
          'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
          'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
          'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
          'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
          'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
          'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
          'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
          'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
          'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
          'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
          'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
          'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
          'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
          'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
          'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
          'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
          'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
          'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
          'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
          'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
          'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
          'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
          'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
          'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

# main loop
while not exiting:
    if plungerMode:
        ball.y = plunger.y - ball.d - 1
        ball.redraw_ball()
        mode_plunger()
        tk.update()
        time.sleep(DURATION / 100)
        continue
    showMessage(points)
    count += 1
    timer += DURATION  # timerにDURATIONを足す。DURATIONが整数なのは、誤差を減らすため
    vy = GRAVITY * timer / 100  # 自由落下の公式に当てはめて、その時間の下方向の力を計算

    if not falling and ball.vy > 0:
        ball.y = border.bottom - ball.d

    ball.move_ball(vy)  # ボールを実際に動かす
    move_paddle(paddle)  # パドルを動かす

    # 当たり判定処理係
    box_collision(ball)
    for wall in walls_class:
        paddle_collision(ball, paddle, wall)
    for obj in objects_class:
        obj_collision(ball, obj)
    obj_collision(ball, plunger, True)

    # 再描写
    ball.redraw_ball()
    redraw_paddle(paddle)

    tk.update()
    time.sleep(DURATION / 100)

tk.mainloop()
