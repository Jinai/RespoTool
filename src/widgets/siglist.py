# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk
import pyperclip
from .treelist import Treelist
from signalement import Signalement
from .popup import Popup


class Siglist(Treelist):
    def __init__(self, master, signalements, *args, **kwargs):
        Treelist.__init__(self, master, *args, **kwargs)
        self.signalements = signalements
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
        self.tree.tag_configure("todo", foreground="red")

    def insert(self, values, update=True, tags=()):
        if "todo" in values[-1]:
            tags = ("todo",)
        super().insert(values, update, tags)

    def delete(self):
        for item in self.tree.selection():
            index = self.tree.get_children().index(item)
            del self.signalements[index]
        super().delete()

    def sort(self, col, descending):
        index = self.headers.index(col)
        self.signalements.sort(reverse=descending, key=self._keys[index])
        super().sort(col, descending)

    def on_doubleclick(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            # Clipboard
            item = self.tree.identify("item", event.x, event.y)
            column = int(self.tree.identify("column", event.x, event.y)[1:]) - 1
            value = self.tree.item(item)['values'][column]
            pyperclip.copy(value)
            # Popup
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()
            msg = value if len(value) <= 20 else value[:20] + "..."
            Popup('"{}" copié dans le presse-papiers'.format(msg), x, y, delay=50, txt_color="white", bg_color="#111111")

    def on_enter(self, event):
        item = self.tree.selection()[0]
        self.place_entry(item)

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

    def place_entry(self, item):
        if self._entry_edit is not None:
            self._entry_edit.destroy()
        x, y, width, height = self.tree.bbox(item, "statut")
        pady = height // 2
        statut = self.tree.item(item)['values'][-1]
        self._entry_edit = ttk.Entry(self.tree, width=17)
        self._entry_edit.place(x=x + width, y=y + pady, anchor="e")
        self._entry_edit.item = item
        self._entry_edit.insert(0, statut)
        self._entry_edit.select_range(0, "end")
        self._entry_edit.bind('<FocusOut>', lambda *x: self.remove_entry())
        self._entry_edit.bind('<Escape>', lambda *x: self.remove_entry())
        self._entry_edit.bind('<Control-a>', lambda *x: self._entry_edit.select_range(0, "end"))
        self._entry_edit.bind('<Return>', lambda *x: self.edit_status())
        self._entry_edit.focus_force()

    def remove_entry(self):
        self.focus_item(self._entry_edit.item)
        self._entry_edit.destroy()

    def edit_status(self):
        item = self._entry_edit.item
        new = self._entry_edit.get()
        self._entry_edit.destroy()
        values = self.tree.item(item)['values']
        values[0] = str(values[0])  # tkinter forces str to int if it's a digit
        index = self._data.index(values)
        values[-1] = new
        self.signalements[index] = Signalement(*values[1:])
        self.refresh()
        self.focus_index(index)

    def populate(self):
        for sig in self.signalements:
            self.insert(sig.fields())

    def refresh(self):
        self.clear()
        self.populate()


if __name__ == '__main__':
    import signalement

    root = tk.Tk()
    headers = ['date', 'auteur', 'code', 'flag', 'description', 'statut']
    column_widths = [30, 40, 85, 100, 80, 350, 105]
    sigs = [
        signalement.Signalement("5/11", "Jinai", "@123456789", "Rally", "faille inf"),
        signalement.Signalement("6/11", "Shodaboy", "@987654321", "Défilante", "Impossible"),
        signalement.Signalement("7/11", "Jinai", "@123456789", "Rally", "faille inf", "corrigé"),
        signalement.Signalement("8/11", "Shodaboy", "@987654321", "Défilante", "Impossible", "supprimé"),
    ]
    tree = Siglist(root, sigs, headers, column_widths)
    tree.pack(fill='both', expand=True)
    for s in sigs:
        tree.insert(s.fields())
    root.mainloop()
