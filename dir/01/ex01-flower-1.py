# 練習課題1.1 (1)


from tkinter import *
from dataclasses import *


@dataclass
class Flower:
    x: int
    y: int
    flowerColor: str
    underFlowerColor: str


def draw_flower(flower):
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

    canvas.create_polygon(flowerDown_x, flowerDown_y, flowerLeft_x, flowerLeft_y, flowerRight_x, flowerRight_y, outline=flower.flowerColor, fill=flower.flowerColor)
    canvas.create_polygon(flower1Left_x, flower1Left_y, flower1Right_x, flower1Right_y, flower1Top_x, flower1Top_y, outline=flower.flowerColor, fill=flower.flowerColor)
    canvas.create_polygon(flower2Left_x, flower2Left_y, flower2Right_x, flower2Right_y, flower2Top_x, flower2Top_y, outline=flower.flowerColor, fill=flower.flowerColor)
    canvas.create_polygon(flower3Left_x, flower3Left_y, flower3Right_x, flower3Right_y, flower3Top_x, flower3Top_y, outline=flower.flowerColor, fill=flower.flowerColor)


tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

flower1 = Flower(100, 100, "red", "green")

draw_flower(flower1)

tk.mainloop()
