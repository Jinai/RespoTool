# -*- coding: utf-8 -*-
# !python3

import tkinter as tk


class Popup(tk.Toplevel):
    def __init__(self, message, pos_x, pos_y, lifetime=1500, delay=0, fadein=200, fadeout=600, offset=(10, -20),
                 txt_color="black", bg_color="#F0F0F0", persistent=False, max_alpha=1.0, **options):
        tk.Toplevel.__init__(self, **options)
        self.message = message        # Message to display
        self.pos_x = pos_x            # Top left corner position on x-axis
        self.pos_y = pos_y            # Top left corner position on y-axis
        self.lifetime = lifetime      # Time the popup stays on screen (milliseconds)
        self.delay = delay            # Delay before fadein begins (milliseconds)
        self.fadein = fadein          # Duration of fadein (milliseconds)
        self.fadeout = fadeout        # Duration of fadeout (milliseconds)
        self.offset = offset          # (x,y) offset from pos (pixels)
        self.txt_color = txt_color    # Color the message will appear in
        self.bg_color = bg_color      # Background color of the popup
        self.persistent = persistent  # Disable fadeout if true
        self.max_alpha = max_alpha    # 1 = opaque, <1 = transparent
        self.refresh_delay = 30       # Delay between each transparency adjustment (milliseconds)
        self.alpha_fadein = (self.max_alpha / self.fadein) * self.refresh_delay    # Fadein transparency increment
        self.alpha_fadeout = (self.max_alpha / self.fadeout) * self.refresh_delay  # Fadeout transparency decrement
        self.setup()

    def setup(self):
        self.overrideredirect(True)  # Removes title bar
        self.wm_geometry("+{}+{}".format(self.pos_x + self.offset[0], self.pos_y + self.offset[1]))
        self.attributes("-alpha", 0.0)  # Set transparency to 0%
        self.label = tk.Label(self, text=self.message, justify="left", fg=self.txt_color, bg=self.bg_color)
        self.label.pack()
        self.after(self.delay, self.fade_in)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < self.max_alpha:
            alpha += self.alpha_fadein
            self.attributes("-alpha", alpha)
            self.after(self.refresh_delay, self.fade_in)
        elif not self.persistent:
            self.after(self.lifetime, self.fade_out)

    def fade_out(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= self.alpha_fadeout
            self.attributes("-alpha", alpha)
            self.after(self.refresh_delay, self.fade_out)
        else:
            self.destroy()
