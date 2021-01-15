# 練習課題1.2 (2)

from tkinter import *
import math

centerX = 100
centerY = 300
width = 800
height = 600
scaleX = 40
scaleY = 40

start = 0
end = 4 * math.pi
scale = 0.01


def draw_point(x, y, r=1, c="black"):
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)


def make_axes(ox, oy, width, height):
    canvas.create_line(0, oy, width, oy)
    canvas.create_line(ox, 0, ox, height)


def plot(x, y):
    draw_point(scaleX * x + centerX, centerY - scaleY * y)


def f(x):
    return math.cos(x)


tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

make_axes(centerX, centerY, width, height)

x = start
while x < end:
    plot(x, f(x))
    x += scale

tk.mainloop()
