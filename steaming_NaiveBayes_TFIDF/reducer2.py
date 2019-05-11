#!/usr/bin/env python
import sys
import numpy as np
import re

if __name__ == "__main__":
    N = None
    last_label = None
    words_in_label = 0
    # with open('./letmesese', 'r') as f:
    #     content = f.readlines()

    for value_pair in sys.stdin:
        # for value_pair in content:
        value_pair = value_pair.strip()
        key, value = value_pair.rsplit(',', 1)
        value = int(value)
        if key == "All":  # total label types
            N = value
        elif re.match('.*W=\*.*', key):  # this is a document words indicator
            label, _ = key.split(',')
            if label != last_label:
                last_label = label
                words_in_label = value
        else:
            label, word, nt = key.split(',')
            nt = int(nt[3:])
            if label == last_label:
                tfidf = round(value / words_in_label * np.log(N / nt), 6)
                sys.stdout.write('{0}\t{1}\t{2}\n'.format(label, word, tfidf))
            else:
                print(label)
                print('Something wrong')
