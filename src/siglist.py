# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk
import pyperclip
from treelist import Treelist
from signalement import Signalement
from popup import Popup

STATUS = [
    "ignoré",
    "corrigé",
    "supprimé",
    "reset",
    "reclassé",
    "mappeur contacté",
]


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
        # Bindings
        self.tree.bind('<Double-1>', self.on_doubleclick)
        self.tree.bind('<Return>', self.on_enter)
        # Tags
        self.tree.tag_configure("todo", foreground="red")

    def insert(self, values, update=True, tags=()):
        if "todo" in values[-1]:
            tags = ("todo",)
        super().insert(values, update, tags)

    def delete(self):
        for item in self.tree.selection():
            self.signalements.remove(Signalement(*self.tree.item(item)['values'][1:]))
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
            Popup('"{}" copié dans le presse-papiers'.format(msg), x, y)

    def on_enter(self, event):
        item = self.tree.selection()[0]
        self.place_entry(item)

    def place_entry(self, item):
        if self._entry_edit is not None:
            self._entry_edit.destroy()
        x, y, width, height = self.tree.bbox(item, "statut")
        pady = height // 2
        self._entry_edit = ttk.Entry(self.tree, width=17)
        self._entry_edit.place(x=x + width, y=y + pady, anchor="e")
        self._entry_edit.item = item
        self._entry_edit.bind('<Escape>', lambda *x: self._entry_edit.destroy())
        self._entry_edit.bind('<Control-a>', lambda *x: self._entry_edit.select_range(0, "end"))
        self._entry_edit.bind('<Return>', lambda event: self.edit_status(event, item))
        self._entry_edit.focus_force()

    def edit_status(self, event, item):
        new = event.widget.get()
        values = self.tree.item(self._entry_edit.item)['values']
        values[0] = str(values[0])
        data_index = self._data.index(values)
        sig_index = self.signalements.index(Signalement(*values[1:]))
        values[-1] = new
        self._data[data_index] = values
        self.signalements[sig_index] = Signalement(*values[1:])
        self._entry_edit.destroy()
        item_index = self.tree.get_children().index(item)
        self.refresh()
        self.selection(item_index)

    def selection(self, index):
        self.tree.selection_set(self.tree.get_children()[index])

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
