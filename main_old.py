# -*- coding: utf-8 -*-
""" todo:
#* 1. Build a dict of vocab that needs derivatives
#* 2. Explore the possibility of using data structures
# 3. Explore dictionary.com's web structure
# 4. Extract content with bs4
# 5. Build a dict of vocab with derivative
# 6. Anki import file
"""

import sqlite3
import time
# import progressbar
from extract import extracting
# predefined attributes
vocab_list = []
err_log = r"/error_log/log.txt"

# Method: retrieve vocab
def retr_vocab(sql_path):
    """ access sql and retrieve a list of vocabulary"""
    with sqlite3.connect(sql_path) as connection:
        print("Connection to SQL successfully!")
        cursor = connection.cursor()
        cursor.execute("SELECT vocab FROM pho;")
        result = cursor.fetchall()
        return result

def store_der(sql_path, vocab_dict):
    """ store extracted derivatives based back to pho in the vocab.db"""

    totalVocab = len(vocab_dict)
    count = 0
    with sqlite3.connect(sql_path) as connection:
        cursor = connection.cursor()
        for key, value in vocab_dict.items():
            cursor.execute('UPDATE pho SET derivatives = ? WHERE vocab = ?;', (value, key))
            count = count + 1
            print(str(count)+ '/' + str(totalVocab))

def main():
    """main function"""
    print("main function initiated.")
    dict_der = {}
    # retrieve a list of vocabulary
    sql_res = retr_vocab("./database/vocab.db")
    print("Obtained vocabulary from database")
    # sql_res = ['glaze', 'abandon']

    for voc in sql_res:
        voc = str(voc[0])
        print("looping thru sql result: " + voc)
        try:
            temp_ = extracting(voc)
            dict_der[voc] = temp_
        except:
            dict_der[voc] = None
    print("Finishing writing dictionary!")
    store_der(r"./database/vocab.db", dict_der)

if __name__ == '__main__':
    main()
