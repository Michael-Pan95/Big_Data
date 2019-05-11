import re
import sys

import numpy as np


def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)


def update_dict(keyword, count_dict):
    if keyword in count_dict:
        count_dict[keyword] += 1
    else:
        count_dict[keyword] = 1


def train_NB(train_files, count_dict, vocabulary_set, class_set):
    labels_list = []
    doc_list = []
    for instance in train_files:
        has_cat = False
        labels, doc = instance.split('\t')
        labels = labels.split(',')
        for label in labels:
            if re.search("CAT", label):
                has_cat = True
                labels_list.append((label, len(doc_list)))  # (label, doc_index)
        if has_cat:
            doc_list.append(tokenizeDoc(doc))  # using given tokenizer
    if len(labels_list) == 0:
        return None
    else:
        for (label, w_index) in labels_list:
            # record classes
            class_set.add(label)
            # count instance
            key_word = 'Y=*'
            update_dict(keyword=key_word, count_dict=count_dict)
            # count label
            key_word = 'Y={0}'.format(label)
            update_dict(keyword=key_word, count_dict=count_dict)
            for word in doc_list[w_index]:
                # unique word count
                vocabulary_set.add(word)
                # count total words within a document
                key_word = 'Y={0},W=*'.format(label)
                update_dict(keyword=key_word, count_dict=count_dict)
                # count specific word
                key_word = 'Y={0},W={1}'.format(label, word)
                update_dict(keyword=key_word, count_dict=count_dict)


if __name__ == "__main__":
    count_dict = {}
    vocabulary_set, class_set = set(), set()
    # raw_data = open('./RCV1.small_train.txt', 'r')
    raw_data = sys.stdin.readlines()
    train_NB(raw_data, count_dict, vocabulary_set, class_set)
    # add classes to the
    count_dict['vocabulary_size'] = len(vocabulary_set)
    count_dict['classes_name'] = ' '.join(class_set)
    for key, value in count_dict.items():
        # print(key + '\t' + str(value))
        sys.stdout.write(key + '\t' + str(value) + '\n')
