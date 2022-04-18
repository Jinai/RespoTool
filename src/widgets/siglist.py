# -*- coding: utf-8 -*-
# !python3

import datetime
import json
import logging
import webbrowser

import pyperclip

import utils
from signalement import Signalement
from widgets.dialogs.editsigdialog import EditSigDialog
from widgets.popup import Popup
from widgets.treelist import Treelist

logger = logging.getLogger(__name__)


class Siglist(Treelist):
    def __init__(self, master, *, signalements, archives, respomap_widget, statusbar, **kwargs):
        super().__init__(master, **kwargs)
        self.signalements = signalements
        self.respomap_widget = respomap_widget
        self.statusbar = statusbar
        self._keys = [
            lambda x: 0,
            lambda x: x.datetime(),
            lambda x: x.auteur.lower(),
            lambda x: x.code,
            lambda x: x.flag.lower(),
            lambda x: x.desc.lower(),
            lambda x: x.statut.lower(),
            lambda x: str(x.respo)
        ]
        self.archives = archives
        self._last_popup_space = None
        self._last_popup_rightclick = None
        self._dialogs = []
        self.tree.bind("<Double-1>", self.on_doubleclick)
        self.tree.bind("<Button-3>", self.on_rightclick)
        self.tree.bind("<Return>", lambda _: self.edit())
        self.tree.bind("<Control-c>", lambda _: self.copy(with_load=True))
        self.tree.bind("<Control-x>", lambda _: self.copy())
        self.tree.bind("<Control-l>", lambda _: self.open_urls())
        self.tree.bind("<space>", lambda _: self.on_space())
        self.tree.bind("<FocusOut>", lambda _: self.remove_popups())
        self.tree.bind("<<TreeviewSelect>>", lambda _: self.selection_handler())
        self.tree.bind("<<TreelistScroll>>", lambda _: self.remove_popups())
        # self.tree.bind("<<TreelistDelete>>", lambda _: self.delete())
        self.get_tags()
        self.get_templates()
        self.get_statuses()

    def get_tags(self):
        with open(utils.resource_path("data/tags.json"), "r", encoding="utf-8") as f:
            self.tags = json.load(f)
        for tag in self.tags:
            keyword, color = tag
            self.tree.tag_configure(keyword, background=color)

    def get_templates(self):
        with open(utils.resource_path("data/duplicates_msg.json"), "r", encoding="utf-8") as f:
            self.archives_templates = json.load(f)

    def get_statuses(self):
        with open(utils.resource_path("data/statuses.json"), "r", encoding="utf-8") as f:
            self.statuses = json.load(f)

    def insert(self, values, update=True, tags=None):
        tags = []
        for tag in self.tags:
            keyword = tag[0]
            if keyword in values[-2]:
                tags.append(keyword)
                break
        super().insert(values, update, tags)

    def delete(self):
        if self.tree.selection():
            for item in self.tree.selection():
                values = self.tree.item(item)["values"]
                values[0] = str(values[0])  # Treeviews force str to int if it's a digit
                values[-1] = [respo.strip() for respo in values[-1].split(",")] if values[-1] else []
                sig = Signalement(*values[1:])
                self.signalements.remove(sig)
                logger.debug("Deleting {}".format(sig))
            index = super().delete()
            if index == len(self.tree.get_children()):
                index -= 1
            self.refresh()
            if self._search_query.get() != "":
                self.search(debounced=True)
            self.focus_index(index)

    def selection_indexes(self):
        indexes = []
        for item in self.tree.selection():
            indexes.append(int(self.tree.item(item)["values"][0]) - 1)
        return indexes

    def get_selected_sigs(self):
        selected = []
        for item in self.tree.selection():
            index = int(self.tree.item(item)["values"][0]) - 1
            selected.append(self.signalements[index])
        return selected

    def sort(self, col, descending):
        if self.sortable:
            index = self.headers.index(col)
            if index == 0:
                self.signalements.reverse()
            else:
                self.signalements.sort(reverse=descending, key=self._keys[index])
            super().sort(col, descending)

    def on_doubleclick(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            # Clipboard
            item = self.tree.identify("item", event.x, event.y)
            column = int(self.tree.identify("column", event.x, event.y)[1:]) - 1
            value = str(self.tree.item(item)["values"][column])
            pyperclip.copy(value)
            # Popup
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()
            msg = utils.text_ellipsis(value, width=30)
            Popup("'{}' copié dans le presse-papiers".format(msg), x, y, offset=(10, -20))

    def on_rightclick(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            item = self.tree.identify("item", event.x, event.y)
            column = int(self.tree.identify("column", event.x, event.y)[1:]) - 1
            value = str(self.tree.item(item)["values"][column])
            if self.headers[column] == "Code":
                timestamp = int(value[1:11]) + int(value[11:]) / 1000
                value = datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y à %H:%M:%S")
            x, y = self.tree.bbox(item, self.headers[column])[:2]
            x = x + self.winfo_rootx()
            y = y + self.winfo_rooty() - 2
            self.remove_popups()
            self._last_popup_rightclick = Popup(value, x, y, persistent=True, txt_color="#575757",
                                                bg_color="white", border_color="#767676", border_width=1)

    def edit(self):
        selection = self.tree.selection()
        if selection:
            respo = self.respomap_widget.textvariable.get()
            if respo == "":
                self.bell()
                x, y = self.master.winfo_rootx(), self.master.winfo_rooty()
                Popup("Qui es-tu ? ^_^", x, y, offset=(243, 61), delay=50, lifetime=3000)  # Magic offset
                # Pull down the respomap selection menu
                self.respomap_widget.event_generate("<Button-1>")
                return
            item = selection[0]
            item_index = self.tree.get_children().index(item)
            values = self.tree.item(item)["values"]
            values[0] = str(values[0])  # Treeviews force str to int if it's a digit
            data_index = self._data.index(values)
            title = "Signalement #{num} ({auteur})".format(num=values[0], auteur=values[2])
            dialog = EditSigDialog(self, statuses=self.statuses, original_text=values[-2], dialog_title=title)
            self._dialogs.append(dialog)
            dialog.spawn()
            new_statut = dialog.result
            if isinstance(new_statut, str) and new_statut != values[-2]:
                values[-1] = [respo.strip() for respo in values[-1].split(",")] if values[-1] else []
                sig = Signalement(*values[1:])
                sig_index = self.signalements.index(sig)
                if respo not in sig.respo:
                    sig.respo.append(respo)
                if " // " in new_statut and new_statut.split(" // ", 1)[1] == "/reset":
                    sig.respo = []
                else:
                    sig.statut = new_statut
                new_values = list(sig.fields())
                new_values.insert(0, values[0])
                new_values[-1] = ", ".join(new_values[-1])
                self._data[data_index] = new_values
                self.signalements[sig_index] = sig
                self.refresh(keep_search_query=True)
                self.focus_index(item_index)
            else:
                self.focus_item(item)

    def copy(self, with_load=False):
        selection = self.tree.selection()
        if len(selection) == 1:
            item = selection[0]
            cmd = "/load " if with_load else ""
            cmd += self.tree.item(item)["values"][3]
            logger.info("Copying '{}' to the clipboard".format(cmd))
            pyperclip.copy(cmd)
            try:
                x, y = self.tree.bbox(item, "Code")[:2]
                x = x + self.winfo_rootx()
                y = y + self.winfo_rooty()
                Popup("'{}' copié dans le presse-papiers".format(cmd), x, y, offset=(0, -21))
            except ValueError:
                pass

    def open_urls(self):
        for sig in self.get_selected_sigs():
            urls = utils.extract_urls(str(sig))
            if urls:
                logger.info("Opening {} URLs for sig #{}".format(len(urls), self.signalements.index(sig) + 1))
            for url in urls:
                webbrowser.open_new_tab(url)

    def on_space(self):
        selection = self.tree.selection()
        if len(selection) == 1:
            item = selection[0]
            code = self.tree.item(item)["values"][3]
            match_archives = self.archives.filter_sigs("code", [code])
            match_session = self.archives.filter_sigs("code", [code], source=self.signalements)
            if len(match_archives) != 0 or len(match_session) > 1:
                self.remove_popups()
                text = ""
                if len(match_archives) != 0:
                    text += self.archives_templates["archives_msg"]
                    text += "\n    ".join(
                        [""] + [self.archives_templates["archives"].format(**s.__dict__) for s in match_archives])
                if len(match_session) > 1:
                    if text:
                        text += "\n"
                    text += self.archives_templates["session_msg"]
                    text += "\n    ".join(
                        [""] + [self.archives_templates["session"].format(**s.__dict__) for s in match_session])
                self.tree.see(item)
                self.update_idletasks()
                bbox = self.tree.bbox(item, "Code")
                if bbox:
                    x, y = bbox[:2]
                    x = x + self.winfo_rootx()
                    y = y + self.winfo_rooty() + 20
                    self._last_popup_space = Popup(text, x, y, persistent=True, max_alpha=0.90)

    def remove_popups(self):
        if self._last_popup_space:
            self._last_popup_space.fade_out()
            self._last_popup_space = None
        if self._last_popup_rightclick:
            self._last_popup_rightclick.fade_out()
            self._last_popup_rightclick = None

    def selection_handler(self):
        self.remove_popups()
        selection = self.tree.selection()
        if selection:
            plural = "" if len(selection) == 1 else "s"
            self.statusbar.set("{0} signalement{1} sélectionné{1}".format(len(selection), plural), clear_after=0)
        else:
            self.statusbar.clear()

    def close_dialogs(self):
        for dialog in self._dialogs:
            dialog.cancel()
        self.dialogs = []

    def populate(self):
        for i, sig in enumerate(self.signalements):
            f = list(sig.fields())
            f[-1] = ", ".join(f[-1])
            self.insert(f)

    def refresh(self, keep_search_query=False):
        self.close_dialogs()
        if keep_search_query:
            key = self._search_query.get()
            if key != "" and key not in self.search_excludes:
                self.search(debounced=True)
                return
        self.clear()
        self.populate()
        self._matches_label.set("")
