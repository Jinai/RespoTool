# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict

import utils
from widgets.dialogs.basedialog import BaseDialog


class EditSigDialog(BaseDialog):
    def __init__(self, master, *, statuses, original_text, **kwargs):
        super().__init__(master, **kwargs)
        self.statuses = statuses
        self.original_text = original_text
        self.parsed_state = OrderedDict()
        self.comment = ""
        self.parse_original_text()

    def body(self, container):
        # Checkbuttons for statuses
        checkbuttons_frame = ttk.Frame(container)
        checkbuttons_frame.pack(fill="both", expand=True, side="top")
        for chunk in utils.sequence_chunker(self.statuses, 3):
            column = ttk.Frame(checkbuttons_frame)
            column.pack(fill="both", expand=True, side="left")
            for status in chunk:
                if status in self.parsed_state:
                    var = self.parsed_state[status]
                else:
                    var = tk.IntVar(master=self, value=0)
                    self.parsed_state[status] = var

                command = lambda var=var, status=status: self.validate_status(var, status)
                cb = ttk.Checkbutton(column, text=status.title(), variable=var, takefocus=False, command=command)
                cb.pack(side="top", anchor="w")

        # Text area for comments
        comment_frame = ttk.Frame(container)
        comment_frame.pack(fill="both", expand=True, pady=5)
        comment_label = ttk.Label(comment_frame, text="Commentaire :")
        comment_label.pack(anchor="w")
        self.comment_field = tk.Text(comment_frame, width=60, height=4, wrap="word", font=("Segoe UI", 9), undo=True,
                                     exportselection=False, autoseparators=True, maxundo=-1)
        self.comment_field.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(comment_frame, command=self.comment_field.yview)
        scrollbar.pack(fill="y", side="right")
        self.comment_field["yscrollcommand"] = scrollbar.set
        self.comment_field.bind("<Return>", lambda *_: self.ok())
        self.comment_field.bind("<Tab>", lambda _: "break")
        self.comment_field.event_add("<<select_all>>", "<Control-a>", "<Double-1>")
        self.comment_field.bind("<<select_all>>", self.select_all)

        self.comment_field.insert(tk.INSERT, self.comment)
        self.comment_field.edit_reset()  # reset undo/redo stack so that ctrl+z doesn't delete the original comment

        self.comment_field.event_generate("<<select_all>>")
        return self.comment_field

    def parse_original_text(self, status_sep="+", comment_sep="//"):
        tmp = self.original_text.split(comment_sep, 1)
        comment = ""
        if len(tmp) == 2:
            comment = tmp.pop().strip()
        self.comment = comment
        for status in tmp.pop().split(status_sep):
            var = tk.IntVar(master=self, value=1)
            self.parsed_state[status.strip()] = var

    def validate_status(self, current_var, status):
        if status != "todo" and current_var.get():
            # Remove todo if any other status is checked. Note that you can still have it if you add it last.
            self.parsed_state["todo"].set(0)
        elif not current_var.get():
            if not any([var.get() for var in self.parsed_state.values()]):
                # If no status is checked, force todo
                self.parsed_state["todo"].set(1)

    def apply(self):
        self.comment = self.comment_field.get("1.0", tk.END).strip()
        self.result = " + ".join([status for status, var in self.parsed_state.items() if var.get()])
        if self.comment:
            self.result += " // " + self.comment

    def select_all(self, event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END + "-1c")
        event.widget.mark_set(tk.INSERT, tk.END + "-1c")
        event.widget.see(tk.INSERT)
        return "break"
