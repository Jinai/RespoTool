# -*- coding: utf-8 -*-
# !python3

import os
import pickle
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
import tkinter.filedialog as fdialog

import pyperclip
import sigparser
import signalement
from widgets import siglist, stats
from _version import __version__

__author__ = "Jinai"


class RespoTool(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.signalements = []
        self._setup_widgets()
        self.title("RespoTool v" + __version__)
        self.update_idletasks()
        self.minsize(742, self.winfo_reqheight())
        try:
            self.tk.call('encoding', 'system', 'utf-8')
            self.iconbitmap("resources/respotool.ico")
        except:
            pass
        self.bind('<Control-q>', lambda _: self.quit())

    def _setup_widgets(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True, pady=5, padx=5)

        # -------------------------------------------- IMPORT / EXPORT --------------------------------------------- #

        self.labelframe_new = ttk.Labelframe(self.main_frame, text="Nouvelle session")
        button_file = ttk.Button(self.labelframe_new, text="Fichier", command=self.new_file)
        button_file.pack(fill="both", expand=True, side="left", padx=(7, 0), pady=(0, 7))
        button_clipboard = ttk.Button(self.labelframe_new, text="Presse-papiers", command=self.new_clipboard)
        button_clipboard.pack(fill="both", expand=True, side="right", padx=(0, 7), pady=(0, 7))

        self.labelframe_append = ttk.Labelframe(self.main_frame, text="Ajouter nouveaux sigs")
        button_append_file = ttk.Button(self.labelframe_append, text="Fichier", command=self.append_file)
        button_append_file.pack(fill="both", expand=True, side="left", padx=(7, 0), pady=(0, 7))
        button_append_clipboard = ttk.Button(self.labelframe_append, text="Presse-papiers", command=self.append_clipboard)
        button_append_clipboard.pack(fill="both", expand=True, side="right", padx=(0, 7), pady=(0, 7))

        self.labelframe_session = ttk.Labelframe(self.main_frame, text="Importer / Exporter session")
        button_import = ttk.Button(self.labelframe_session, text="Importer", command=self.import_save)
        button_import.pack(fill="both", expand=True, side="left", padx=(7, 0), pady=(0, 7))
        button_export = ttk.Button(self.labelframe_session, text="Exporter", command=self.export_save)
        button_export.pack(fill="both", expand=True, side="right", padx=(0, 7), pady=(0, 7))

        # ---------------------------------------------- SIGNALEMENTS ---------------------------------------------- #

        headers = ['date', 'auteur', 'code', 'flag', 'description', 'statut']
        column_widths = [30, 40, 85, 100, 80, 350, 300]
        sort_keys = [
            lambda x: int(x[0]),
            lambda x: (int(x[0].split("/")[1]), int(x[0].split("/")[0])),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
        ]
        stretch = [False, False, False, False, False, True, True]
        self.tree_sig = siglist.Siglist(self.main_frame, self.signalements, False, headers, column_widths, sort_keys=sort_keys,
                                        stretch=stretch)

        # ------------------------------------------------ ACTIONS ------------------------------------------------- #

        #self.labelframe_stats = stats.Stats(self.main_frame, text="Archives")

        self.frame_actions = tk.Frame(self.main_frame)
        self.frame_act1 = tk.Frame(self.frame_actions)
        self.frame_act1.pack()
        self.button_archive = ttk.Button(self.frame_act1, text="Archiver", command=self.archive, state="disabled",
                                         width=16)
        self.button_archive.pack(side="left")
        self.button_archive_selection = ttk.Button(self.frame_act1, text="Archiver sélection", state="disabled",
                                                   command=self.archive_selection, width=16)
        self.button_archive_selection.pack(side="right")


        self.frame_act2 = tk.Frame(self.frame_actions)
        self.frame_act2.pack()
        self.button_playlist = ttk.Button(self.frame_act2, text="Playlist", command=self.playlist, state="disabled",
                                          width=16)
        self.button_playlist.pack(side="left")
        self.button_sigmdm = ttk.Button(self.frame_act2, text="Obtenir sigmdm", state="disabled", command=self.sigmdm,
                                        width = 16)
        self.button_sigmdm.pack(side="right")

        # ------------------------------------------- WIDGETS PLACEMENT -------------------------------------------- #

        self.labelframe_new.grid(row=0, column=0, sticky="nsew")
        self.labelframe_append.grid(row=0, column=1, sticky="nsew", padx=10)
        self.labelframe_session.grid(row=0, column=2, sticky="nsew")
        self.tree_sig.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        #self.labelframe_stats.grid(row=2, column=0, sticky="nw")
        self.frame_actions.grid(row=2, column=1, sticky="nsew", pady=(0, 5))

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)

    def new_file(self):
        file_name = fdialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                self.signalements = sigparser.parse(f.read(), self._allow_duplicates.get())
            self.refresh()

    def new_clipboard(self):
        self.signalements = sigparser.parse(pyperclip.paste(), self._allow_duplicates.get())
        self.refresh()

    def append_file(self):
        file_name = fdialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                signalements = sigparser.parse(f.read(), self._allow_duplicates.get())
            self.signalements.extend(signalements)
            self.refresh()

    def append_clipboard(self):
        signalements = sigparser.parse(pyperclip.paste(), self._allow_duplicates.get())
        self.signalements.extend(signalements)
        self.refresh()

    def playlist(self):
        with open("playlist.txt", "w", encoding="utf-8") as f:
            for sig in self.signalements:
                f.write(str(sig) + "\n")

    def archive(self):
        msg = "Êtes-vous sûr de vouloir archiver ces signalements ?\nNe le faites que s'ils sont tous traités, " + \
              "car ils seront retirés de la liste une fois fait !"
        if mbox.askokcancel("Archiver", msg, icon="warning", parent=self):
            self.create_archive()
            with open("archives/archives.txt", "a", encoding="utf-8") as f:
                for sig in self.signalements:
                    f.write(sig.format() + "\n")
            del self.signalements[:]
            self.refresh()
            self.button_archive.configure(state="disabled")

    def archive_selection(self):
        indexes = self.tree_sig.selection_indexes()
        if self.check_valid_selection(indexes):
            msg = "Êtes-vous sûr de vouloir archiver ces signalements ?\nNe le faites que s'ils sont tous traités, " + \
                  "car ils seront retirés de la liste une fois fait !"
            if mbox.askokcancel("Archiver", msg, icon="warning", parent=self):
                self.create_archive()
                with open("archives/archives.txt", "a", encoding="utf-8") as f:
                    for i in indexes:
                        f.write(self.signalements[i].format() + "\n")
                    self.signalements = [sig for i, sig in enumerate(self.signalements) if i not in indexes]
                self.refresh()
        else:
            msg = ("Votre sélection doit être d'un seul bloc (pas de trous) et doit commencer par le premier " +
                   "signalement afin de conserver l'ordre des archives")
            mbox.showwarning("Mauvais archivage", msg)

    def create_archive(self):
        if not os.path.exists("archives/archives.txt"):
            header = signalement.Signalement("Date", "Auteur Sig.", "Code", "Flag", "Description", "Statut").format()
            sep = "------+--------------+----------------+-------------+---------------------------------------------" \
                  + "---------------------------------------------------------+-----------------"
            with open("archives/archives.txt", "w", encoding="utf-8") as f:
                f.write(header + "\n")
                f.write(sep + "\n")

    def check_valid_selection(self, indexes):
        for pos, idx in enumerate(indexes):
            if pos != idx:
                return False
        return len(indexes)

    def sigmdm(self):
        res = ""
        for sig in self.signalements:
            res += sig.sigmdm() + "\n"
        pyperclip.copy(res)

    def export_save(self):
        file_name = fdialog.asksaveasfilename(initialdir="saves", initialfile='session', defaultextension='.sig')
        if file_name:
            with open(file_name, "wb") as f:
                pickle.dump(self.signalements, f)

    def import_save(self):
        file_name = fdialog.askopenfilename(initialdir="saves",
                                            filetypes=(("Sig Files", "*.sig"), ("All Files", "*.*")))
        if file_name:
            with open(file_name, "rb") as f:
                self.signalements = pickle.load(f)
            self.refresh()

    def refresh(self):
        self.tree_sig.signalements = self.signalements
        self.tree_sig.refresh()
        self.button_playlist.configure(state="enabled")
        self.button_archive.configure(state="enabled")
        self.button_archive_selection.configure(state="enabled")
        self.button_sigmdm.configure(state="enabled")

    def quit(self):
        raise SystemExit

if __name__ == '__main__':
    app = RespoTool()
    app.mainloop()
