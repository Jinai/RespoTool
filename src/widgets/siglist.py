# -*- coding: utf-8 -*-
# !python3

import json
import logging
import webbrowser
import winsound

import pyperclip

import utils
from signalement import Signalement
from widgets.editstatus import EditStatusDialog
from widgets.popup import Popup
from widgets.treelist import Treelist

logger = logging.getLogger(__name__)


class Siglist(Treelist):
    def __init__(self, master, signalements, respomap, archives, *args, **kwargs):
        Treelist.__init__(self, master, *args, **kwargs)
        self.signalements = signalements
        self.respomap = respomap
        self._keys = {
            0: lambda x: 0,
            1: lambda x: x.datetime(),
            2: lambda x: x.auteur.lower(),
            3: lambda x: x.code,
            4: lambda x: x.flag.lower(),
            5: lambda x: x.desc.lower(),
            6: lambda x: x.statut.lower(),
            7: lambda x: str(x.respo)
        }
        self._entry_edit = None
        self.archives = archives
        self.last_popup_space = None
        self.last_popup_rightclick = None
        self.tree.bind('<Double-1>', self.on_doubleclick)
        self.tree.bind('<Button-3>', self.on_rightclick)
        self.tree.bind('<Return>', self.on_enter)
        self.tree.bind('<Control-c>', lambda _: self.copy(with_load=True))
        self.tree.bind('<Control-x>', lambda _: self.copy())
        self.tree.bind('<Control-l>', lambda _: self.open_urls())
        self.tree.bind('<space>', self.on_space)
        self.tree.bind('<FocusOut>', self.remove_popups)
        self.tree.bind('<<TreeviewSelect>>', self.remove_popups)
        self.update_tags()
        self.update_templates()

    def update_tags(self):
        with open("data/tags.json", 'r', encoding='utf-8') as f:
            self.tags = json.load(f)
        for index in self.tags:
            for keyword in self.tags[index]:
                self.tree.tag_configure(keyword, background=self.tags[index][keyword])

    def update_templates(self):
        with open("data/duplicates_msg.json", 'r', encoding='utf-8') as f:
            self.archives_templates = json.load(f)

    def insert(self, values, update=True, tags=None):
        tags = []
        try:
            for index in sorted(self.tags):
                for keyword in self.tags[index]:
                    if keyword in values[-2]:
                        tags.append(keyword)
                        raise StopIteration
        except StopIteration:
            pass
        super().insert(values, update, tags)

    def delete(self):
        if self.tree.selection():
            for item in self.tree.selection():
                values = self.tree.item(item)['values']
                values[0] = str(values[0])  # Treeviews force str to int if it's a digit
                values[-1] = [respo.strip() for respo in values[-1].split(",")] if values[-1] else []
                sig = Signalement(*values[1:])
                self.signalements.remove(sig)
                logger.debug("Deleting {}".format(sig))
            index = super().delete()
            self.refresh()
            if self._search_key.get() != '':
                self.search()
            self.focus_index(index)

    def selection_indexes(self):
        indexes = []
        for item in self.tree.selection():
            indexes.append(int(self.tree.item(item)['values'][0]) - 1)
        return indexes

    def get_selected_sigs(self):
        selected = []
        for item in self.tree.selection():
            index = int(self.tree.item(item)['values'][0]) - 1
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

    def search(self, key=None):
        key = key.strip() if key is not None else self._search_key.get().strip()
        if key == '':
            self.refresh()
        else:
            super().search(key)

    def on_doubleclick(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            # Clipboard
            item = self.tree.identify("item", event.x, event.y)
            column = int(self.tree.identify("column", event.x, event.y)[1:]) - 1
            value = str(self.tree.item(item)['values'][column])
            pyperclip.copy(value)
            # Popup
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()
            msg = utils.ellipsis(value, width=30)
            Popup('"{}" copié dans le presse-papiers'.format(msg), x, y, offset=(10, -20))

    def on_rightclick(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            item = self.tree.identify("item", event.x, event.y)
            column = int(self.tree.identify("column", event.x, event.y)[1:]) - 1
            value = str(self.tree.item(item)['values'][column])
            x, y = self.tree.bbox(item, self.headers[column])[:2]
            x = x + self.winfo_rootx()
            y = y + self.winfo_rooty() - 2
            self.remove_popups()
            self.last_popup_rightclick = Popup(value, x, y, persistent=True, txt_color="#575757",
                                               bg_color="white", border_color="#767676", border_width=1)

    def on_enter(self, event):
        selection = self.tree.selection()
        if selection:
            if self.respomap.get() == '':
                winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
                x, y = self.master.winfo_rootx(), self.master.winfo_rooty()
                Popup("Qui es-tu ? ^_^", x, y, offset=(220, 61), delay=50, lifetime=3000)
                # Pull down the respomap selection menu [dirty]
                self.master.master.dropdown_respo.event_generate("<Button-1>")
                return
            item = selection[0]
            item_index = self.tree.get_children().index(item)
            values = self.tree.item(item)['values']
            values[0] = str(values[0])  # Treeviews force str to int if it's a digit
            data_index = self._data.index(values)
            dialog = EditStatusDialog(self, "Éditer statut #{} : {}".format(values[0], values[3]), values[-2])
            dialog.spawn()
            new_statut = dialog.result
            if new_statut is not None and new_statut != values[-2]:
                values[-1] = [respo.strip() for respo in values[-1].split(",")] if values[-1] else []
                sig = Signalement(*values[1:])
                sig_index = self.signalements.index(sig)
                respo = self.respomap.get()
                if respo != '' and respo not in sig.respo:
                    sig.respo.append(respo)
                if "/reset" in new_statut.lower():
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
            cmd += self.tree.item(item)['values'][3]
            pyperclip.copy(cmd)
            try:
                x, y = self.tree.bbox(item, "code")[:2]
                x = x + self.winfo_rootx()
                y = y + self.winfo_rooty()
                Popup('"{}" copié dans le presse-papiers'.format(cmd), x, y, offset=(0, -21))
            except ValueError:
                pass

    def open_urls(self):
        for sig in self.get_selected_sigs():
            for url in utils.extract_urls(str(sig)):
                webbrowser.open_new_tab(url)

    def on_space(self, event):
        selection = self.tree.selection()
        if len(selection) == 1:
            item = selection[0]
            code = self.tree.item(item)['values'][3]
            match_archives = self.archives.filter_sigs("code", [code])
            match_session = self.archives.filter_sigs("code", [code], source=self.signalements)
            if len(match_archives) != 0 or len(match_session) > 1:
                self.remove_popups()
                text = ""
                if len(match_archives) != 0:
                    text += self.archives_templates["archives_msg"]
                    text += "\n    ".join(
                        [''] + [self.archives_templates["archives"].format(**s.__dict__) for s in match_archives])
                if len(match_session) > 1:
                    if text:
                        text += "\n"
                    text += self.archives_templates["session_msg"]
                    text += "\n    ".join(
                        [''] + [self.archives_templates["session"].format(**s.__dict__) for s in match_session])
                x, y = self.tree.bbox(item, "code")[:2]
                x = x + self.winfo_rootx()
                y = y + self.winfo_rooty() + 20
                self.last_popup_space = Popup(text, x, y, persistent=True, max_alpha=0.90)

    def remove_popups(self, event=None):
        if self.last_popup_space:
            self.last_popup_space.destroy()
        if self.last_popup_rightclick:
            self.last_popup_rightclick.destroy()

    def populate(self):
        for i, sig in enumerate(self.signalements):
            f = list(sig.fields())
            f[-1] = ", ".join(f[-1])
            self.insert(f)

    def refresh(self, keep_search_query=False):
        if keep_search_query:
            key = self._search_key.get().strip()
            if key != '' and key not in self.search_exludes:
                self.search()
                return
        self.clear()
        self.populate()
        self.update_tags()
        self.update_templates()
        self._matches_label.set('')
