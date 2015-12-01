# -*- coding: utf-8 -*-
# !python3

from signalement import Signalement


# parser dégueu fait à la va vite, mais il marche !!
# je m'y connais pas assez en regex pour faire un truc propre

def parse(text, allow_duplicates=True, previous_sigs=None, sep="\n"):
    if previous_sigs is None:
        previous_sigs = []
    signalements = []
    if not isinstance(text, str):
        return signalements
    for line in text.split(sep):
        if line != "":
            sig = [elem.strip() for elem in line.split(" ")]
            del sig[2:4]
            sig[0] = sig[0][1:-1]  # Enlève les [] autour de la date
            if "guide" in sig[4]:
                sig[3] = sig[3][1:] + " " + sig[4][:-1]  # Enlève les () autour du flag et merge No + guide
                del sig[4]
            else:
                sig[3] = sig[3][1:-1]  # Enlève les () autour du mode
            del sig[4]
            sig[4] = " ".join(sig[4:])  # Merge la description
            sig = sig[:5]
            sig[2] = "@" + sig[2]  # Rajoute @ devant le timestamp

            s = Signalement(*sig)
            if ((s in signalements) or (s in previous_sigs)) and (not allow_duplicates):
                signalements.remove(s)
            signalements.append(s)

    return signalements
