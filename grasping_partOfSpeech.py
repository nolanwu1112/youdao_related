# -*- coding: utf-8 -*-
""" stay alone function to parse content based on input vocabulary"""

import urllib.request as ulreq
import urllib.error
import argparse
import bs4 as bs
from main import retr_vocab as retr

def extracting(vocab_input: str) ->list:
    """extract related words on youdao.com"""
    print("extracting vocab: " + vocab_input)
    # con_list = []
    dest_url = r"http://youdao.com/w/" + vocab_input + r"/#keyfrom=dict2.top"

    sauce = ulreq.urlopen(dest_url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')


    # finding tags to related words
    findings = soup.find('div', {'id':'relWordTab'})
    raw_content = []
    new_content = []
    temp_string = ''
    hasPassRoot = False
    if findings:
        vocab_root = findings.p.span.a.text

        for child in findings.strings:
            child_string = str(child)
            # print(type(child_string))
            if child_string == u'\n':
                pass
            elif u'词根' in child_string:
                pass
            elif (child_string == vocab_root) and (not hasPassRoot):
                hasPassRoot = True
            else:
                child_string = child_string.replace('\n', '').replace(' ', '')
                raw_content.append(child_string)
        print("Finishing tags cleaning")

    """
        for item in raw_content:
            if item == raw_content[-1]:
                temp_string = temp_string + " " + item
                new_content.append(temp_string)
            elif item == raw_content[0]:
                temp_string = item
            elif ('.' in item) and (item != raw_content[0]):
                new_content.append(temp_string)
                temp_string = item
    """
    regular_list = ["n.", "adj.", "adv.", "v.", "vi.", "vt.", "pron.", "int."]
    return [x for x in raw_content if ('.' in x) and (x not in regular_list)]

def filter_part(new_p: list, old_p: list):
    """ filter out the part of speech existed """
    return [x for x in new_p if x not in old_p]

def main():
    """ main function"""
#    parser = argparse.ArgumentParser()
#    parser.add_argument("vocab", help="Enter the vocab to find related vocab",\
#            type=str)
#    args = parser.parse_args()
#    extracting(args.vocab)
    sql_p = r"./database/vocab.db"
    vocab_list = retr(sql_p)
    part_list = ["n.", "adj.", "adv.", "v.", "vi.", "vt.", "pron.", "int."]
    for vocab in vocab_list:
        part_list.append(filter_part(extracting(vocab[0]), part_list))
    for i in part_list:
        print(i)
    with open(r"part_of_speeches.txt", "w") as file:
        for i in part_list:
            file.write(i)

if __name__ == "__main__":
    main()
