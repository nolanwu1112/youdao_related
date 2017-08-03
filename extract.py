# -*- coding: utf-8 -*-
""" stay alone function to parse content based on input vocabulary"""

import urllib.request as ulreq
import argparse
import bs4 as bs

def extracting(vocab_input: str) ->list:
    """extract related words on youdao.com"""
    print("extracting vocab: " + vocab_input)
    # con_list = []
    dest_url = r"http://youdao.com/w/" + vocab_input + r"/#keyfrom=dict2.top"

    sauce = ulreq.urlopen(dest_url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    # finding tags to related words
    findings = soup.find('div', {'id':'relWordTab'})
    part_speech = {}
    raw_content = []
    new_content = []
    temp_string = ''
    temp_list = []
    dict_content = []
    vocab_root = findings.p.span.a.text
    hasPassRoot = False

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

    # Part of speech + vocabulary + Chinese definitions
    for item in raw_content:
        if item == raw_content[-1]:
            temp_string = temp_string + " " + item
            temp_list.append(item)
            new_content.append(temp_string)
            dict_content.append(temp_list[:])
        elif item == raw_content[0]:
            temp_string = item
            temp_list = []
            temp_list.append(item)
        elif ('.' in item) and (item != raw_content[0]):
            new_content.append(temp_string)
            temp_string = item
            dict_content.append(temp_list[:])
            temp_list = []
            temp_list.append(item)
        else:
            temp_string = temp_string + " " + item
            temp_list.append(item)
    print("<br>".join(new_content))
    temp_dict_1 = {}
    temp_dict_2 = {}
    # constructing a dictionary for part of speech
    for first_layer in dict_content:
        for ind in range(1, len(first_layer)-1, 2):
            temp_dict_2[first_layer[ind]] = first_layer[ind + 1]
        temp_dict_1[first_layer[0]] = temp_dict_2.copy()
    part_speech[vocab_input] = temp_dict_1.copy()
    print(str(part_speech))
    # return a importable text separated with breaklines <br>
    return "<br>".join(new_content), part_speech

def main():
    """ main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("vocab", help="Enter the vocab to find related vocab",\
            type=str)
    args = parser.parse_args()
    extracting(args.vocab)

if __name__ == "__main__":
    main()
