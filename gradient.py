# gradient.py
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class Gradient:
    def __init__(self, width=250, height=30, start_color=(255, 0, 0), end_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.start_color = start_color
        self.end_color = end_color
        self.image = self.create_gradient()

    def create_gradient(self):
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        for x in range(self.width):
            r = int((self.start_color[0] * (self.width - x) + self.end_color[0] * x) / self.width)
            g = int((self.start_color[1] * (self.width - x) + self.end_color[1] * x) / self.width)
            b = int((self.start_color[2] * (self.width - x) + self.end_color[2] * x) / self.width)
            color = (r, g, b)
            draw.line((x, 0, x, self.height), fill=color)

        return ImageTk.PhotoImage(img)

class GradientLabel(tk.Label):
    def __init__(self, master=None, text="", gradient=None, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.gradient = gradient
        self.configure(image=self.gradient.image, compound="center") 

class GradientButton(tk.Button):
    def __init__(self, master=None, text="", gradient=None, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.gradient = gradient
        self.configure(image=self.gradient.image, compound="center")

