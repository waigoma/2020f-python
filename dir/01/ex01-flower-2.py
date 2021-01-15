# 練習課題1.1 (2)


from tkinter import *
from dataclasses import *


@dataclass
class Flower:
    x: int
    y: int
    flowerColor: str


def draw_flower_at(pos_x, pos_y, flower):
    flowerLeft_x = flower.x / 2
    flowerLeft_y = flower.y
    flowerRight_x = flower.x * 2
    flowerRight_y = flower.y
    flowerDown_x = (flowerRight_x + flowerLeft_x) / 2
    flowerDown_y = flower.y * 1.75

    flower1Left_x = flowerLeft_x
    flower1Left_y = flower.y
    flower1Right_x = flowerDown_x
    flower1Right_y = flower.y
    flower1Top_x = (flower1Right_x + flower1Left_x) / 2
    flower1Top_y = flower.y / 1.5

    flower2Left_x = flowerDown_x
    flower2Left_y = flower.y
    flower2Right_x = flowerRight_x
    flower2Right_y = flower.y
    flower2Top_x = (flower2Right_x + flower2Left_x) / 2
    flower2Top_y = flower.y / 1.5

    flower3Left_x = flower1Top_x
    flower3Left_y = flower.y
    flower3Right_x = flower2Top_x
    flower3Right_y = flower.y
    flower3Top_x = flowerDown_x
    flower3Top_y = flower.y / 1.5

    canvas.create_polygon(flowerDown_x + pos_x, flowerDown_y + pos_y, flowerLeft_x + pos_x, flowerLeft_y + pos_y, flowerRight_x + pos_x, flowerRight_y + pos_y, outline=flower.flowerColor, fill=flower.flowerColor)
    canvas.create_polygon(flower1Left_x + pos_x, flower1Left_y + pos_y, flower1Right_x + pos_x, flower1Right_y + pos_y, flower1Top_x + pos_x, flower1Top_y + pos_y, outline=flower.flowerColor, fill=flower.flowerColor)
    canvas.create_polygon(flower2Left_x + pos_x, flower2Left_y + pos_y, flower2Right_x + pos_x, flower2Right_y + pos_y, flower2Top_x + pos_x, flower2Top_y + pos_y, outline=flower.flowerColor, fill=flower.flowerColor)
    canvas.create_polygon(flower3Left_x + pos_x, flower3Left_y + pos_y, flower3Right_x + pos_x, flower3Right_y + pos_y, flower3Top_x + pos_x, flower3Top_y + pos_y, outline=flower.flowerColor, fill=flower.flowerColor)


tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

flower1 = Flower(100, 100, "red")
flower2 = Flower(50, 50, "red")
flower3 = Flower(20, 20, "red")
flower4 = Flower(200, 200, "red")

draw_flower_at(0, 0, flower1)
draw_flower_at(250, 0, flower2)
draw_flower_at(300, 0, flower3)
draw_flower_at(100, 0, flower4)

tk.mainloop()
