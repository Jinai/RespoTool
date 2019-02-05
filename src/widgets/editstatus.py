# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk

import utils
from .modaldialog import ModalDialog


class EditStatusDialog(ModalDialog):
    def __init__(self, master, statuses, original_text, title=None):
        ModalDialog.__init__(self, master, title)
        self.statuses = statuses
        self.original_text = original_text
        self.checkbuttons_state = {}
        self.comment = ""
        self.parse_original_text()

    def body(self, main_frame):
        # Checkbuttons for statuses
        checkbuttons_frame = tk.Frame(main_frame)
        checkbuttons_frame.pack(fill="both", expand=True, side="top")
        for chunk in utils.sequence_chunker(self.statuses, 3):
            column = tk.Frame(checkbuttons_frame)
            column.pack(fill="both", expand=True, side="left")
            for status in chunk:
                if status in self.checkbuttons_state:
                    var = self.checkbuttons_state[status]
                else:
                    var = tk.IntVar(master=self, value=0)
                    self.checkbuttons_state[status] = var

                var.trace("w", lambda *_, var=var, name=status: self.checkbutton_callback(var, name))
                cb = ttk.Checkbutton(column, text=status.title(), variable=var, takefocus=False)
                cb.pack(side="top", anchor="w")

        # Text area for comments
        comment_frame = tk.Frame(main_frame)
        comment_frame.pack(fill="both", expand=True, pady=5)
        comment_label = ttk.Label(comment_frame, text="Commentaire :")
        comment_label.pack(anchor="w")
        self.comment_field = tk.Text(comment_frame, width=60, height=4, wrap="word", font=("Segoe UI", 9),
                                     exportselection=False,
                                     undo=True, autoseparators=True, maxundo=-1)
        self.comment_field.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(comment_frame, command=self.comment_field.yview)
        scrollbar.pack(fill="y", side="right")
        self.comment_field['yscrollcommand'] = scrollbar.set
        self.comment_field.bind('<Return>', lambda *_: self.ok())
        self.comment_field.bind('<Control-Key-a>', lambda *_: self.select_all())

        self.comment_field.insert(tk.INSERT, self.comment)
        self.comment_field.edit_reset()  # reset undo/redo stack so that ctrl+z doesn't delete the original status
        self.select_all()
        return self.comment_field

    def parse_original_text(self, status_sep="+", comment_sep="//"):
        tmp = self.original_text.split(comment_sep, 1)
        comment = ""
        if len(tmp) == 2:
            comment = tmp.pop().strip()
        self.comment = comment
        for status in tmp.pop().split(status_sep):
            var = tk.IntVar(master=self, value=1)
            self.checkbuttons_state[status.strip()] = var

    def checkbutton_callback(self, current_var, name):
        if name == "todo" and current_var.get():
            for status, var in self.checkbuttons_state.items():
                if status != "todo" and var.get():
                    var.set(0)
        elif name != "todo" and current_var.get():
            todo = self.checkbuttons_state["todo"]
            if todo.get():
                todo.set(0)

    def apply(self):
        self.comment = self.comment_field.get("1.0", tk.END).strip()
        self.result = " + ".join([status for status in self.statuses if self.checkbuttons_state[status].get()])
        if self.comment:
            self.result += " // " + self.comment

    def select_all(self):
        self.comment_field.tag_add(tk.SEL, "1.0", tk.END + "-1c")
        self.comment_field.mark_set(tk.INSERT, tk.END + "-1c")
        self.comment_field.see(tk.INSERT)
        return "break"
