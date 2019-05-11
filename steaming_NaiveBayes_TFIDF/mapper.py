#!/usr/bin/env python
import sys
import re


def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)


def mapper(doc, labels):
    for label in labels:
        # count instance
        sys.stdout.write("Y=*,{0}".format(1) + '\n')
        # count label
        sys.stdout.write("Y={0},{1}".format(label, 1) + '\n')
        for word in doc:
            # count words in label
            sys.stdout.write("Y={0},W=*,{1}".format(label, 1) + '\n')
            # count specific word
            sys.stdout.write("Y={0},W={1},{2}".format(label, word, 1) + '\n')


if __name__ == "__main__":
    full_train = sys.stdin.readlines()
    for instance in full_train:
        id, labels, doc = instance.split('\t')
        labels = labels.split(',')
        doc = tokenizeDoc(doc)
        mapper(doc, labels)
