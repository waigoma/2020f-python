# -*- coding: utf-8 -*-
# 例題プログラム 迷路作成
# --------------------------
# プログラム名: 09-maze-auto.py

import random

MAZE_WIDTH = 11
MAZE_HEIGHT = 9

SPACE = 0
WALL = 1
PILLAR = 2

class Maze:
    def __init__(self):
        # ↓ ここは、教材用
        # よくネットで見かけるが、この例だとうまく行かない
        self.mark = [[0] * MAZE_HEIGHT] * MAZE_WIDTH
        self.mark[1][3] = 1
        print(self.mark)
        # (1,3)だけ1に設定したはずなのに(0,3),(1,3)(2,3)などが1になっている。
        # 
        # 下の例だと、全てのセルが独立でうまくいく
        # 教科書 P305 Deep CopyとShallow Copyを参照のこと
        self.mark = [[0 for i in range(MAZE_HEIGHT)] for j in range(MAZE_WIDTH)]
        self.mark[1][3] = 1
        print(self.mark)
        # ↑ うまく行かない初期化の解説、ここまで。(各自削除して下さい)

        self.mark = [[0 for i in range(MAZE_HEIGHT)] for j in range(MAZE_WIDTH)]

        # 壁と柱の設定
        # このプログラムは、column-majorで書かれている点に注意！
        for i in range(0, MAZE_WIDTH, 2):
            for j in range(0, MAZE_HEIGHT, 2):
                if i==0 or j==0 or i==MAZE_WIDTH-1 or j==MAZE_HEIGHT-1:
                    self.mark[i][j] = WALL
                else:
                    self.mark[i][j] = PILLAR

        # この迷路は、下記サイトの「壁のばし」法と同じ考え方で作っています。
        # http://www5d.biglobe.ne.jp/stssk/maze/make.html
        self.maze = [[SPACE for i in range(MAZE_HEIGHT)] for j in range(MAZE_WIDTH)]
        for i in range(MAZE_WIDTH):
            self.maze[i][0] = WALL
            self.maze[i][MAZE_HEIGHT-1] = WALL
        for j in range(MAZE_HEIGHT):
            self.maze[0][j] = WALL
            self.maze[MAZE_WIDTH-1][j] = WALL
        for i in range(0, MAZE_WIDTH, 2):
            for j in range(0, MAZE_HEIGHT, 2):
                self.maze[i][j] = WALL

        finished = False
        while not finished:
            finished = True
            for i in range(2, MAZE_WIDTH, 2):
                for j in range(2, MAZE_HEIGHT, 2):
                    if self.mark[i][j]==WALL: continue
                    # まだ接続されていない柱があったら、
                    finished = False
                    direction = random.randint(0, 4)
                    if direction == 0: # 左
                        if self.mark[i-2][j] == WALL:  # 壁に接続する
                            self.maze[i-1][j] = WALL
                            self.mark[i][j] = WALL
                    elif direction == 1:  # 上
                        if self.mark[i][j-2] == WALL:
                            self.maze[i][j-1] = WALL
                            self.mark[i][j] = WALL
                    elif direction == 2:  # 右
                        if self.mark[i+2][j] == WALL:
                            self.maze[i+1][j] = WALL
                            self.mark[i][j] = WALL
                    elif direction == 3:
                        if self.mark[i][j+2] == WALL:
                            self.maze[i][j+1] = WALL
                            self.mark[i][j] = WALL
        print(self.maze)

# -------------------

maze = Maze()
