# 問題[1]


from tkinter import *


class Flower:
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__flower_color = color

    def draw_flower_at(self, pos_x, pos_y):
        flowerLeft_x = self.__x / 2
        flowerLeft_y = self.__y
        flowerRight_x = self.__x * 2
        flowerRight_y = self.__y
        flowerDown_x = (flowerRight_x + flowerLeft_x) / 2
        flowerDown_y = self.__y * 1.75

        flower1Left_x = flowerLeft_x
        flower1Left_y = self.__y
        flower1Right_x = flowerDown_x
        flower1Right_y = self.__y
        flower1Top_x = (flower1Right_x + flower1Left_x) / 2
        flower1Top_y = self.__y / 1.5

        flower2Left_x = flowerDown_x
        flower2Left_y = self.__y
        flower2Right_x = flowerRight_x
        flower2Right_y = self.__y
        flower2Top_x = (flower2Right_x + flower2Left_x) / 2
        flower2Top_y = self.__y / 1.5

        flower3Left_x = flower1Top_x
        flower3Left_y = self.__y
        flower3Right_x = flower2Top_x
        flower3Right_y = self.__y
        flower3Top_x = flowerDown_x
        flower3Top_y = self.__y / 1.5

        canvas.create_polygon(flowerDown_x + pos_x, flowerDown_y + pos_y, flowerLeft_x + pos_x, flowerLeft_y + pos_y, flowerRight_x + pos_x, flowerRight_y + pos_y, outline=self.__flower_color, fill=self.__flower_color)
        canvas.create_polygon(flower1Left_x + pos_x, flower1Left_y + pos_y, flower1Right_x + pos_x, flower1Right_y + pos_y, flower1Top_x + pos_x, flower1Top_y + pos_y, outline=self.__flower_color, fill=self.__flower_color)
        canvas.create_polygon(flower2Left_x + pos_x, flower2Left_y + pos_y, flower2Right_x + pos_x, flower2Right_y + pos_y, flower2Top_x + pos_x, flower2Top_y + pos_y, outline=self.__flower_color, fill=self.__flower_color)
        canvas.create_polygon(flower3Left_x + pos_x, flower3Left_y + pos_y, flower3Right_x + pos_x, flower3Right_y + pos_y, flower3Top_x + pos_x, flower3Top_y + pos_y, outline=self.__flower_color, fill=self.__flower_color)


tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

flowers = [Flower(200, 200, "red"), Flower(100, 100, "red"), Flower(50, 50, "red"), Flower(20, 20, "red")]
i = 0

for flower in flowers:
    flower.draw_flower_at(0 + i * 100, 0)
    i += 1

tk.mainloop()
