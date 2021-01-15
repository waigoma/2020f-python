# 問題[6]
from dataclasses import dataclass, field


@dataclass
class Maze:
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