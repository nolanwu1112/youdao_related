# -*- coding: utf-8 -*-
""" extract data from youdao and writing it in a py file as a dict"""

import sqlite3
from extract import extracting

# SQL_PATH_CUS = "./database/vocab.db"
SQL_PATH_CUS = "./database/test.db"

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

    total_vocab = len(vocab_dict)
    count = 0
    with sqlite3.connect(sql_path) as connection:
        cursor = connection.cursor()
        for key, value in vocab_dict.items():
            cursor.execute('UPDATE pho SET youdao = ? WHERE vocab = ?;', (value, key))
            count = count + 1
            # print(str(count)+ '/' + str(totalVocab))
            print(r"Modifying database {}/{}".format(count, total_vocab))

def main(sql_input):
    """main function"""
    print("main function initiated.")
    dict_der = {}
    # retrieve a list of vocabulary
    sql_res = retr_vocab(sql_input)
    print("Obtained vocabulary from database")
    vocab_list = [vocab[0] for vocab in sql_res]
    vocab_list.sort()
    total = len(vocab_list)
    count = 0
    for voc in vocab_list:
        voc = str(voc)
        print("looping thru sql result: " + voc)
        dict_der[voc] = extracting(voc)
        count += 1
        print(r"{}/{}".format(count, total))

    print("Finishing writing dictionary!")
    store_der(SQL_PATH_CUS, dict_der)
    print("Finishing writing database!!")
    with open(r"related_data.py", "w") as file:
        file.write(dict_der)
    print("Finishing writing data file!")

if __name__ == '__main__':
    main(SQL_PATH_CUS)
