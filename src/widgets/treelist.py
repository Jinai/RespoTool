# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk


class Treelist(tk.Frame):
    def __init__(self, master, headers, column_widths=None, height=15, alt_colors=None, sort_keys=None, stretch=None,
                 **opts):
        tk.Frame.__init__(self, master, **opts)
        self.master = master
        self.headers = ["#"]
        self.headers.extend(headers)
        self.column_widths = column_widths if column_widths else [30] + [90] * len(headers)
        self.height = height
        self.alt_colors = alt_colors if alt_colors else ["white", "grey97"]
        if sort_keys:  # List of functions used to sort columns
            self.sort_keys = sort_keys
        else:
            self.sort_keys = [lambda x: int(x[0])] + [lambda x: str(x[0]).lower()] * (len(headers))
        # List of booleans telling which column are stretchable
        self.stretch = stretch if stretch else [False] * len(headers) + [True]
        # Internal variables
        self._search_key = tk.StringVar()
        self._search_key.trace("w", lambda _, __, ___: self.search())
        self._data = []
        self._item_count = 0

        self._setup_widgets()

    def _setup_widgets(self):
        frame_tree = tk.Frame(self)
        frame_tree.pack(fill='both', expand=True)
        vsb = ttk.Scrollbar(frame_tree, orient="vertical")
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(frame_tree, orient="horizontal")
        hsb.pack(side='bottom', fill='x')
        self.tree = ttk.Treeview(frame_tree, columns=self.headers, displaycolumns=self.headers, show="headings",
                                 height=self.height, selectmode="extended")
        self.tree.pack(side='top', fill='both', expand=True)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.configure(command=self.tree.yview)
        hsb.configure(command=self.tree.xview)
        # Tags
        self.tree.tag_configure("odd_row", background=self.alt_colors[0])
        self.tree.tag_configure("even_row", background=self.alt_colors[1])
        # Bindings
        self.tree.bind('<BackSpace>', lambda _: self.delete())
        self.tree.bind('<Delete>', lambda _: self.delete())
        self.tree.bind('<Control-a>', lambda _: self.select_all())

        self._build_tree()

    def _build_tree(self):
        for i, header in enumerate(self.headers):
            self.tree.heading(header, text=header.title(), anchor="w", command=lambda h=header: self.sort(h, False))
            self.tree.column(self.headers[i], width=self.column_widths[i], stretch=self.stretch[i])

    def insert(self, values, update=True, tags=()):
        self._item_count += 1
        values = list(values)
        values.insert(0, str(self._item_count))
        t = [["even_row", "odd_row"][self._item_count % 2]]
        t.extend(tags)
        self.tree.insert('', 'end', values=values, tags=t)
        if update:
            self._data.append(values)

    def delete(self):
        for item in self.tree.selection():
            values = self.tree.item(item)['values']
            values[0] = str(values[0])
            self._data.remove(values)
            self.tree.delete(item)
            self._item_count -= 1

    def clear(self, keep_data=False):
        self.tree.delete(*self.tree.get_children())
        self._item_count = 0
        if not keep_data:
            del self._data[:]

    def sort(self, col, descending):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        index = self.headers.index(col)
        data.sort(reverse=descending, key=self.sort_keys[index])
        self._data.sort(reverse=descending, key=lambda x: (self.sort_keys[index]([x[index]]), int(x[0])))
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        # Switch heading command to reverse the sort next time
        self.tree.heading(col, command=lambda col=col: self.sort(col, not descending))
        # Hack to refresh the tree with an empty search to get the alternate colors right
        self.search()

    def search(self, key=None):
        key = key if key else self._search_key.get()
        self.clear(keep_data=True)
        for values in self._data:
            for item in values:
                if key.lower() in str(item).lower():
                    self.insert(values[1:], update=False)
                    break

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())
