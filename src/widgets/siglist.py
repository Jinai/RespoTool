# -*- coding: utf-8 -*-
# !python3

import json
import winsound

import pyperclip
from .treelist import Treelist
from signalement import Signalement
from .popup import Popup
from .editstatus import EditStatusDialog
from signalement import Signalement


class Siglist(Treelist):
    def __init__(self, master, signalements, respomap, *args, **kwargs):
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
        }
        self._entry_edit = None
        self.tree.bind('<Double-1>', self.on_doubleclick)
        self.tree.bind('<Return>', self.on_enter)
        self.tree.bind('<Control-c>', self.copy)
        self.tree.tag_configure("todo", foreground="red2")

    def insert(self, values, update=True, tags=()):
        if "todo" in values[-1]:
            tags = ("todo",)
        super().insert(values, update, tags)

    def delete(self):
        for item in reversed(self.tree.selection()):  # reversed to avoid index errors
            index = self.tree.get_children().index(item)
            del self.signalements[index]
        super().delete()
        self.refresh()

    def sort(self, col, descending):
        if self.sortable:
            index = self.headers.index(col)
            self.signalements.sort(reverse=descending, key=self._keys[index])
            super().sort(col, descending)

    def on_doubleclick(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            # Clipboard
            item = self.tree.identify("item", event.x, event.y)
            column = int(self.tree.identify("column", event.x, event.y)[1:]) - 1
            value = str(self.tree.item(item)['values'][column])
            pyperclip.copy(value)
            # Popup
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()
            msg = value if len(value) <= 20 else value[:20] + "..."
            Popup('"{}" copié dans le presse-papiers'.format(msg), x, y, delay=50, txt_color="white", bg_color="#111111")

    def on_enter(self, event):
        select = self.tree.selection()
        if select:
            if self.respomap.get() == '':
                winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
                x, y = self.master.winfo_rootx(), self.master.winfo_rooty()
                Popup("<- Qui es-tu ? ^_^", x, y, offset=(220, 61), delay=50, txt_color='white', bg_color='#111111')
                return
            item = select[0]
            values = self.tree.item(item)['values']
            dialog = EditStatusDialog(self, "Éditer statut #{} : {}".format(values[0], values[3]), values[-1])
            new_statut = dialog.result
            if new_statut is not None:
                values[0] = str(values[0])  # tkinter forces str to int if it's a digit
                index = self._data.index(values)
                values[-1] = new_statut
                self.signalements[index] = Signalement(*values[1:])
                self.refresh()
                self.focus_index(index)
            else:
                self.focus_item(item)

    def copy(self, event):
        selection = self.tree.selection()
        if len(selection) == 1:
            item = selection[0]
            load = "/load "
            load += self.tree.item(item)['values'][3]
            pyperclip.copy(load)
            try:
                x, y, width, height = self.tree.bbox(item, "code")
                x = x + self.master.master.winfo_x() + 5
                y = y + self.master.master.winfo_y() + 96
                Popup('"{}" copié dans le presse-papiers'.format(load), x, y, delay=50, txt_color="white", bg_color="#111111")
            except ValueError:
                pass

    def populate(self):
        for i, sig in enumerate(self.signalements):
            f = list(sig.fields())
            f[-1] = ", ".join(f[-1])
            self.insert(f)

    def refresh(self):
        self.clear()
        self.populate()
