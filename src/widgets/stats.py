# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont


class LabelPair(tk.Frame):
    def __init__(self, master, left, right, **opts):
        tk.Frame.__init__(self, master, **opts)
        self.master = master
        self.left = left
        self.right = right
        self.setup()

    def setup(self):
        self.label_left = ttk.Label(self, text=self.left)
        self.label_left.pack(side="left")
        f = tkFont.Font(family="Segoe UI", size=9, weight="bold")
        self.label_right = ttk.Label(self, text=self.right, font=f)
        self.label_right.pack(side="right")


class Stats(ttk.LabelFrame):
    def __init__(self, master, **opts):
        ttk.Labelframe.__init__(self, master, **opts)
        self.master = master
        self.setup()

    def setup(self):
        lp_suppr = LabelPair(self, "Suppr : ", "78")
        lp_reclasse = LabelPair(self, "Reclassé : ", "55")
        lp_corrige = LabelPair(self, "Corrigé : ", "34")
        sep = ttk.Separator(self, orient="vertical")
        lp_reset = LabelPair(self, "Rec reset : ", "10")
        lp_ignore = LabelPair(self, "Ignoré : ", "14")
        lp_archive = LabelPair(self, "Archivé : ", "191")

        lp_suppr.grid(row=0, column=0, sticky="nsew")
        lp_reclasse.grid(row=1, column=0, sticky="nsew")
        lp_corrige.grid(row=2, column=0, sticky="nsew", pady=(0, 7))
        sep.grid(row=0, column=1, rowspan=3, sticky="ns", padx=5, pady=(0, 7))
        lp_reset.grid(row=0, column=2, sticky="nsew")
        lp_ignore.grid(row=1, column=2, sticky="nsew")
        lp_archive.grid(row=2, column=2, sticky="nsew", pady=(0, 7))

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)


if __name__ == '__main__':
    root = tk.Tk()
    st = Stats(root, text="Stats")
    st.pack(expand=True, fill="both")
    root.mainloop()
