#!/usr/bin/env python
import sys

if __name__ == "__main__":
    # with open('./letmesese', 'r') as f:
    #     content = f.readlines()
    nt_word = None  # keep track of nt
    nt_val = None  # keep track of nt
    for value_pair in sys.stdin:
        # for value_pair in content:
        value_pair = value_pair.strip()
        key, value = value_pair.rsplit(',', 1)
        if key == "All":
            sys.stdout.write(value_pair + '\n')
        elif key.split(',')[0] == "W=*":
            word, label = key.split(',')
            sys.stdout.write('{0},{1},{2}\n'.format(label, word, value))
        else:
            word, label = key.split(',')
            if label == "D=*":
                nt_word = word
                nt_val = value
            elif word == nt_word:
                sys.stdout.write('{0},{1},NT={2},{3}\n'.format(label, word, nt_val, value))  # original data
            else:
                print(word)
                print('Impossible! Something wrong')
