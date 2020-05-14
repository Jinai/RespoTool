# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
from tkinter import ttk

from widgets.frameseparator import FrameSeparator


class StatusBar(ttk.Frame):
    def __init__(self, master, text="", **opts):
        ttk.Frame.__init__(self, master, **opts)
        self.master = master
        self.text = text
        self._textvar = tk.StringVar()
        self._textvar.set(self.text)
        self.border = FrameSeparator(self, orient="horizontal", thickness=1)
        self.border.pack(side="top")
        self.label = tk.Label(self, anchor="w", textvariable=self._textvar)
        self.label.pack(side="left", fill="x", expand=True)
        self._clear_id = None

    def set(self, new_text, clear_after=10000):
        self._textvar.set(new_text)
        if clear_after > 0:
            self.schedule_clear(clear_after)
        else:
            self.unschedule_clear()

    def clear(self):
        self._textvar.set("")

    def schedule_clear(self, delay):
        self.unschedule_clear()
        self._clear_id = self.after(delay, self.clear)

    def unschedule_clear(self):
        id = self._clear_id
        self._clear_id = None
        if id:
            self.after_cancel(id)
