# -*- coding: utf-8 -*-
# !python3

import tkinter as tk


class FrameSeparator(tk.Frame):
    # A thin frame acting like a border / separator for other widgets.
    # Color and thickness are customizable.

    def __init__(self, master, thickness=1, color="#D7D7D7", orient="horizontal", side="top"):
        tk.Frame.__init__(self, master)
        self.master = master
        self.thickness = thickness
        self.color = color
        self.orient = orient
        self.side = side
        self.set_color(color)
        self.set_thickness(thickness)

    def set_color(self, new_color):
        self.configure(background=new_color)

    def set_thickness(self, new_thickness):
        self.thickness = new_thickness
        if self.orient == "horizontal":
            self.configure(height=self.thickness)
        else:
            self.configure(width=self.thickness)

    def pack(self, **kwargs):
        fill = "x" if self.orient == "horizontal" else "y"
        super().pack(fill=fill, **kwargs)
