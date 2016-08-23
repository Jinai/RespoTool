# -*- coding: utf-8 -*-
# !python3

import json
from collections import OrderedDict
from datetime import date


class Signalement():
    TEMPLATE = "{date:<5} {auteur:<12} {code:<14} {flag:<11} {desc:<100} {statut:<10}"

    def __init__(self, date, auteur, code, flag, desc="", statut="todo"):
        self.date = date
        self.auteur = auteur
        self.code = code
        self.flag = flag
        self.desc = desc
        self.statut = statut

    def fields(self):
        return self.date, self.auteur, self.code, self.flag, self.desc, self.statut

    def datetime(self):
        y, m, d = date.today().year, int(self.date.split("/")[1]), int(self.date.split("/")[0])
        return date(y, m, d)

    def archive(self, separator=" | "):
        # Format d'archives
        template = separator.join(Signalement.TEMPLATE.split(" "))
        return template.format(**self.__dict__)

    def sigmdm(self):
        # Format /sigmdm
        return "[{}] {} a signalé {} ({}) : {}".format(self.date, self.auteur, self.code[1:], self.flag, self.desc)

    def ordered_dict(self):
        return OrderedDict(zip(['date', 'auteur', 'code', 'flag', 'desc', 'statut'], self.fields()))

    @staticmethod
    def from_dict(d):
        return Signalement(d['date'], d['auteur'], d['code'], d['flag'], d['desc'], d['statut'])

    def __str__(self):
        # Format PlayLister + status
        return "{}  [{}] ({}) : {} [{}]".format(self.code, self.statut.upper(), self.flag, self.desc, self.auteur)

    def __eq__(self, other):
        return self.code == other.code


if __name__ == '__main__':
    print(Signalement("5/11", "Jinai", "123456789", "Rally", "faille inf"))
    print(Signalement("5/11", "Jinai", "123456789", "Rally", "faille inf", "corrigé"))
    print(Signalement("5/11", "Jinai", "123456789", "Rally", "faille inf").format())
    print(Signalement("5/11", "Jinai", "123456789", "Rally", "faille inf", "corrigé").format())
