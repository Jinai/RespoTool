# -*- coding: utf-8 -*-
# !python3

import json
import logging
import os
import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.messagebox as mbox
import tkinter.ttk as ttk

import pyperclip

import archives
import signalement
import sigparser
import utils
from _meta import __version__
from widgets import customentries, modaldialog, siglist, statusbar


class RespoTool(tk.Tk):
    def __init__(self, master=None, session_path=None, archives_dir=None, archives_pattern=None, auto_import=False,
                 warning=True, warning_msg=""):
        # Init var
        tk.Tk.__init__(self, master)
        self.master = master
        self.session_path = session_path
        self.archives_dir = archives_dir
        self.auto_import = auto_import
        self.warning = warning
        self.warning_msg = warning_msg
        self.current_respo = tk.StringVar()
        with open("data/respomaps.json", 'r', encoding='utf-8') as f:
            self.respomaps = json.load(f)
        with open("data/contact.json", 'r', encoding='utf-8') as f:
            self.contact = json.load(f)
        self.signalements = []
        self.archives = archives.Archives(archives_dir, archives_pattern)

        # Rendering
        self._setup_widgets()
        self.title("RespoTool " + __version__)
        self.update_idletasks()
        self.minsize(742, self.winfo_reqheight())
        try:
            self.tk.call('encoding', 'system', 'utf-8')
            self.iconbitmap("data/img/respotool.ico")
        except Exception as e:
            logging.error(e)

        # Imports
        if self.auto_import:
            if self.session_path and os.path.exists(self.session_path):
                self.import_save(self.session_path)

        # Bindings
        self.bind('<Control-s>', lambda _: self.export_save())
        self.bind('<Control-o>', lambda _: self.import_save())
        self.bind('<Control-f>', lambda _: self.search())
        self.bind('<Control-q>', lambda _: self.quit())
        self.main_frame.bind('<Control-v>', lambda _: self.append_clipboard())
        self.main_frame.bind('<Button-1>', lambda _: self.clear_focus())
        self.tree_sig.tree.bind('<<TreeviewSelect>>', lambda _: self.selection_handler(), add="+")
        self.current_respo.trace("w", lambda *_: logging.debug("Setting respo={}".format(self.current_respo.get())))
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Warnings
        if self.warning:
            modaldialog.InfoModal(self, "RespoTool " + __version__, self.warning_msg, "J'ai compris").spawn()

    def _setup_widgets(self):
        self.statusbar = statusbar.StatusBar(self)
        self.statusbar.pack(side="bottom", fill="x")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True, pady=5, padx=5)

        # -------------------------------------------- IMPORT / EXPORT --------------------------------------------- #

        self.labelframe_new = ttk.Labelframe(self.main_frame, text="Nouvelle session")
        button_new_file = ttk.Button(self.labelframe_new, text="Fichier", command=self.new_file)
        button_new_file.pack(fill="both", expand=True, side="left", padx=(7, 0), pady=(0, 7))
        button_new_cb = ttk.Button(self.labelframe_new, text="Presse-papiers", command=self.new_clipboard)
        button_new_cb.pack(fill="both", expand=True, side="right", padx=(0, 7), pady=(0, 7))

        self.labelframe_append = ttk.Labelframe(self.main_frame, text="Ajouter nouveaux sigs")
        button_append_file = ttk.Button(self.labelframe_append, text="Fichier", command=self.append_file)
        button_append_file.pack(fill="both", expand=True, side="left", padx=(7, 0), pady=(0, 7))
        button_append_cb = ttk.Button(self.labelframe_append, text="Presse-papiers", command=self.append_clipboard)
        button_append_cb.pack(fill="both", expand=True, side="right", padx=(0, 7), pady=(0, 7))

        self.labelframe_session = ttk.Labelframe(self.main_frame, text="Importer / Exporter session")
        button_import = ttk.Button(self.labelframe_session, text="Importer", command=self.import_save)
        button_import.pack(fill="both", expand=True, side="left", padx=(7, 0), pady=(0, 7))
        button_export = ttk.Button(self.labelframe_session, text="Exporter", command=self.export_save)
        button_export.pack(fill="both", expand=True, side="right", padx=(0, 7), pady=(0, 7))

        button_new_file.configure(state="disabled")
        button_new_cb.configure(state="disabled")
        button_append_file.configure(state="disabled")

        # ----------------------------------------- CURRENT RESPO & SEARCH ----------------------------------------- #

        self.frame_respo = tk.Frame(self.main_frame)
        self.icon_respo = tk.PhotoImage(file="data/img/shield_respo.png")
        lbl_icon_respo = tk.Label(self.frame_respo, image=self.icon_respo)
        lbl_icon_respo.pack(side="left")
        label_respo = ttk.Label(self.frame_respo, text="Respomap  :  ")
        label_respo.pack(side="left")
        self.dropdown_respo = ttk.Combobox(self.frame_respo, state='readonly', textvariable=self.current_respo)
        self.dropdown_respo.pack(side="right")
        self.dropdown_respo['values'] = self.respomaps['main']  # comptes principaux

        self.frame_search = tk.Frame(self.main_frame)
        search_icon = tk.PhotoImage(file="data/img/search.gif")
        self.entry_search = customentries.PlaceholderEntry(self.frame_search, placeholder=" Rechercher",
                                                           icon=search_icon,
                                                           width=30)
        self.entry_search.pack(side="right")
        self.label_matches = ttk.Label(self.frame_search, foreground="grey40")
        self.label_matches.pack(side="right", padx=(0, 5))

        # ---------------------------------------------- SIGNALEMENTS ---------------------------------------------- #

        headers = ['date', 'auteur', 'code', 'flag', 'description', 'statut', 'respomap']
        column_widths = [30, 40, 85, 100, 80, 350, 300, 100]
        sort_keys = [
            lambda x: int(x[0]),
            lambda x: (int(x[0].split("/")[1]), int(x[0].split("/")[0])),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
            lambda x: x[0].lower(),
        ]
        stretch = [False, False, False, False, False, True, True, True]
        self.tree_sig = siglist.Siglist(self.main_frame, self.signalements, self.current_respo, self.archives, headers,
                                        column_widths, sort_keys=sort_keys, stretch=stretch, sortable=False,
                                        auto_increment=True, search_excludes=["Rechercher"], match_template="{} sur {}")
        self.entry_search.entry.configure(textvariable=self.tree_sig._search_key)
        self.label_matches.configure(textvariable=self.tree_sig._matches_label)

        # ------------------------------------------------ ACTIONS ------------------------------------------------- #

        self.frame_actions = tk.Frame(self.main_frame)
        self.button_generate_mp = ttk.Button(self.frame_actions, command=self.generate_contact_message)
        self.button_generate_mp.pack(side="left")
        self.button_archive_selection = ttk.Button(self.frame_actions, command=self.archive_selection)
        self.button_archive_selection.pack(side="right")

        self.button_generate_mp.configure(text="Générer MP", width=16, state="disabled")
        self.button_archive_selection.configure(text="Archiver sélection", width=16, state="disabled")

        # ------------------------------------------- WIDGETS PLACEMENT -------------------------------------------- #

        self.labelframe_new.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.labelframe_append.grid(row=0, column=1, sticky="nsew", padx=5)
        self.labelframe_session.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        self.frame_respo.grid(row=1, column=0, sticky="w", pady=10)
        self.frame_search.grid(row=1, column=2, sticky="e", padx=(0, 17), pady=10)
        self.tree_sig.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        self.frame_actions.grid(row=3, column=1)

        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="_")
        # Changes the widget stack order so that pressing Tab after setting the Respomap brings the focus directly to
        # the table instead of giving the focus to the search bar. Not doing so would clear the selected items in the
        # table upon entering the search bar, which is unwanted. This is particularly useful when one forgets to set
        # the Respomap value and is prompted with it before being able to edit a status.
        self.frame_search.lower()
        # Needed to rewrite the placeholder because we hooked an empty StringVar that erased it
        self.entry_search.focus_out(None)

    def selection_handler(self):
        selection = self.tree_sig.tree.selection()
        if len(selection) == 0:
            self.button_generate_mp.configure(state="disabled")
            self.button_archive_selection.configure(state="disabled")
        elif len(selection) == 1:
            self.button_generate_mp.configure(state="enabled")
            self.button_archive_selection.configure(state="enabled")
        elif len(selection) > 1:
            self.button_generate_mp.configure(state="disabled")
            self.button_archive_selection.configure(state="enabled")

    def new_file(self):
        filename = fdialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                self.signalements = sigparser.parse(f.read())
            if self.signalements:
                self.refresh(scroll="up")
                self.statusbar.set(
                    "Nouvelle session depuis '{}', {} signalements importés.".format(filename, len(self.signalements))
                )

    def new_clipboard(self):
        self.signalements = sigparser.parse(pyperclip.paste())
        if self.signalements:
            self.refresh(scroll="up")
            self.statusbar.set(
                "Nouvelle session depuis le presse-papiers, {} signalements importés.".format(len(self.signalements))
            )

    def append_file(self):
        filename = fdialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                signalements = sigparser.parse(f.read())
            if signalements:
                self.signalements.extend(signalements)
                self.refresh(scroll="down")
                self.statusbar.set(
                    "{} signalements ajoutés à la session courante depuis '{}'.".format(len(signalements), filename)
                )

    def append_clipboard(self):
        signalements = sigparser.parse(pyperclip.paste())
        if signalements:
            self.signalements.extend(signalements)
            self.refresh(scroll="down")
            self.statusbar.set(
                "{} signalements ajoutés à la session courante depuis le presse-papiers.".format(len(signalements))
            )

    def generate_contact_message(self):
        sig = self.tree_sig.get_selected_sigs()[0]
        template = "\n".join(self.contact['message'])
        message = template.format(**sig.__dict__)
        pyperclip.copy(message)
        self.statusbar.set("MP copié dans le presse-papiers.")

    def archive_selection(self):
        indexes = self.tree_sig.selection_indexes()
        if utils.validate_indexes(indexes):
            archived = []
            msg = "Êtes-vous sûr de vouloir archiver {} signalements ?".format(len(indexes))
            if mbox.askokcancel("Archiver sélection", msg, parent=self):
                for i in indexes:
                    sig = self.signalements[i]
                    if "todo" in sig.statut:
                        msg = "{} signalements sur {} ont été archivés car il en reste un non traité :\n{}"
                        mbox.showwarning("Archivage incomplet", msg.format(i, indexes[-1] + 1, sig.sigmdm()),
                                         parent=self)
                        break
                    elif self.archives.archive_sig(sig):
                        archived.append(sig)
                    else:
                        break
                if archived:
                    self.signalements = [sig for sig in self.signalements if sig not in archived]
                    self.refresh(archives=True, scroll="up")
                    self.statusbar.set("{} signalements archivés.".format(len(archived)))
        else:
            msg = ("Votre sélection doit être d'un seul bloc (pas de trous) et doit commencer par le premier " +
                   "signalement afin de conserver l'ordre des archives.")
            mbox.showerror("Mauvais archivage", msg)

    def export_save(self, path=None):
        if path:
            filename = path
        else:
            filename = fdialog.asksaveasfilename(initialdir="saves", initialfile='session', defaultextension='.sig')
        if filename:
            logging.info("Exporting '{}'".format(filename))
            dicts = []
            for i, sig in enumerate(self.signalements):
                d = sig.ordered_dict()
                d.update({"#": i + 1})
                d.move_to_end("#", last=False)
                dicts.append(d)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(json.dumps(dicts, indent=4, ensure_ascii=False))
            self.statusbar.set("{} signalements exportés dans '{}'.".format(len(self.signalements), filename))

    def import_save(self, path=None):
        if path:
            filename = path
        else:
            filename = fdialog.askopenfilename(initialdir="saves",
                                               filetypes=(("Sig Files", "*.sig"), ("All Files", "*.*")))
        if filename:
            logging.info("Importing '{}'".format(filename))
            self.session_path = filename
            with open(filename, "r", encoding="utf-8") as f:
                dicts = json.load(f)
            del self.signalements[:]
            for d in dicts:
                self.signalements.append(signalement.Signalement.from_dict(d))
            self.refresh(archives=True, scroll="down")
            self.statusbar.set("{} signalements importés depuis '{}'.".format(len(self.signalements), filename))

    def search(self):
        self.entry_search.focus()
        self.entry_search.select_range(0, 'end')

    def refresh(self, archives=False, scroll=None):
        logging.debug("Refreshing {} sigs".format(len(self.signalements)))
        self.tree_sig.signalements = self.signalements
        self.tree_sig.refresh()
        if archives:
            self.archives.open()
        self.tree_sig.search()
        if scroll == "down":
            self.tree_sig.scroll_down()
        elif scroll == "up":
            self.tree_sig.scroll_up()

    def clear_focus(self):
        self.tree_sig.deselect_all()
        self.main_frame.focus_force()

    def quit(self):
        logging.info("Exiting RespoTool\n")
        logging.shutdown()
        raise SystemExit


if __name__ == '__main__':
    log_level = utils.init_logging("RespoTool", "respotool.log")
    logging.info("Starting RespoTool {} with log_level={}".format(__version__, log_level))

    msg = ""
    session = "saves/session.sig"
    arch_dir = "archives/"
    arch_pattern = "archives_{0}{0}{0}{0}.txt".format("[0-9]")
    app = RespoTool(session_path=session, archives_dir=arch_dir, archives_pattern=arch_pattern, auto_import=True,
                    warning=False, warning_msg=msg)
    app.mainloop()
