# 問題[4]
import random
import time
from dataclasses import dataclass, field
from tkinter import Tk, Canvas, CENTER, W
from maze import Maze

MAZE_HEIGHT = 11
MAZE_WIDTH = 9

SPACE = 0
WALL = 1
PILLAR = 2

OFFSET_X = 100
OFFSET_Y = 100
CELL_SIZE = 40
CELL_CENTER = CELL_SIZE / 2
FONT_SIZE = 20

FONT = "Helvetica " + str(FONT_SIZE)


@dataclass
class MazeGame:
    maze: Maze = field(init=False, default=None)
    player: tuple = field(init=False, default=None)
    isWin: bool = field(init=False, default=False)
    next_place: list = field(init=False, default_factory=list)
    first: bool = field(init=False, default=True)

    def print_floormap(self):
        for x in self.maze.floormap:
            str_map: str = str(x)
            str_map = str_map.replace("[", "")
            str_map = str_map.replace("]", "")
            str_map = str_map.replace(",", "")
            print(str_map)

    def set_player(self, i, j):
        self.player = (i, j)

    # def draw_player(self):
    #     for i in range(self.maze.width):
    #         for j in range(self.maze.height):
    #             if self.player == (i, j):
    #                 self.draw_text(i, j, "P")

    def draw(self):
        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                text = self.maze.floormap[j][i]
                if text == 0:
                    text = ""
                if text == 8:
                    text = "S"
                if text == 9:
                    text = "G"
                if self.player == (i, j):
                    text = "P"

                self.draw_text(i, j, text)  # テキストの表示

    def draw_text(self, i, j, text):
        x = OFFSET_X + i * CELL_SIZE  # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE  # インデックスjからy座標を計算
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE)  # 枠
        canvas.create_text(x + CELL_CENTER, y + CELL_CENTER,
                           text=text, font=FONT, anchor=CENTER)

    def redraw(self):
        canvas.delete("all")

        player_pos = []
        for x in self.player:
            player_pos.append(x)
        if self.maze.floormap[player_pos[1]][player_pos[0]] == 9:
            self.you_win()
            return

        self.draw()

    def you_win(self):
        # canvas.delete("all")
        # canvas.create_text(180, 200, text="You Win", anchor=W, font=("UD デジタル 教科書体 NK-R", 24))
        self.isWin = True

    def start(self):
        self.maze = Maze()
        self.maze.from_file("ex11-2-move.txt")
        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                if self.maze.floormap[j][i] == 8:
                    self.set_player(i, j)
        # tk.bind_all('<KeyPress-Up>', self.player_up)
        # tk.bind_all('<KeyPress-Right>', self.player_right)
        # tk.bind_all('<KeyPress-Down>', self.player_down)
        # tk.bind_all('<KeyPress-Left>', self.player_left)
        self.redraw()

        while not self.isWin:
            tuple_list = []
            player_xy = []
            next_place = []
            if self.first:
                for x in self.player:
                    tuple_list.append(x)
                player_xy.append(tuple_list)
                self.first = False

            for x in self.next_place:
                player_xy.append(x)

            for xy in player_xy:
                for y in [-1, 1]:
                    if len(self.maze.floormap) <= xy[1] + y:
                        continue
                    if self.maze.floormap[xy[1] + y][xy[0]] == 0:
                        next_place.append([xy[0], xy[1] + y])
                    elif self.maze.floormap[xy[1] + y][xy[0]] == 9:
                        self.you_win()

                for x in [-1, 1]:
                    if self.maze.floormap[xy[1]][xy[0] + x] == 0:
                        next_place.append([xy[0] + x, xy[1]])
                    elif self.maze.floormap[xy[1]][xy[0] + x] == 9:
                        self.you_win()

            if self.isWin:
                break

            for go in next_place:
                self.set_player(go[0], go[1])
                self.maze.floormap[go[1]][go[0]] = 5
                self.redraw()

                tk.update()
                time.sleep(0.25)

            print(self.next_place)

            self.next_place = next_place
            tk.update()

    def player_up(self, e):
        tuple_list = []
        for x in self.player:
            tuple_list.append(x)

        if self.maze.floormap[tuple_list[1] - 1][tuple_list[0]] == 1:
            self.redraw()
            return
        if MAZE_HEIGHT >= tuple_list[1] - 1 >= 0:
            self.set_player(tuple_list[0], tuple_list[1] - 1)

        self.redraw()

    def player_right(self, e):
        tuple_list = []
        for x in self.player:
            tuple_list.append(x)

        if self.maze.floormap[tuple_list[1]][tuple_list[0] + 1] == 1:
            self.redraw()
            return
        if MAZE_WIDTH - 1 >= tuple_list[0] + 1 >= 0:
            self.set_player(tuple_list[0] + 1, tuple_list[1])

        self.redraw()

    def player_down(self, e):
        tuple_list = []
        for x in self.player:
            tuple_list.append(x)

        if len(self.maze.floormap) <= tuple_list[1] + 1:
            self.redraw()
            return
        if self.maze.floormap[tuple_list[1] + 1][tuple_list[0]] == 1:
            self.redraw()
            return
        if MAZE_HEIGHT - 1 >= tuple_list[1] + 1 >= 0:
            self.set_player(tuple_list[0], tuple_list[1] + 1)

        self.redraw()

    def player_left(self, e):
        tuple_list = []
        for x in self.player:
            tuple_list.append(x)

        if self.maze.floormap[tuple_list[1]][tuple_list[0] - 1] == 1:
            self.redraw()
            return
        if MAZE_WIDTH >= tuple_list[0] - 1 >= 0:
            self.set_player(tuple_list[0] - 1, tuple_list[1])

        self.redraw()


game = MazeGame()
tk = Tk()

canvas = Canvas(tk, width=600, height=600, bd=0)
canvas.pack()

maze_map = [[1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]]

game.start()
game.print_floormap()

tk.mainloop()
