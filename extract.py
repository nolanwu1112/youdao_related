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
    raw_content = []
    new_content = []
    temp_list = []
    temp_string = ''
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

    for item in raw_content:
        if item == raw_content[-1]:
            temp_string = temp_string + " " + item
            new_content.append(temp_string)
        elif item == raw_content[0]:
            temp_string = item
        elif ('.' in item) and (item != raw_content[0]):
            new_content.append(temp_string)
            temp_string = item
        else:
            temp_string = temp_string + " " + item
    print("<br>".join(new_content))
    return vocab_input, "<br>".join(new_content)

def main():
    """ main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("vocab", help="Enter the vocab to find related vocab",\
            type=str)
    args = parser.parse_args()
    extracting(args.vocab)

if __name__ == "__main__":
    main()
