# 13-問題[3]
import time
from dataclasses import dataclass, field
import pygame
from maze import Maze

# 分岐点ごとに配列作ればよかった説
# 行き止まりの道選んだら、分岐点まで行き止まりの色で染めているやり方にしている。
# start -> goal と goal -> start が同じ座標を持つまで無限ループしてる。

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

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


@dataclass
class MazeGame:
    maze: Maze = field(init=False, default=None)
    player: tuple = field(init=False, default=None)
    isWin: bool = field(init=False, default=False)
    next_place: list = field(init=False, default_factory=list)
    first: bool = field(init=False, default=True)
    end: bool = field(init=False, default=False)
    sg_gs: bool = field(init=False, default=False)
    sg_list: list = field(init=False, default_factory=list)
    gs_list: list = field(init=False, default_factory=list)
    goal: tuple = field(init=False, default_factory=list)
    start: tuple = field(init=False, default_factory=list)

    def print_floormap(self):
        for x in self.maze.floormap:
            str_map: str = str(x)
            str_map = str_map.replace("[", "")
            str_map = str_map.replace("]", "")
            str_map = str_map.replace(",", "")
            print(str_map)

    def set_player(self, i, j):
        self.player = (i, j)

    def draw(self):
        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                text = self.maze.floormap[j][i]
                if text == 0:
                    text = ""
                if text == 8:
                    text = "S"
                    self.start = (i, j)
                if text == 9:
                    text = "G"
                    self.goal = (i, j)
                if self.player == (i, j):
                    text = "P"

                self.draw_text(i, j, text)  # テキストの表示
                if self.end and self.isWin:
                    self.fill_draw(i, j, text)

    def draw_text(self, i, j, word):
        x = OFFSET_X + i * CELL_SIZE  # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE  # インデックスjからy座標を計算

        if word == 1:
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=0)
            word = ""

        pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=1)  # 枠

        text = font.render(str(word), True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (x + CELL_CENTER, y + CELL_CENTER)

        screen.blit(text, text_rect)

    def fill_draw(self, i, j, word):
        x = OFFSET_X + i * CELL_SIZE + 600  # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE  # インデックスjからy座標を計算

        if word == 1:
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=0)
            word = ""

        elif word == 2:
            pygame.draw.rect(screen, (0, 106, 182), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=0)
            word = ""

        elif word == "" or word == "P":
            pygame.draw.rect(screen, (247, 227, 62), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=0)
            word = ""

        pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=1)  # 枠

        text = font.render(str(word), True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (x + CELL_CENTER, y + CELL_CENTER)

        screen.blit(text, text_rect)

    def redraw(self):
        screen.fill(WHITE)

        player_pos = []
        for x in self.player:
            player_pos.append(x)
        if self.maze.floormap[player_pos[1]][player_pos[0]] == 9:
            self.you_win()
            return

        self.draw()

    def back(self, li, back_num=5):
        back_list = []

        for xy in li:
            self.maze.floormap[xy[1]][xy[0]] = 2

            for y in [-1, 1]:
                if len(self.maze.floormap) <= xy[1] + y:
                    continue
                if self.maze.floormap[xy[1] + y][xy[0]] == back_num:
                    back_list.append([xy[0], xy[1] + y])

            for x in [-1, 1]:
                if self.maze.floormap[xy[1]][xy[0] + x] == back_num:
                    back_list.append([xy[0] + x, xy[1]])

        if len(back_list) != 0:
            self.back(back_list)

    def you_win(self):
        # canvas.delete("all")
        # canvas.create_text(180, 200, text="You Win", anchor=W, font=("UD デジタル 教科書体 NK-R", 24))
        self.isWin = True

    def reset(self):
        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                if self.maze.floormap[j][i] == 3 or self.maze.floormap[j][i] == 5:
                    self.maze.floormap[j][i] = 0

    def start_maze(self):
        self.maze = Maze()
        self.maze.from_file("ex13-map.txt")
        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                if self.maze.floormap[j][i] == 8:
                    self.set_player(i, j)

        self.redraw()

        while not self.sg_gs:
            self.sg_list = []
            self.gs_list = []

            for goal in [9, 8]:
                self.isWin = False
                self.next_place = []
                self.first = True

                if goal == 9:
                    self.player = self.start
                elif goal == 8:
                    self.player = self.goal

                self.animate(goal)
                self.reset()

            if len(self.sg_list) != len(self.gs_list):
                continue

            if self.sg_list != self.gs_list:
                self.sg_gs = False
                self.sg_list.clear()
                self.gs_list.clear()
                break
            else:
                self.sg_gs = True

        self.end = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.redraw()

            pygame.display.update()
            clock.tick(FPS)

    def animate(self, goal_num):
        while not self.isWin:
            tuple_list = []
            player_xy = []
            next_place = []

            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if self.first:
                for x in self.player:
                    tuple_list.append(x)
                player_xy.append(tuple_list)
                self.first = False

            for x in self.next_place:
                player_xy.append(x)

            for xy in player_xy:
                count = 0
                for y in [-1, 1]:
                    if len(self.maze.floormap) <= xy[1] + y:
                        continue
                    if self.maze.floormap[xy[1] + y][xy[0]] == 0:
                        next_place.append([xy[0], xy[1] + y])
                        count += 1
                    elif self.maze.floormap[xy[1] + y][xy[0]] == goal_num:
                        self.you_win()
                        count += 1

                for x in [-1, 1]:
                    if self.maze.floormap[xy[1]][xy[0] + x] == 0:
                        next_place.append([xy[0] + x, xy[1]])
                        count += 1
                    elif self.maze.floormap[xy[1]][xy[0] + x] == 0:
                        self.you_win()
                        count += 1

                if count == 0:
                    xy_li = [xy]
                    self.back(xy_li, 5)

                if count > 1 and not self.end:
                    self.maze.floormap[xy[1]][xy[0]] = 3

            if self.isWin:
                break

            for go in next_place:
                if goal_num == 9:
                    self.sg_list.append(go)
                elif goal_num == 8:
                    self.gs_list.insert(0, go)

                self.set_player(go[0], go[1])
                self.maze.floormap[go[1]][go[0]] = 5
                self.redraw()

                pygame.display.update()
                time.sleep(0.1)

            # print(self.next_place)

            self.next_place = next_place

            self.redraw()

            pygame.display.update()
            clock.tick(FPS)

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
pygame.font.init()

screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('ex13-duplicate')

font = pygame.font.SysFont("Consolas.tff", 24)

maze_map = [[1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]]

game.start_maze()
game.print_floormap()
