# 問題[6]
from dataclasses import dataclass, field
from tkinter import Tk, Canvas, CENTER
import random

MAZE_WIDTH = 6
MAZE_HEIGHT = 4

SPACE = 0
WALL = 1
PILLAR = 2

OFFSET_X = 100
OFFSET_Y = 100
CELL_SIZE = 40
CELL_CENTER = CELL_SIZE/2
FONT_SIZE = 20

FONT = "Helvetica " + str(FONT_SIZE)


@dataclass
class MazeGame:
    height: int = field(init=False, default=None)
    width: int = field(init=False, default=None)
    floormap: list = field(init=False, default=None)

    def set_floormap(self, __maze_map):
        self.floormap = __maze_map

    def from_file(self, filename):
        self.floormap = []
        with open(filename) as file:
            height = 0
            for line in file:
                height += 1
                line = line.rstrip("\n")
                str_maps = line.split(",")
                maps = []
                width = 0
                for m in str_maps:
                    width += 1
                    maps.append(int(m))
                self.width = width
                self.height = height
                self.floormap.append(maps)

    def print_floormap(self):
        for x in self.floormap:
            str_map: str = str(x)
            str_map = str_map.replace("[", "")
            str_map = str_map.replace("]", "")
            str_map = str_map.replace(",", "")
            print(str_map)

    def draw(self):
        canvas.delete("all")                # 一旦クリアすす。
        for i in range(self.width):         # iは幅方向の添え字
            for j in range(self.height):    # jは、高さ方向の添え字
                text = self.floormap[j][i]
                if text == 0:
                    text = ""
                # if self.is_open[i][j]:   # マス目が開いていて
                #     if self.mine[i][j]:  # 地雷だったら
                #         text = "*"            # "*"
                #     else:                     # 地雷でないなら
                #         text = str(self.count(i, j))  # カウント数表示
                # else:                         # マス目が開いていないなら
                #     text = "-"                # "-"を表示
                self.draw_text(i, j, text)     # テキストの表示

    def draw_text(self, i, j, text):
        x = OFFSET_X + i * CELL_SIZE      # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE      # インデックスjからy座標を計算
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE) # 枠
        canvas.create_text(x + CELL_CENTER, y + CELL_CENTER,
                           text=text, font=FONT, anchor=CENTER)


class Maze:
    def __init__(self):
        # # ↓ ここは、教材用
        # # よくネットで見かけるが、この例だとうまく行かない
        # self.mark = [[0] * MAZE_HEIGHT] * MAZE_WIDTH
        # self.mark[1][3] = 1
        # print(self.mark)
        # # (1,3)だけ1に設定したはずなのに(0,3),(1,3)(2,3)などが1になっている。
        # #
        # # 下の例だと、全てのセルが独立でうまくいく
        # # 教科書 P305 Deep CopyとShallow Copyを参照のこと
        # self.mark = [[0 for i in range(MAZE_HEIGHT)] for j in range(MAZE_WIDTH)]
        # self.mark[1][3] = 1
        # print(self.mark)
        # # ↑ うまく行かない初期化の解説、ここまで。(各自削除して下さい)

        self.mark = [[0 for i in range(MAZE_HEIGHT)] for j in range(MAZE_WIDTH)]

        # 壁と柱の設定
        # このプログラムは、column-majorで書かれている点に注意！
        for i in range(0, MAZE_WIDTH, 2):
            for j in range(0, MAZE_HEIGHT, 2):
                if i == 0 or j == 0 or i == MAZE_WIDTH - 1 or j == MAZE_HEIGHT - 1:
                    self.mark[i][j] = WALL
                else:
                    self.mark[i][j] = PILLAR

        # この迷路は、下記サイトの「壁のばし」法と同じ考え方で作っています。
        # http://www5d.biglobe.ne.jp/stssk/maze/make.html
        self.maze = [[SPACE for i in range(MAZE_HEIGHT)] for j in range(MAZE_WIDTH)]
        for i in range(MAZE_WIDTH):
            self.maze[i][0] = WALL
            self.maze[i][MAZE_HEIGHT - 1] = WALL
        for j in range(MAZE_HEIGHT):
            self.maze[0][j] = WALL
            self.maze[MAZE_WIDTH - 1][j] = WALL
        for i in range(0, MAZE_WIDTH, 2):
            for j in range(0, MAZE_HEIGHT, 2):
                self.maze[i][j] = WALL

        finished = False
        while not finished:
            finished = True
            for i in range(2, MAZE_WIDTH, 2):
                for j in range(2, MAZE_HEIGHT, 2):
                    if self.mark[i][j] == WALL: continue
                    # まだ接続されていない柱があったら、
                    finished = False
                    direction = random.randint(0, 4)
                    if direction == 0:  # 左
                        if self.mark[i - 2][j] == WALL:  # 壁に接続する
                            self.maze[i - 1][j] = WALL
                            self.mark[i][j] = WALL
                    elif direction == 1:  # 上
                        if self.mark[i][j - 2] == WALL:
                            self.maze[i][j - 1] = WALL
                            self.mark[i][j] = WALL
                    elif direction == 2:  # 右
                        if self.mark[i + 2][j] == WALL:
                            self.maze[i + 1][j] = WALL
                            self.mark[i][j] = WALL
                    elif direction == 3:
                        if self.mark[i][j + 2] == WALL:
                            self.maze[i][j + 1] = WALL
                            self.mark[i][j] = WALL
        # print(self.maze)

        with open(r"maze.txt", mode="w") as file:
            for x in self.maze:
                strx = str(x)
                strx = strx.replace("[", "")
                strx = strx.replace("]", "")
                file.write(strx)
                file.write("\n")
                # print(strx)


# maze = Maze()
game = MazeGame()
tk = Tk()

canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

maze_map = [[1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]]

game.from_file(r"maze6.txt")
game.print_floormap()
game.draw()

tk.mainloop()

# game.set_floormap(maze_map)
# print(game.floormap)
