# -*- coding: utf-8 -*-
# !python3

from collections import OrderedDict
from datetime import date


class Signalement():
    TEMPLATE = "{date:<5} {auteur:<12} {code:<14} {flag:<11} {respo:<24} {desc:<100} {statut:<60}"

    def __init__(self, date, auteur, code, flag, desc="", statut="todo", respo=None):
        self.date = date
        self.auteur = auteur
        self.code = code
        self.flag = flag
        self.desc = desc
        self.statut = statut
        self.respo = [] if respo is None else respo

    def fields(self):
        return self.date, self.auteur, self.code, self.flag, self.desc, self.statut, self.respo

    def datetime(self):
        y, m, d = date.today().year, int(self.date.split("/")[1]), int(self.date.split("/")[0])
        return date(y, m, d)

    def archive(self, separator=" | "):
        # Format d'archives
        template = separator.join(Signalement.TEMPLATE.split(" "))
        d = dict(self.__dict__)
        d['respo'] = ", ".join(d['respo'])
        return template.format(**d)

    def sigmdm(self):
        # Format /sigmdm
        return "[{}] {} a signalé {} ({}) : {}".format(self.date, self.auteur, self.code[1:], self.flag, self.desc)

    def ordered_dict(self):
        return OrderedDict(zip(['date', 'auteur', 'code', 'flag', 'desc', 'statut', 'respo'], self.fields()))

    def playlister(self):
        # Format PlayLister de Saki + status
        return "{}  [{}] ({}) : {} [{}]".format(self.code, self.statut.upper(), self.flag, self.desc, self.auteur)

    @staticmethod
    def from_dict(d):
        return Signalement(d['date'], d['auteur'], d['code'], d['flag'], d['desc'], d['statut'], d['respo'])

    def __str__(self):
        return str(self.ordered_dict())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


if __name__ == '__main__':
    import json
    s = Signalement("5/11", "Jinai", "@123456789", "Rally", "faille inf", "modifié", ["Jinai", "Krakas"])
    print("__str__    : " + str(s))
    print("fields     : " + str(s.fields()))
    print("datetime   : " + str(s.datetime()))
    print("archive    : " + s.archive())
    print("sigmdm     : " + s.sigmdm())
    print("playlister : " + s.playlister())
    print()
    print("from dict  : " + Signalement.from_dict(json.loads(json.dumps(s.__dict__))).archive())

