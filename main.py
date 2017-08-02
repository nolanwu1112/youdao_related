# -*- coding: utf-8 -*-
""" extract data from youdao and writing it in a py file as a dict"""

import sqlite3
from extract import extracting
vocab_list = []

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
            cursor.execute('UPDATE pho SET youdao = ? WHERE vocab = ?;', (value, key))
            count = count + 1
            print(str(count)+ '/' + str(totalVocab))

def main():
    """main function"""
    print("main function initiated.")
    dict_der = {}
    # retrieve a list of vocabulary
    sql_res = retr_vocab("./database/vocab.db")
    print("Obtained vocabulary from database")

    for voc in sql_res:
        voc = str(voc[0])
        print("looping thru sql result: " + voc)
        try:
            dict_der[voc] = extracting(voc)
        except:
            dict_der[voc] = None
    print("Finishing writing dictionary!")
    store_der(r"./database/vocab.db", dict_der)
    print("Finishing writing database!!")
    with open(r"related_data.py", "w") as file:
        file.write(dict_der)
    print("Finishing writing data file!")

if __name__ == '__main__':
    main()
