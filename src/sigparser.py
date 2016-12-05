# -*- coding: utf-8 -*-
# !python3

import re
import logging

from signalement import Signalement

logger = logging.getLogger(__name__)

def parse(text, allow_duplicates=True, previous_sigs=None, sep="\n"):
    if previous_sigs is None:
        previous_sigs = []
    signalements = []

    if not isinstance(text, str):
        return signalements

    for line in text.split(sep):
        if line.strip() == '':
            continue

        matches = {
            "date": "([0-9]{1,2}/[0-9]{1,2})",
            "auteur": "([a-zA-Z]{1,12})",
            "code": "([0-9]{13})",
            "flag": "(.*)",
            "desc": "(.*)"
        }
        regex = "\[{date}\] {auteur} a signalé {code} \({flag}\) : {desc}".format(**matches)
        match = re.match(regex, line)
        if match:
            date, auteur, code, flag, desc = match.groups()
            s = Signalement(date, auteur, "@" + code, flag, desc)
            if ((s in signalements) or (s in previous_sigs)) and (not allow_duplicates):
                signalements.remove(s)
            signalements.append(s)
        else:
            logger.debug("Not a match : '{}'".format(line))

    return signalements
