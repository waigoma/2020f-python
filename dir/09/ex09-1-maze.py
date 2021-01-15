# 問題[1]
from dataclasses import dataclass, field


@dataclass
class MazeGame:
    height: int = field(init=False, default=None)
    width: int = field(init=False, default=None)
    floormap: list = field(init=False, default=None)

    def set_floormap(self, maze_map):
        self.floormap = maze_map


game = MazeGame()
maze = [[1, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1]]
game.set_floormap(maze)
print(game.floormap)
