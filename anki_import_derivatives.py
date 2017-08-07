# -*- coding: utf-8 -*-
""" This script imports derivatives obtained from dictionary.com
    with sqlite db: vocab.db
    in table: pho
"""

from related_data import der
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

errorlog = []
ERROR_LOG_PATH = r'./error.log'
def adding_derivatives():
    """
    Obtaining a list of vocab from anki db
    looping thru and adding derivatives
    """
    ids_cards = mw.col.findCards("mid:1496356407592")
    count = 0
    total = len(ids_cards)

#    for key, value in derivatives.items():
#        if value is not None:
#            derivatives[key] = value.decode("utf-8")

    for id_card in ids_cards:
        card = mw.col.getCard(id_card)
        note = card.note()
        vocab_anki = note['vocab']
        try:
            if der[vocab_anki] is not None:
                note["deri"] = der[vocab_anki].decode("utf-8")
            else:
                note["deri"] = "None"
        except KeyError:
            errorlog.append(vocab_anki + " ")
        note.flush()
        count = count + 1
    mw.reset()

#    with open(ERROR_LOG_PATH, "w") as file:
#        for word in errorlog:
#            file.write(word)
    error_info = ' '.join(errorlog)
    showInfo(error_info)
    showInfo(r"Change completed: {}/{}".format(count, total))


# Tag action
action = QAction("importing derivatives", mw)
action.triggered.connect(adding_derivatives)
mw.form.menuTools.addAction(action)
