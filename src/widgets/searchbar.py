# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.font as tkfont


class CustomEntry(tk.Frame):
    # This widget emulates the graphical behaviour of a ttk.Entry widget (on Windows),
    # using a frame as a colored border and a normal tk.Entry widget embedded inside

    LIGHT_BLUE = "#7EB4EA"
    DARK_BLUE = "#569DE5"
    DARK_GREY = "#ABADB3"

    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.master = master
        self.has_focus = False
        self.entry = tk.Entry(self, **kwargs)
        self.entry.configure(insertwidth=1, bd=0, highlightthickness=0)
        self.entry.pack(fill="both", expand=True, ipady=1, pady=1, padx=1)
        self.set_border_color(CustomEntry.DARK_GREY)

        self.entry.bind("<FocusIn>", self.focus_in)
        self.entry.bind("<FocusOut>", self.focus_out)
        self.entry.bind("<Enter>", lambda e: None if self.has_focus else self.set_border_color(CustomEntry.LIGHT_BLUE))
        self.entry.bind("<Leave>", lambda e: None if self.has_focus else self.set_border_color(CustomEntry.DARK_GREY))

        self.focus = self.entry.focus  # Focusing the frame should focus the entry instead

    def set_border_color(self, color):
        self.configure(background=color)

    def disable_border(self):
        self.entry.pack_forget()
        self.entry.pack(fill="both", expand=True, ipady=1)

    def enable_border(self):
        self.entry.pack_forget()
        self.entry.pack(fill="both", expand=True, ipady=1, padx=1, pady=1)

    def focus_in(self, event):
        self.has_focus = True
        self.set_border_color(CustomEntry.DARK_BLUE)

    def focus_out(self, event):
        self.has_focus = False
        if self.winfo_containing(*self.winfo_pointerxy()) == self.entry:
            # Mouse pointer still over the entry
            self.entry.event_generate("<Enter>")
        else:
            self.set_border_color(CustomEntry.DARK_GREY)

    def __getattr__(self, item):
        # Delegates attributes/methods to the entry
        return self.entry.__getattribute__(item)


class SearchBar(CustomEntry):
    # A search bar with an optional placeholder / icon
    #
    # The placeholder will automatically disappear when focusing in, and reappear
    # when focusing out if the entry is empty.
    #
    # The icon can be placed on the right or left side of the entry and will blend
    # in nicely.

    def __init__(self, master, *, placeholder_options=None, icon_options=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        placeholder_options = placeholder_options if placeholder_options else {}
        self.placeholder_text = placeholder_options.get("text", "")
        self.placeholder_color = placeholder_options.get("color", "#ABADB3")
        self.placeholder_slant = placeholder_options.get("slant", "roman")
        icon_options = icon_options if icon_options else {}
        self.icon_path = icon_options.get("path", None)
        self.icon_path_alt = icon_options.get("alt", None)
        self.icon_side = icon_options.get("side", "right")
        self.icon_background = icon_options.get("background", self.entry.cget("background"))

        if self.icon_path:
            if self.icon_path_alt:
                self.icon_alt = tk.PhotoImage(file=self.icon_path_alt)
            self.entry.pack_forget()
            self.icon = tk.PhotoImage(file=self.icon_path)
            self.label_icon = tk.Label(self, image=self.icon, background=self.icon_background, cursor="xterm",
                                       borderwidth=1, highlightthickness=1)
            self.label_icon.bind("<Button-1>", lambda e: self.entry.focus_set())
            if self.icon_side == "right":
                self.entry.pack(side="left", fill="both", expand=True, ipady=1, padx=(1, 0), pady=1)
                self.label_icon.pack(side="right", fill="both", padx=(0, 1), pady=1)
            else:
                self.entry.pack(side="right", fill="both", expand=True, ipady=1, padx=(0, 1), pady=1)
                self.label_icon.pack(side="left", fill="both", padx=(1, 0), pady=1)

        if self.placeholder_text:
            self.entry.insert(0, self.placeholder_text)
            self.entry.configure(foreground=self.placeholder_color)
            self.set_slant(self.placeholder_slant)
            self.entry.bind("<FocusIn>", self.focus_in, add="+")
            self.entry.bind("<FocusOut>", self.focus_out, add="+")

    def focus_in(self, event):
        if self.icon_path_alt:
            self.label_icon.configure(image=self.icon_alt)
        if self.get() in ("", self.placeholder_text):
            self.delete(0, tk.END)
            self.entry.configure(foreground="black")
            self.set_slant("roman")
        super().focus_in(event)

    def focus_out(self, event):
        if self.icon_path_alt:
            self.label_icon.configure(image=self.icon)
        if self.get() == "":
            self.entry.configure(foreground=self.placeholder_color)
            self.set_slant(self.placeholder_slant)
            self.insert(0, self.placeholder_text)
        super().focus_out(event)

    def set_placeholder(self, new_placeholder):
        self.placeholder_text = new_placeholder
        self.entry.insert(0, self.placeholder_text)

    def set_slant(self, new_slant):
        self.font = tkfont.Font(font=tk.Entry()["font"])
        self.font.configure(slant=new_slant)
        self.entry.configure(font=self.font)
