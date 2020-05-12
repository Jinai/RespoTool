# -*- coding: utf-8 -*-
# !python3

import tkinter as tk
import tkinter.ttk as ttk


class Treelist(ttk.Frame):
    def __init__(self, master, headers, column_widths=None, height=15, alt_colors=None, sortable=True, sort_keys=None,
                 stretch_bools=None, index_options=None, debounce_time=300, search_excludes=None, match_template=None,
                 scroll_speed=3, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.master = master
        self.headers = headers
        self.column_widths = column_widths if column_widths else [90] * (len(headers))
        self.height = height

        # x[0] == cell value ; x[1] == list of all values of the row (can be used to compare against index)
        self.sort_keys = sort_keys if sort_keys else [lambda x: str(x[0]).lower()] * (len(headers))
        # List of booleans telling which columns are stretchable
        self.stretch_bools = stretch_bools if stretch_bools else [False] * (len(headers) - 1) + [True]

        # Options for the special column showing row index (starting at 1)
        index_options = index_options if index_options else {}
        self.index_show = index_options.get("show", True)
        self.index_header = index_options.get("header", "#")
        self.index_width = index_options.get("width", 30)
        self.index_sort = index_options.get("sort", lambda x: int(x[0]))
        self.index_stretch = index_options.get("stretch", False)
        self.headers.insert(0, self.index_header)
        self.column_widths.insert(0, self.index_width)
        self.sort_keys.insert(0, self.index_sort)
        self.stretch_bools.insert(0, self.index_stretch)

        # Configure colors for even/odd rows
        alt_colors = alt_colors if alt_colors else {}
        even_row = alt_colors.get("even", "grey98")  # ttk.Style().lookup("TFrame", "background")
        odd_row = alt_colors.get("odd", "grey93")
        self.alt_colors = [even_row, odd_row]

        # Allows clicking on headers to sort columns according to `sort_keys`
        self.sortable = sortable

        # In milliseconds. Delays calls to search() until the user has finished typing his query
        # Use debounce_time <= 0 for instant feedback
        self.debounce_time = debounce_time

        # A list of words to ignore when search() is triggered
        self.search_excludes = search_excludes if search_excludes else []

        # A formatted string that can be used to display the number of matches yielded by a search query
        self.match_template = match_template if match_template else "{}/{}"

        # Number of lines to scroll when using the mouse wheel. Internally, a scroll speed of N is represented as N-1
        self.scroll_speed = max(scroll_speed - 1, 0)

        # Internal variables
        self._search_query = tk.StringVar()
        self._search_query.trace("w", lambda *x: self.search())
        self._last_search_query = ""
        self._matches_label = tk.StringVar()  # Contains the number of matches (formatted) yielded by the search query
        self._debounce_after_id = None
        self._data = []  # Contains inserted values
        self._row_count = 0  # Used for colored odd rows

        self._setup_widgets()

    def _setup_widgets(self):
        frame_tree = ttk.Frame(self)
        frame_tree.pack(fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbar.pack(side='right', fill='y')

        display = self.headers if self.index_show else self.headers[1:]
        self.tree = ttk.Treeview(frame_tree, columns=self.headers, displaycolumns=display, show="headings",
                                 height=self.height, selectmode="extended")
        self.tree.pack(side='top', fill='both', expand=True)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tree.yview)

        # Tags
        self.tree.tag_configure("even_row", background=self.alt_colors[0])
        self.tree.tag_configure("odd_row", background=self.alt_colors[1])

        # Bindings
        self.tree.event_add("<<TreelistDelete>>", "<BackSpace>", "<Delete>")
        self.tree.bind("<Control-a>", lambda _: self.select_all())
        self.tree.bind("<MouseWheel>", self.mousewheel_handler)

        self._build_tree()

    def _build_tree(self):
        for i, header in enumerate(self.headers):
            self.tree.heading(header, text=header, anchor="w", command=lambda h=header: self.sort(h, True))
            self.tree.column(self.headers[i], width=self.column_widths[i], stretch=self.stretch_bools[i])

    def insert(self, values, update=True, tags=None):
        self._row_count += 1
        values = list(values)
        tags = tags if tags else []
        if update:
            values.insert(0, str(self._row_count))
            self._data.append(values)
        if not tags:
            tags.append(["even_row", "odd_row"][self._row_count % 2])
        self.tree.insert('', 'end', values=values, tags=tags)

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
            self._row_count -= 1
        return index

    def clear(self, keep_data=False):
        self._row_count = 0
        self.tree.delete(*self.tree.get_children())
        if not keep_data:
            del self._data[:]

    def scroll_up(self):
        self.update()
        self.tree.yview_moveto(0)

    def scroll_down(self):
        self.update()
        self.tree.yview_moveto(1)

    def focus_index(self, index):
        rows = self.tree.get_children()
        if 0 <= index < len(rows):
            item = rows[index]
            self.focus_item(item)

    def focus_item(self, item):
        try:
            self.focus_force()
            self.tree.selection_set((item,))
            self.tree.focus_set()
            self.tree.focus(item)
        except tk.TclError:
            pass

    def sort(self, col, descending):
        if self.sortable:
            tree_data = [(self.tree.set(child, col), self.tree.set(child, 0), child) for child in
                         self.tree.get_children('')]
            index = self.headers.index(col)
            tree_data.sort(reverse=descending, key=lambda x: (self.sort_keys[index](x), int(x[1])))
            self._data.sort(reverse=descending, key=lambda x: (self.sort_keys[index]([x[index]]), int(x[0])))
            for index, item in enumerate(tree_data):
                self.tree.move(item[2], '', index)
                self.tree.item(item[2], tags=[["even_row", "odd_row"][(index + 1) % 2]])
            # Switch heading command to reverse the sort next time
            self.tree.heading(col, command=lambda col=col: self.sort(col, not descending))
            # In case the user is in the middle of a search
            self.search()

    def search(self, query=None, debounced=False):
        if self.debounce_time > 0 and not debounced:
            id = self._debounce_after_id
            self._debounce_after_id = None
            if id:
                self.after_cancel(id)
            self._debounce_after_id = self.after(self.debounce_time, lambda: self.search(query, debounced=True))
            return

        query = query if query is not None else self._search_query.get()
        if query in self.search_excludes:
            query = ""

        if query == "" and self._last_search_query == "":
            return

        self.clear(keep_data=True)
        if query == "":
            for values in self._data:
                self.insert(values, update=False)
            self._matches_label.set('')
        else:
            matches = 0
            for values in self._data:
                for item in values:
                    if query.lower() in str(item).lower():
                        self.insert(values, update=False)
                        matches += 1
                        break
            self._matches_label.set(self.match_template.format(matches, len(self._data)))
        self._last_search_query = query
        self.scroll_up()

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def deselect_all(self):
        self.tree.selection_remove(self.tree.get_children())

    def mousewheel_handler(self, event):
        direction = 1
        if event.delta > 0:
            direction = -1
        self.tree.yview_scroll(self.scroll_speed * direction, "units")
