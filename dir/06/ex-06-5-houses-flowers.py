# 問題[5]

from tkinter import *
from dataclasses import dataclass


@dataclass
class House:
    w: int
    h: int
    roof_color: str
    wall_color: str

    def draw(self, x, y):
        rtop_x = x + self.w / 2
        wtop_y = y + self.h / 2
        bottom_x = x + self.w
        bottom_y = y + self.h
        canvas.create_polygon(
            rtop_x, y,
            x, wtop_y,
            x + self.w, wtop_y,
            outline=self.roof_color, fill=self.roof_color)
        canvas.create_rectangle(
            x, wtop_y, bottom_x, bottom_y,
            outline=self.wall_color, fill=self.wall_color)

    def width(self):
        return self.w


@dataclass
class Flower:
    w: int
    h: int
    color: str

    def draw(self, x, y):
        rtop_x = x + self.w / 2
        wtop_y = y + self.h / 2
        rtop_y = wtop_y - y
        canvas.create_polygon(
            rtop_x, wtop_y + rtop_y,
            x, wtop_y / 1.2,
                    x + self.w, wtop_y / 1.2,
            outline=self.color, fill=self.color)
        canvas.create_polygon(
            rtop_x, y,
            x, wtop_y,
            x + self.w, wtop_y,
            outline=self.color, fill=self.color)

    def width(self):
        return self.w


tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0, bg="whitesmoke")
canvas.pack()

objects = [
    House(50, 100, "green", "white"),
    House(100, 70, "blue", "gray"),
    Flower(50, 100, "pink"),
    Flower(100, 70, "red")
]

x = 0
PAD = 10
for obj in objects:
    obj.draw(x, 100)
    x = x + obj.width() + PAD

tk.mainloop()
