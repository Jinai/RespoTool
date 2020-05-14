# -*- coding: utf-8 -*-
# !python3

from tkinter import ttk as ttk

from widgets.dialogs.basedialog import BaseDialog


class InfoDialog(BaseDialog):
    def __init__(self, master, *, body_text, button_text="OK", font=None, can_resize=False, **kwargs):
        super().__init__(master, can_resize=can_resize, **kwargs)
        self.body_text = body_text
        self.button_text = button_text
        self.font = font

    def body(self, container):
        wrap = ttk.Frame(container)
        wrap.pack(fill="both", expand=True, padx=15, pady=15)
        self.message = ttk.Label(wrap, text=self.body_text)
        if self.font:
            self.message.config(font=self.font)
        self.message.pack(fill="both", expand=True)
        return self.message

    def buttonbox(self, container):
        wrap = ttk.Frame(container)
        wrap.pack(padx=10, pady=(10, 5))
        btn = ttk.Button(wrap, text=self.button_text, command=self.ok, default="active", width=13)
        btn.pack(padx=10, pady=(10, 5))
