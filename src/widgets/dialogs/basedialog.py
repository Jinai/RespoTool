# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk


class BaseDialog(tk.Toplevel):
    def __init__(self, master, *, dialog_title=None, can_resize=True, centered=True, is_modal=True, is_transient=True,
                 **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.master = master
        self.dialog_title = dialog_title
        self.can_resize = can_resize
        self.centered = centered
        self.is_modal = is_modal
        self.is_transient = is_transient
        self.result = None

    #
    # construction hooks

    def spawn(self):
        self.attributes("-alpha", 0.0)
        self.deiconify()
        self.title(self.dialog_title)
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.body_frame = ttk.Frame(self.main_frame)
        self.body_frame.pack(fill="both", expand=True)
        self.buttonbox_frame = ttk.Frame(self.main_frame)
        self.buttonbox_frame.pack(fill="both", expand=True)
        self.initial_focus = self.body(self.body_frame)
        self.buttonbox(self.buttonbox_frame)
        if not self.initial_focus:
            self.initial_focus = self
        self.initial_focus.focus_set()
        self.initial_focus.focus_force()
        self.protocol("WM_DELETE_WINDOW", lambda *_: self.cancel())
        self.bind("<Return>", lambda *_: self.ok())
        self.bind("<Escape>", lambda *_: self.cancel())
        if self.centered:
            self.center(self.master)
        else:
            self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        self.resizable(width=self.can_resize, height=self.can_resize)
        self.attributes("-alpha", 1.0)
        if self.is_transient:
            self.transient(self.master)
        if self.is_modal:
            self.master_window = self.master.winfo_toplevel()
            self.master_window.wm_attributes("-disabled", True)
            self.grab_set()
            self.wait_window(self)

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
        self.geometry("{}x{}+{}+{}".format(width, height, x, y))

    def body(self, container):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self, container):
        # add standard button box. override if you don't want the
        # standard buttons
        wrap = ttk.Frame(container)
        wrap.pack(padx=10, pady=(10, 5))
        self.button_ok = ttk.Button(wrap, text="OK", width=13, command=self.ok, default="active")
        self.button_ok.pack(side="left", padx=3)
        self.button_cancel = ttk.Button(wrap, text="Annuler", width=13, command=self.cancel)
        self.button_cancel.pack(side="right", padx=3)

    #
    # standard button semantics

    def ok(self):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.apply()
        self.cancel()

    def cancel(self):
        # put focus back to the parent window
        if self.is_modal:
            self.master_window.wm_attributes("-disabled", False)
        self.destroy()

    #
    # command hooks

    def validate(self):
        return True  # override

    def apply(self):
        pass  # override
