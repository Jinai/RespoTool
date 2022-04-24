# -*- coding: utf-8 -*-
# !python3

import re


class Tag:
    def __init__(self, index, label, label_span=None, content=None):
        self.index = index
        self.label = label
        self.label_span = label_span
        self.content = content

    def __eq__(self, other):
        return self.label_span == other.label_span

    def __lt__(self, other):
        return self.label_span < other.label_span

    def __repr__(self):
        return f"<Tag index='{self.index}' label='{self.label}', label_span='{self.label_span}', content='{self.content}'>"


class SearchParser:
    def __init__(self, tags):
        self.tags = dict.fromkeys(tags)

    def parse(self, query):
        tags = []
        for index, tag in enumerate(self.tags):
            for match in re.finditer(f"(?i) ?{tag}:", query):
                t = Tag(index, tag, label_span=match.span())
                tags.append(t)
        if tags:
            tags.sort()
            for index, tag in enumerate(tags):
                if index < len(tags) - 1:
                    start = tag.label_span[1]
                    end = tags[index + 1].label_span[0]
                    tag.content = query[start:end]
            tags[-1].content = query[tags[-1].label_span[1]:]

            t = Tag(-1, "_notag")
            t.content = query[:tags[0].label_span[0]]
            tags.insert(0, t)
            return tags
        else:
            return [Tag(-1, "_notag", content=query)]
