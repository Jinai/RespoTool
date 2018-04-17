# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk

from .modaldialog import ModalDialog


class EditStatusDialog(ModalDialog):
    def __init__(self, parent, title=None, original_text=''):
        self.original_text = original_text
        ModalDialog.__init__(self, parent, title)

    def body(self, master):
        text_frame = tk.Frame(master)
        text_frame.pack(fill="both", expand=True)
        self.text = tk.Text(text_frame, width=60, height=4, wrap="word", font=("Segoe UI", 9), exportselection=False,
                            undo=True, autoseparators=True, maxundo=-1)
        self.text.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        scrollbar.pack(fill="y", side="right")
        self.text['yscrollcommand'] = scrollbar.set
        self.text.bind('<Return>', lambda _: self.on_enter())
        self.text.bind('<Right>', lambda _: self.text.mark_set(tk.INSERT, tk.END))

        self.text.insert(tk.INSERT, self.original_text)
        self.text.edit_reset()  # reset undo/redo stack so that ctrl+z doesn't delete the original status
        self.select_all(None)
        return self.text

    def buttonbox(self):
        box = tk.Frame(self)
        box.pack()
        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Annuler", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

    def on_enter(self):
        # Stores widget's content before a newline is inserted or the text removed
        self.result = self.text.get("1.0", tk.END).strip()

    def apply(self):
        if not self.result:
            # Clicked on 'Ok' instead of pressing Enter
            self.result = self.text.get("1.0", tk.END).strip()

    def select_all(self, event):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return 'break'
