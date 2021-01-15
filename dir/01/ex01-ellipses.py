# 練習課題1.3 (1)
from tkinter import *
import math

centerX = 400
centerY = 300
width = 800
height = 600
scaleX = 100
scaleY = 100

start = 0
end = 2 * math.pi
scale = 0.01


def draw_point(x, y, r=1, c="black"):
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)


def make_axes(ox, oy, width, height):
    canvas.create_line(0, oy, width, oy)
    canvas.create_line(ox, 0, ox, height)


def plot(x, y, r=1, c="black"):
    draw_point(scaleX * x + centerX, centerY - scaleY * y, r, c)


def f1(x):
    return math.cos(x)


def f2(x):
    return math.sin(x)


tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

make_axes(centerX, centerY, width, height)

theta = start
while theta < end:
    plot(f1(theta)*2, f2(theta)*2)
    plot(f1(theta) / 2, 2 * f2(theta), 1, "blue")
    theta += scale

tk.mainloop()
