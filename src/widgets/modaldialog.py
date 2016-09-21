# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk


class ModalDialog(tk.Toplevel):
    def __init__(self, parent, title=None, can_resize=False):
        super(ModalDialog, self).__init__()
        self.parent = parent
        if title:
            self.title(title)
        self.can_resize = can_resize
        self.result = None

        self.attributes('-alpha', 0.0)
        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=5, pady=5)
        self.initial_focus = self.body(body)
        self.buttonbox()
        if not self.initial_focus:
            self.initial_focus = self
        self.initial_focus.focus_set()
        self.initial_focus.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        self.center(parent)
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        self.resizable(width=self.can_resize, height=self.can_resize)
        self.attributes('-alpha', 1.0)
        # self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    #
    # construction hooks

    def center(self, master):
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + (2 * frm_width)
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = master.winfo_rootx() + (master.winfo_width() // 2) - (win_width // 2)
        y = master.winfo_rooty() + (master.winfo_height() // 2) - (win_height // 2) - 9
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)
        box.pack()
        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        return 1  # override

    def apply(self):
        pass  # override


class InfoModal(ModalDialog):
    def __init__(self, parent, title=None, body_text='', button_text="OK"):
        self.body_text = body_text
        self.button_text= button_text
        ModalDialog.__init__(self, parent, title)

    def body(self, master):
        self.msg = tk.Message(master, text=self.body_text, width=300)
        self.msg.pack()
        return self.msg

    def buttonbox(self):
        box = tk.Frame(self)
        box.pack()
        w = ttk.Button(box, text=self.button_text, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
