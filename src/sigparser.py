# -*- coding: utf-8 -*-
# !python3

import logging
import re

from signalement import Signalement
from utils import log_args

logger = logging.getLogger(__name__)


@log_args(logger=logger)
def parse(text, allow_duplicates=True, previous_sigs=None):
    if previous_sigs is None:
        previous_sigs = []
    signalements = []

    if not isinstance(text, str):
        return signalements

    for line in text.splitlines():
        if line == "":
            continue

        matches = {
            "date": "([0-9]{1,2}/[0-9]{1,2})",
            "auteur": "([a-zA-Z]{1,12})",
            "code": "([0-9]{13})",
            "flag": "(.*)",
            "desc": "(.+)"
        }
        regex = r"\[{date}\] {auteur} a signalé {code} \({flag}\) : {desc}".format(**matches)
        match = re.match(regex, line)
        if match:
            date, auteur, code, flag, desc = match.groups()
            s = Signalement(date, auteur, "@" + code, flag, desc)
            if ((s in signalements) or (s in previous_sigs)) and (not allow_duplicates):
                signalements.remove(s)
            signalements.append(s)
            logger.debug("Parsed sig : {}".format(s))
        else:
            logger.debug("Not a match : '{}'".format(line))

    return signalements
