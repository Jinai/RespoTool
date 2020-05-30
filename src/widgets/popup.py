# -*- coding: utf-8 -*-
# !python3

import tkinter as tk


class Popup(tk.Toplevel):
    def __init__(self, message, pos_x, pos_y, lifetime=1500, delay=0, fadein=200, fadeout=200, offset=(0, 0),
                 txt_color="white", bg_color="#111111", border_color="#999999", border_width=0, persistent=False,
                 max_alpha=1.0, **kwargs):
        super().__init__(**kwargs)
        self.message = message            # Message to display
        self.pos_x = pos_x                # Top left corner position on x-axis
        self.pos_y = pos_y                # Top left corner position on y-axis
        self.lifetime = lifetime          # Time the popup stays on screen, not counting fade in/out (milliseconds)
        self.delay = delay                # Delay before fadein begins (milliseconds)
        self.fadein = fadein              # Duration of fadein (milliseconds)
        self.fadeout = fadeout            # Duration of fadeout (milliseconds)
        self.offset = offset              # (x,y) offset from pos (pixels)
        self.txt_color = txt_color        # Color the message will appear in
        self.bg_color = bg_color          # Background color of the popup
        self.border_color = border_color  # Border color of the popup
        self.border_width = border_width  # Border width of the popup
        self.persistent = persistent      # Disable fadeout if true
        self.max_alpha = max_alpha        # 1 = opaque, <1 = transparent
        self.refresh_delay = 30           # Delay between each transparency adjustment (milliseconds)
        self.alpha_fadein = (self.max_alpha / self.fadein) * self.refresh_delay  # Fadein transparency increment
        self.alpha_fadeout = (self.max_alpha / self.fadeout) * self.refresh_delay  # Fadeout transparency decrement
        self._fadein_after_id = None
        self.setup()

    def setup(self):
        self.overrideredirect(True)  # Removes title bar
        self.wm_geometry("+{}+{}".format(self.pos_x + self.offset[0], self.pos_y + self.offset[1]))
        self.attributes("-alpha", 0.0)  # Set transparency to 0%
        self.frame = tk.Frame(self, highlightbackground=self.border_color, highlightcolor=self.border_color,
                              highlightthickness=self.border_width, bd=0)
        self.frame.pack()
        self.label = tk.Label(self.frame, text=self.message, justify="left", fg=self.txt_color, bg=self.bg_color)
        self.label.pack()
        self.after(self.delay, self.fade_in)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < self.max_alpha:
            alpha += self.alpha_fadein
            self.attributes("-alpha", alpha)
            self._fadein_after_id = self.after(self.refresh_delay, self.fade_in)
        elif not self.persistent:
            self.after(self.lifetime, self.fade_out)

    def fade_out(self):
        self._cancel_fade_in()
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= self.alpha_fadeout
            self.attributes("-alpha", alpha)
            self.after(self.refresh_delay, self.fade_out)
        else:
            self.destroy()

    def _cancel_fade_in(self):
        after_id = self._fadein_after_id
        self._fadein_after_id = None
        if after_id:
            self.after_cancel(after_id)
