# -*- coding: utf-8 -*-
# !python3

import datetime
import glob
import logging
import os

import utils
from signalement import Signalement

logger = logging.getLogger(__name__)


class Archives():
    read_counter = 0
    write_counter = 0

    def __init__(self, dir_path, pattern):
        self.dir_path = dir_path
        self.pattern = pattern
        self.signalements = []
        self.files = glob.glob(os.path.join(dir_path, pattern))
        self.current_file = None

    def refresh(self):
        self.files = glob.glob(os.path.join(self.dir_path, self.pattern))
        self.open()

    def open(self):
        self.signalements = []
        for file in self.files:
            logger.info("Reading \"{}\"".format(file))
            self.current_file = file
            try:
                f = open(file, "r", encoding="utf-8")
            except IOError as e:
                logger.error(e)
            else:
                try:
                    raw_text = "".join(f.readlines()[2:])
                    self.signalements.extend(self.parse(raw_text))
                    Archives.read_counter += 1
                except (IOError, IndexError) as e:
                    logger.error(e)
                finally:
                    f.close()

    def archive_sig(self, sig):
        if not self.files:
            self.new_archive(os.path.join(self.dir_path, "archives_{}.txt".format(sig.datetime().year)))
        if self.signalements and sig.datetime().month < self.signalements[-1].datetime().month:
            self.new_archive()  # New year => new file

        archived = False
        logger.info("Writing {} to '{}'".format(sig.fields(), self.current_file))
        try:
            f = open(self.current_file, "a", encoding="utf-8")
        except IOError as e:
            logger.error(e)
        else:
            try:
                f.write(sig.archive() + "\n")
                self.signalements.append(sig)
                Archives.write_counter += 1
                archived = True
            except IOError as e:
                logger.error(e)
            finally:
                f.close()
        return archived

    def new_archive(self, filename=None):
        if filename is None:
            filename = os.path.join(self.dir_path, "archives_{}.txt".format(datetime.datetime.now().year))

        if filename not in self.files:
            self.files.append(filename)
            self.current_file = filename
            return self.write_header(filename)

    def write_header(self, path):
        created = False
        header = "Date  | Auteur Sig.  | Code           | Flag        | Respomap                 | Description" + \
                 "                                                                                          | " + \
                 "Statut                                                      \n" + \
                 "------+--------------+----------------+-------------+--------------------------+------------" + \
                 "------------------------------------------------------------------------------------------+-" + \
                 "------------------------------------------------------------"
        logger.info("Creating archive file \"{}\"".format(path))
        try:
            f = open(path, "w", encoding="utf-8")
        except IOError as e:
            logger.error(e)
        else:
            try:
                f.write(header + "\n")
                Archives.write_counter += 1
                created = True
            except IOError as e:
                logger.error(e)
            finally:
                f.close()
        return created

    def strip_comments(self):
        for sig in self.signalements:
            if "//" in sig.statut:
                sig.statut = sig.statut[:sig.statut.find("//")].strip()

    def parse(self, text, col_sep="|"):
        signalements = []
        year = utils.extract_numbers(self.current_file)[0]
        if not isinstance(text, str):
            return signalements
        for line in text.splitlines():
            if line.strip() != "":
                values = [elem.strip() for elem in line.split(col_sep)]
                values[0] = values[0] + "/" + year[2:]
                values[4] = [respo.strip() for respo in values[4].split(",")] if values[4] else []
                respo = values.pop(4)
                values.append(respo)
                s = Signalement(*values)
                signalements.append(s)
        return signalements

    def filter_sigs(self, key=None, values=None, exact=False, func=None, source=None):
        if key is None or values is None:
            return self.signalements
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
        n = len(self.signalements)
        s = "Sigs : {}".format(n)
        if n > 0:
            first, last = self.signalements[0], self.signalements[-1]
            s += "\nFrom {} to {}".format(first.date, last.date)
        return s
