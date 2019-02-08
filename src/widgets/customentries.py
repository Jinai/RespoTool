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

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.master = master
        self.has_focus = False
        self.entry = tk.Entry(self, *args, **kwargs)
        self.entry.configure(insertwidth=1, bd=0, highlightthickness=0)
        self.entry.pack(fill="both", expand=True, ipady=1, pady=1, padx=1)
        self.configure(background=CustomEntry.DARK_GREY)

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
        self.set_border_color(CustomEntry.LIGHT_BLUE)
        if self.winfo_containing(*self.winfo_pointerxy()) != self.entry:
            # Only go back to a grey border when focusing out if the
            # mouse pointer isn't over the entry
            self.set_border_color(CustomEntry.DARK_GREY)

    def __getattr__(self, item):
        # Delegates attributes/methods to the entry
        return self.entry.__getattribute__(item)


class IconEntry(CustomEntry):
    # Blends an image to the left or right side of an Entry widget

    def __init__(self, master, icon, icon_side="right", icon_bg="white", *args, **kwargs):
        CustomEntry.__init__(self, master, *args, **kwargs)
        self.icon = icon
        self.icon_side = icon_side
        self.icon_bg = icon_bg

        self.entry.pack_forget()
        self.label_icon = tk.Label(self, background=icon_bg, borderwidth=1, highlightthickness=1, image=icon,
                                   cursor="xterm")
        self.label_icon.bind("<Button-1>", lambda e: self.entry.focus_set())
        if icon_side == "right":
            self.entry.pack(side="left", fill="both", expand=True, ipady=1, padx=(1, 0), pady=1)
            self.label_icon.pack(side="right", fill="both", padx=(0, 1), pady=1)
        else:
            self.entry.pack(side="right", fill="both", expand=True, ipady=1, padx=(0, 1), pady=1)
            self.label_icon.pack(side="left", fill="both", padx=(1, 0), pady=1)


class PlaceholderEntry(IconEntry):
    # Puts a placeholder in an Entry widget (roman or italic)
    # The placeholder will automatically disappear when focusing in, and reappear
    # when focusing out if the entry is empty

    def __init__(self, master=None, placeholder="", color="#ABADB3", slant="roman",
                 icon=None, icon_side="right", icon_bg="white", **opts):
        IconEntry.__init__(self, master, icon, icon_side, icon_bg, **opts)
        self.placeholder = placeholder
        self.color = color
        self.slant = slant

        self.entry.insert(0, self.placeholder)
        self.entry.configure(foreground=self.color)
        self.set_slant(self.slant)
        self.entry.bind('<FocusIn>', self.focus_in, add="+")
        self.entry.bind('<FocusOut>', self.focus_out, add="+")

    def focus_in(self, event):
        if self.get() in ("", self.placeholder):
            self.delete(0, tk.END)
            self.entry.configure(foreground='black')
            self.set_slant("roman")
        super().focus_in(event)

    def focus_out(self, event):
        if self.get() == "":
            self.entry.configure(foreground=self.color)
            self.set_slant(self.slant)
            self.insert(0, self.placeholder)
        super().focus_out(event)

    def set_placeholder(self, new_placeholder):
        self.placeholder = new_placeholder
        self.entry.insert(0, self.placeholder)

    def set_slant(self, new_slant):
        self.font = tkfont.Font(font=tk.Entry()['font'])
        self.font.configure(slant=new_slant)
        self.entry.configure(font=self.font)
