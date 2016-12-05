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

    def archive_sig(self, sig):
        if not self.files:
            self.new_archive(os.path.join(self.dir_path, "archives_{}.txt".format(sig.datetime().year)))
        if self.signalements and sig.datetime().month < self.signalements[-1].datetime().month:
            self.new_archive()  # New year => new file

        archived = False
        try:
            f = open(self.current_file(), 'a', encoding='utf-8')
        except IOError:
            pass
        else:
            try:
                f.write(sig.archive() + "\n")
                Archives.write_counter += 1
                archived = True
            except IOError:
                pass
            finally:
                f.close()
        return archived

    def new_archive(self, filename=None):
        if filename is None:
            try:
                current = self.current_file()
                if current:
                    increment = int(os.path.splitext(current)[0][-4:]) + 1
                    filename = os.path.join(self.dir_path, "archives_{}.txt".format(increment))
                else:
                    filename = os.path.join(self.dir_path, "archives_{}.txt".format(datetime.datetime.now().year))
            except ValueError as e:
                print(e)
                filename = os.path.join(self.dir_path, "archives_tmp.txt")
        self.files.append(filename)
        return self.write_header(filename)

    def write_header(self, path):
        created = False
        header = "Date  | Auteur Sig.  | Code           | Flag        | Respomap                 | Description" + \
                 "                                                                                          | " + \
                 "Statut                                                      \n" + \
                 "------+--------------+----------------+-------------+--------------------------+------------" + \
                 "------------------------------------------------------------------------------------------+-" + \
                 "------------------------------------------------------------"
        try:
            f = open(path, 'w', encoding='utf-8')
        except IOError:
            pass
        else:
            try:
                f.write(header + "\n")
                Archives.write_counter += 1
                created = True
            except IOError as e:
                print(e)
            finally:
                f.close()
        return created

    def current_file(self):
        if self.files:
            return self.files[-1]
        return None

    def strip_comments(self):
        for sig in self.signalements:
            if '//' in sig.statut:
                sig.statut = sig.statut[:sig.statut.find('//')].strip()

    @staticmethod
    def parse(text, line_sep='\n', col_sep='|'):
        signalements = []
        if not isinstance(text, str):
            return signalements
        for line in text.split(line_sep):
            if line.strip() != '':
                values = [elem.strip() for elem in line.split(col_sep)]
                if "+" in values[4]:
                    sep = "+"
                else:
                    sep = ","
                values[4] = [respo.strip() for respo in values[4].split(sep)] if values[4] else []
                respo = values.pop(4)
                values.append(respo)
                s = Signalement(*values)
                signalements.append(s)
        return signalements

    def filter_sigs(self, key, *values, exact=False, func=None, source=None):
        s = []
        if source is None:
            source = self
        for sig in source:
            for value in values:
                if func:
                    if func(sig, value):
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

    def __repr__(self):
        return repr(self.signalements)

    def __str__(self):
        return "Sigs: {}".format(len(self.signalements))
