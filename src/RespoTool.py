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
import siglist
import signalement
from _version import __version__

__author__ = "Jinai"


class RespoTool(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.signalements = []
        self._setup_widgets()
        self.title("RespoTool v" + __version__)
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def _setup_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=True, pady=5, padx=5)

        # -------------------------------------------- IMPORT / EXPORT --------------------------------------------- #

        frame_impexp = tk.Frame(main_frame)
        frame_impexp.pack(fill="both")

        labelframe_new = ttk.Labelframe(frame_impexp, text="Nouvelle session")
        labelframe_new.pack(side="left")
        button_file = ttk.Button(labelframe_new, text="Fichier", command=self.new_file)
        button_file.pack(side="left", padx=(5, 0), pady=5)
        button_clipboard = ttk.Button(labelframe_new, text="Presse-papiers", command=self.new_clipboard)
        button_clipboard.pack(side="left", padx=(0, 5), pady=5)

        labelframe_append = ttk.Labelframe(frame_impexp, text="Ajouter nouveaux sigs")
        labelframe_append.pack(side="left", padx=20)
        button_append_file = ttk.Button(labelframe_append, text="Fichier", command=self.append_file)
        button_append_file.pack(side="left", padx=(5, 0), pady=5)
        button_append_clipboard = ttk.Button(labelframe_append, text="Presse-papiers", command=self.append_clipboard)
        button_append_clipboard.pack(side="left", padx=(0, 5), pady=5)

        labelframe_session = ttk.Labelframe(frame_impexp, text="Importer / Exporter session")
        labelframe_session.pack(side="left")
        button_import = ttk.Button(labelframe_session, text="Importer", command=self.import_save)
        button_import.pack(side="left", padx=(5, 0), pady=5)
        button_export = ttk.Button(labelframe_session, text="Exporter", command=self.export_save)
        button_export.pack(side="left", padx=(0, 5), pady=5)

        # ---------------------------------------------- SIGNALEMENTS ---------------------------------------------- #

        headers = ['date', 'auteur', 'code', 'flag', 'description', 'statut']
        column_widths = [30, 40, 85, 100, 80, 350, 105]
        sort_keys = [
            lambda x: int(x[0]),
            lambda x: (int(x[0].split("/")[1]), int(x[0].split("/")[0])),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
        ]
        stretch = [False, False, False, False, False, True, False]
        self.tree_sig = siglist.Siglist(main_frame, self.signalements, headers, column_widths, sort_keys=sort_keys,
                                        stretch=stretch)
        self.tree_sig.pack(fill="both", expand=True, pady=5)

        # ------------------------------------------------ COMMANDS ------------------------------------------------ #

        frame_commands = tk.Frame(main_frame)
        frame_commands.pack()
        self.button_playlist = ttk.Button(frame_commands, text="Playlist", command=self.playlist, state="disabled")
        self.button_playlist.pack(side="left")
        self.button_archive = ttk.Button(frame_commands, text="Archiver", command=self.archive, state="disabled")
        self.button_archive.pack()

    def new_file(self):
        file_name = fdialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_name:
            with open(file_name, "r") as f:
                self.signalements = sigparser.parse(f.read())
            self.refresh()

    def new_clipboard(self):
        self.signalements = sigparser.parse(pyperclip.paste())
        self.refresh()

    def append_file(self):
        file_name = fdialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_name:
            with open(file_name, "r") as f:
                signalements = sigparser.parse(f.read())
            self.signalements.extend(signalements)
            self.refresh()

    def append_clipboard(self):
        signalements = sigparser.parse(pyperclip.paste())
        self.signalements.extend(signalements)
        self.refresh()

    def playlist(self):
        with open("playlist.txt", "w", encoding="utf-8") as f:
            for sig in self.signalements:
                f.write(str(sig) + "\n")

    def archive(self):
        msg = "Êtes-vous sûr de vouloir archiver ces signalements ?\nIls seront retirés de la liste une fois fait !"
        if mbox.askokcancel("Archiver", msg, icon="warning", parent=self):
            header = signalement.Signalement("Date", "Auteur Sig.", "Code", "Flag", "Description", "Statut").format()
            sep = "------+--------------+----------------+-------------+------------------------------------------------------------------------------------------------------+-----------------"
            if not os.path.exists("archives/archives.txt"):
                with open("archives/archives.txt", "w") as f:
                    f.write(header + "\n")
                    f.write(sep + "\n")
            with open("archives/archives.txt", "a") as f:
                for sig in self.signalements:
                    f.write(sig.format() + "\n")
            self.button_archive.configure(state="disabled")
            self.tree_sig.clear()
            del self.signalements[:]

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


if __name__ == '__main__':
    app = RespoTool()
    app.mainloop()
