# -*- coding: utf-8 -*-
""" This script imports derivatives obtained from dictionary.com
    with sqlite db: vocab.db
    in table: pho
"""

# import sqlite3
from related_data import der
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

def adding_derivatives():
    """
    Obtaining a list of vocab from anki db
    looping thru and adding derivatives
    """
    ids_cards = mw.col.findCards("mid:1496356407592")
    count = 0
    total = len(ids_cards)

    for id_card in ids_cards:
        card = mw.col.getCard(id_card)
        note = card.note()
        vocab_anki = note['vocab']
        try:
            note["derivatives"] = der[vocab_anki].decode("utf-8")
        except KeyError:
            pass
        note.flush()
        count = count + 1
    mw.reset()

    showInfo(r"Change completed: {}/{}".format(count, total))


# Tag action
action = QAction("importing derivatives", mw)
action.triggered.connect(adding_derivatives)
mw.form.menuTools.addAction(action)
