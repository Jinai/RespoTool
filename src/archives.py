# -*- coding: utf-8 -*-
# !python3

import os
import glob
import datetime

from signalement import Signalement

ARCHIVES_DIR = "archives/"


class Archives():
    read_counter = 0
    write_counter = 0

    def __init__(self, dir_path, pattern):
        self.dir_path = dir_path
        self.pattern = pattern
        self.raw_text = ''
        self.signalements = []
        self.files = glob.glob(os.path.join(dir_path, pattern))
        self.open()

    def open(self):
        self.raw_text = ''
        opened = False
        for file in self.files:
            try:
                f = open(file, 'r', encoding='utf-8')
            except IOError as e:
                print(e)
            else:
                try:
                    self.raw_text += ''.join(f.readlines()[2:])
                    Archives.read_counter += 1
                    opened = True
                except (IOError, IndexError) as e:
                    print(e)
                finally:
                    f.close()
        self.signalements = Archives.parse(self.raw_text)
        return opened


        try:
        except IOError:
            pass
        else:
            try:
                pass
            finally:
                f.close()
    def current_file(self):
        if self.files:
            return self.files[-1]
        return None

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
