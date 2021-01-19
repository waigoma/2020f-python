# ex14-sub

from dataclasses import dataclass, field
import pygame
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
    key_count: int = field(init=False, default=0)
    is_pass: list = field(init=False, default_factory=list)

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

                # if self.search_mode:
                #     self.draw_text(i, j, text, 600)  # テキストの表示
                #     return

                if self.isWin:
                    self.fill_draw(i, j, text)
                else:
                    self.fill_all(i, j)
                    self.draw_text(i, j, text, 0)  # テキストの表示

    def draw_text(self, i, j, word, width):
        x = OFFSET_X + i * CELL_SIZE + width  # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE  # インデックスjからy座標を計算

        if word == 1:
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=0)
            word = ""

        pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=1)  # 枠

        text = font.render(str(word), True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (x + CELL_CENTER, y + CELL_CENTER)

        screen.blit(text, text_rect)

    def fill_all(self, i, j):
        x = OFFSET_X + i * CELL_SIZE  # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE  # インデックスjからy座標を計算

        if not self.is_pass[j][i]:
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), width=0)

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

        if self.isWin:
            self.you_win()

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
        screen.fill(WHITE)
        win_font = pygame.font.Font("UDDigiKyokashoN-R.ttc", 72)
        win_text = win_font.render("You Win!", True, BLACK)
        win_rect = win_text.get_rect()
        win_rect.center = (300, 300)

        move_font = pygame.font.Font("UDDigiKyokashoN-R.ttc", 24)
        move_text = move_font.render("動かした回数: " + str(self.key_count), True, BLACK)
        move_rect = move_text.get_rect()
        move_rect.topleft = (100, 100)

        if self.end:
            comp_font = pygame.font.Font("UDDigiKyokashoN-R.ttc", 24)
            comp_text = comp_font.render("最短回数: " + str(len(self.sg_list) + 1), True, BLACK)
            comp_rect = comp_text.get_rect()
            comp_rect.topleft = (100, 150)
            screen.blit(comp_text, comp_rect)

        screen.blit(win_text, win_rect)
        screen.blit(move_text, move_rect)

        self.isWin = True

    def reset(self):
        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                if self.maze.floormap[j][i] == 3 or self.maze.floormap[j][i] == 5:
                    self.maze.floormap[j][i] = 0

    def start_maze(self):
        self.maze = Maze()
        self.maze.from_file("R03-map.txt")

        for i in range(self.maze.width):  # iは幅方向の添え字
            for j in range(self.maze.height):  # jは、高さ方向の添え字
                if self.maze.floormap[j][i] == 8:
                    self.set_player(i, j)

        wh_list = []
        for i in range(self.maze.height):
            width_list = []
            for j in range(self.maze.width):
                if self.maze.floormap[i][j] == 8 or self.maze.floormap[i][j] == 9:
                    width_list.append(True)
                    continue
                width_list.append(False)

            wh_list.append(width_list)

        self.is_pass = wh_list

        self.redraw()

        while not self.isWin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player_up()
                        self.key_count += 1
                    if event.key == pygame.K_RIGHT:
                        self.player_right()
                        self.key_count += 1
                    if event.key == pygame.K_DOWN:
                        self.player_down()
                        self.key_count += 1
                    if event.key == pygame.K_LEFT:
                        self.player_left()
                        self.key_count += 1

            self.is_pass[self.player[1]][self.player[0]] = True
            self.redraw()

            pygame.display.update()
            clock.tick(FPS)

        self.search_depth()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.redraw()

            pygame.display.update()
            clock.tick(FPS)

    def search_depth(self):
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
                # time.sleep(0.25)

            self.next_place = next_place

            # self.redraw()
            # pygame.display.update()
            # clock.tick(FPS)

            # ↑の4行コメント外せばゆっくり探索の様子を確認できます。

    def player_up(self):
        tuple_list = []
        for x in self.player:
            tuple_list.append(x)

        if self.maze.floormap[tuple_list[1] - 1][tuple_list[0]] == 1:
            self.redraw()
            return
        if MAZE_HEIGHT >= tuple_list[1] - 1 >= 0:
            self.set_player(tuple_list[0], tuple_list[1] - 1)

        self.redraw()

    def player_right(self):
        tuple_list = []
        for x in self.player:
            tuple_list.append(x)

        if self.maze.floormap[tuple_list[1]][tuple_list[0] + 1] == 1:
            self.redraw()
            return
        if MAZE_WIDTH - 1 >= tuple_list[0] + 1 >= 0:
            self.set_player(tuple_list[0] + 1, tuple_list[1])

        self.redraw()

    def player_down(self):
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

    def player_left(self):
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
pygame.display.set_caption('ex14-sub-迷路ゲーム')

font = pygame.font.SysFont("Consolas.tff", 24)

maze_map = [[1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]]

game.start_maze()
game.print_floormap()
