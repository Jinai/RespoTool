# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk


class Treelist(tk.Frame):
    def __init__(self, master, headers, column_widths=None, height=15, alt_colors=None, sort_keys=None, stretch=None,
                 sortable=True, auto_increment=True, search_excludes=None, match_template=None, **opts):
        tk.Frame.__init__(self, master, **opts)
        self.master = master
        self.headers = headers
        self.auto_increment = auto_increment  # Allows automatic handling of # column
        if auto_increment:
            self.headers.insert(0, "#")
            self.column_widths = column_widths if column_widths else [30] + [90] * (len(headers) - 1)
            self.sort_keys = sort_keys if sort_keys else [lambda x: int(x[0])] + [lambda x: str(x[0]).lower()] * (
                    len(headers) - 1)
        else:
            self.column_widths = column_widths if column_widths else [90] * len(headers)
            self.sort_keys = sort_keys if sort_keys else [[lambda x: str(x[0]).lower()] * len(headers)]
        self.height = height
        self.alt_colors = alt_colors if alt_colors else ["white", "grey96"]

        # List of booleans telling which column are stretchable
        self.stretch = stretch if stretch else [False] * (len(headers) - 2) + [True]

        # Allows clicking on headers to sort columns alphabetically
        self.sortable = sortable

        # A list of words to ignore when search() is triggered
        self.search_exludes = search_excludes if search_excludes else []

        # A formatted string that can be used to display the number of matches yielded by a search query
        self.match_template = match_template if match_template else "{}/{}"

        # Internal variables
        self._search_key = tk.StringVar()  # Contains the search query
        self._search_key.trace("w", lambda *x: self.search())  # Everytime the query changes it triggers search()
        self._matches_label = tk.StringVar()  # Contains the number of matches (formatted) yielded by the search query
        self._data = []  # Contains inserted values
        self._parity_check = 0  # For alt colors, incremented every insertion and resetted when the tree is cleared

        self._setup_widgets()

    def _setup_widgets(self):
        frame_tree = tk.Frame(self)
        frame_tree.pack(fill='both', expand=True)
        vsb = ttk.Scrollbar(frame_tree, orient="vertical")
        vsb.pack(side='right', fill='y')
        # hsb = ttk.Scrollbar(frame_tree, orient="horizontal")
        # hsb.pack(side='bottom', fill='x')
        self.tree = ttk.Treeview(frame_tree, columns=self.headers, displaycolumns=self.headers, show="headings",
                                 height=self.height, selectmode="extended")
        self.tree.pack(side='top', fill='both', expand=True)
        self.tree.configure(yscrollcommand=vsb.set)  # , xscrollcommand=hsb.set)
        vsb.configure(command=self.tree.yview)
        # hsb.configure(command=self.tree.xview)
        # Tags
        self.tree.tag_configure("even_row", background=self.alt_colors[0])
        self.tree.tag_configure("odd_row", background=self.alt_colors[1])
        # Bindings
        self.tree.bind('<BackSpace>', lambda _: self.delete())
        self.tree.bind('<Delete>', lambda _: self.delete())
        self.tree.bind('<Control-a>', lambda _: self.select_all())

        self._build_tree()

    def _build_tree(self):
        for i, header in enumerate(self.headers):
            self.tree.heading(header, text=header.title(), anchor="w", command=lambda h=header: self.sort(h, True))
            self.tree.column(self.headers[i], width=self.column_widths[i], stretch=self.stretch[i])

    def insert(self, values, update=True, tags=None):
        values = list(values)
        tags = tags if tags else []
        if self.auto_increment and update:
            values.insert(0, str(len(self._data) + 1))
        if not tags:
            tags.append(["even_row", "odd_row"][self._parity_check % 2])
        self.tree.insert('', 'end', values=values, tags=tags)
        self._parity_check += 1
        if update:
            self._data.append(values)

    def delete(self):
        selection = self.tree.selection()
        index = 0
        for item in selection:
            if item == selection[-1]:
                index = self.tree.get_children().index(item)
            values = self.tree.item(item)['values']
            values[0] = str(values[0])
            self._data.remove(values)
            self.tree.delete(item)
        return index

    def clear(self, keep_data=False):
        self._parity_check = 0
        self.tree.delete(*self.tree.get_children())
        if not keep_data:
            del self._data[:]

    def scroll_up(self, event=None):
        self.update()
        self.tree.yview_moveto(0)

    def scroll_down(self, event=None):
        self.update()
        self.tree.yview_moveto(1)

    def focus_index(self, index):
        if index < len(self.tree.get_children()):
            item = self.tree.get_children()[index]
            self.focus_item(item)

    def focus_item(self, item):
        self.tree.selection_set(item)
        self.tree.focus_set()
        self.tree.focus(item)

    def selection_indexes(self):
        indexes = []
        selection = self.tree.selection()
        for item in selection:
            values = self.tree.item(item)['values']
            values[0] = str(values[0])
            indexes.append(self._data.index(values))
        return indexes

    def sort(self, col, descending):
        if self.sortable:
            tree_data = [(self.tree.set(child, col), self.tree.set(child, 0), child) for child in
                         self.tree.get_children('')]
            index = self.headers.index(col)
            tree_data.sort(reverse=descending, key=lambda x: (self.sort_keys[index](x), int(x[1])))
            self._data.sort(reverse=descending, key=lambda x: (self.sort_keys[index]([x[index]]), int(x[0])))
            for index, item in enumerate(tree_data):
                self.tree.move(item[2], '', index)
            # Switch heading command to reverse the sort next time
            self.tree.heading(col, command=lambda col=col: self.sort(col, not descending))
            # In case the user is in the middle of a search
            self.search()

    def search(self, key=None):
        key = key if key is not None else self._search_key.get()
        if key in self.search_exludes:
            return
        self.clear(keep_data=True)
        matches = 0
        for values in self._data:
            for item in values:
                if key.lower() in str(item).lower():
                    self.insert(values, update=False)
                    matches += 1
                    break
        self._matches_label.set(self.match_template.format(matches, len(self._data)))

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())
