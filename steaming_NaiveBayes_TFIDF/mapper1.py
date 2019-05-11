#!/usr/bin/env python
import sys
import re


def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)


def mapper(doc):
    label, doc = doc.split('\t')
    doc = tokenizeDoc(doc)

    sys.stdout.write('D={0},1'.format(label) + '\n')  # count document
    for word in doc:
        sys.stdout.write('W=*,D={0},{1}\n'.format(label, 1))  # count specific word
        sys.stdout.write('W={0},D={1},{2}\n'.format(word, label, 1))  # count specific word
        sys.stdout.write('W*={0},D={1},{2}\n'.format(word, label, 1))  # count n(t)


if __name__ == "__main__":
    # with open('./train.txt', 'r') as f:
    #     docs = f.readlines()

    for doc in sys.stdin:
        mapper(doc)
