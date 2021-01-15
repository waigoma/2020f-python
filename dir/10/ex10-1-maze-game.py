# 問題[6]
from dataclasses import dataclass, field
from tkinter import Tk, Canvas, CENTER
from maze import Maze

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
    maze: Maze = field(init=False, default=None)

    def print_floormap(self):
        for x in self.maze.floormap:
            str_map: str = str(x)
            str_map = str_map.replace("[", "")
            str_map = str_map.replace("]", "")
            str_map = str_map.replace(",", "")
            print(str_map)

    def draw(self):
        canvas.delete("all")                # 一旦クリアすす。
        for i in range(self.maze.width):         # iは幅方向の添え字
            for j in range(self.maze.height):    # jは、高さ方向の添え字
                text = self.maze.floormap[j][i]
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

    def redraw(self):
        self.draw()

    def start(self):
        self.maze = Maze()
        self.maze.from_file("maze6.txt")
        self.redraw()


game = MazeGame()
tk = Tk()

canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

maze_map = [[1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]]

game.start()
game.print_floormap()

tk.mainloop()
