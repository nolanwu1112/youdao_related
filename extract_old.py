# -*- coding: utf-8 -*-
""" stay alone function to parse content based on input vocabulary"""

import urllib.request as ulreq
import bs4 as bs

def extracting(vocab_input: str) ->list:
    """extract related words on dictionary.com"""
    print("extracting vocab: " + vocab_input)
    con_list = []
    dest_url = r"http://www.dictionary.com/browse/" + vocab_input + r"?s=t"
    # dest_url = r"http://www.merriam-webster.com/dictionary/" + vocab
    # tag: class = "runon-attributes"
    sauce = ulreq.urlopen(dest_url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    findings = soup.find_all('div', class_="tail-elements")

    for finding in findings:
        if ('tail-type-relf' in finding.parent.parent['class']) and \
        ('pm-btn-spot' in finding.parent.parent['class']):
        # if 'ce-spot' in finding.parent['class']:
            # string_l = finding.text
            temp = finding.text
            if "with" in temp:
                temp = finding.text.replace('verb (used with object)', 'vt')
            temp = temp.replace("noun", "n").replace("adverb", "adv").replace("adjective", "adj")
            temp = temp.replace("\n", '').replace(" ", "")
            # string_l = temp.split(",")
            # con_list.append(string_l)
            con_list.append(temp)
    for item in con_list:
        item = ', '.join(item)
    result = '\n'.join(con_list)
    print("extracting result: " + result)
    return result
