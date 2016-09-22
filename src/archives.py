# -*- coding: utf-8 -*-
# !python3

from signalement import Signalement

ARCHIVES_PATH = "archives/archives.txt"


class Archives():
    def __init__(self, path):
        self.path = path
        self.raw_text = ''
        self.signalements = []
        self.read_archives()

    @staticmethod
    def parse(text, line_sep='\n', col_sep='|'):
        signalements = []
        if not isinstance(text, str):
            return signalements
        for line in text.split(line_sep):
            if line.strip() != '':
                values = [elem.strip() for elem in line.split(col_sep)]
                values[4] = [respo.strip() for respo in values[4].split(',')] if values[4] else []
                respo = values.pop(4)
                values.append(respo)
                s = Signalement(*values)
                signalements.append(s)
        return signalements

    def read_archives(self):
        try:
            f = open(self.path, 'r', encoding='utf-8')
        except IOError:
            pass
        else:
            try:
                self.raw_text = ''.join(f.readlines()[2:])
                self.signalements = Archives.parse(self.raw_text)
            except (IOError, IndexError):
                pass
            finally:
                f.close()

    def get_sigs(self, key, *values, exact=False, func=None, source=None):
        s = []
        if source is None:
            source = self
        for sig in source:
            for value in values:
                if func:
                    if func(sig.__dict__[key], value):
                        s.append(sig)
                        break
                elif sig.__dict__[key] == value or (not exact and value in sig.__dict__[key]):
                    s.append(sig)
                    break
        return s

    def __len__(self):
        return len(self.signalements)

    def __iter__(self):
        return iter(self.signalements)
