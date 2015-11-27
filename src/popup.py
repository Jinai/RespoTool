# -*- coding: utf-8 -*-
# !python3

import tkinter as tk


class Popup(tk.Toplevel):
    def __init__(self, message, cursor_x, cursor_y, lifetime=1500, delay=0, fadein=200, fadeout=600, offset=(10, -20),
                 **options):
        tk.Toplevel.__init__(self, **options)
        self.message = message  # Message to display
        self.cursor_x = cursor_x  # Position of cursor in x axis
        self.cursor_y = cursor_y  # Position of cursor in y axis
        self.lifetime = lifetime  # Time the popup stays on screen (milliseconds)
        self.delay = delay  # Delay before fadein begins (milliseconds)
        self.fadein = fadein  # Duration of fadein (milliseconds)
        self.fadeout = fadeout  # Duration of dadeout (milliseconds)
        self.offset = offset  # (x,y) offset from cursor (pixels)
        self.refresh_delay = 30  # Delay between each transparency adjustment (milliseconds)
        self.alpha_fadein = (1 / self.fadein) * self.refresh_delay  # Fadein transparency increment
        self.alpha_fadeout = (1 / self.fadeout) * self.refresh_delay  # Fadeout transparency decrement

        self.after(self.delay, self.setup)

    def setup(self):
        self.overrideredirect(True)  # Removes title bar
        self.wm_geometry("+{}+{}".format(self.cursor_x + self.offset[0], self.cursor_y + self.offset[1]))
        self.attributes("-alpha", 0.0)  # Set transparency to 0%
        self.label = tk.Label(self, text=self.message, justify="left", background="#ffffff", relief="solid",
                              borderwidth=1)
        self.label.pack()
        self.fade_in()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            alpha += self.alpha_fadein
            self.attributes("-alpha", alpha)
            self.after(self.refresh_delay, self.fade_in)
        else:
            self.after(self.lifetime, self.fade_out)

    def fade_out(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= self.alpha_fadeout
            self.attributes("-alpha", alpha)
            self.after(self.refresh_delay, self.fade_out)
        else:
            self.destroy()
