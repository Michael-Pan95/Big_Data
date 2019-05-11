#!/usr/bin/env python
import sys
import re

last_key = None
last_value = 0

# counting for total classes
last_label = None
last_label_total = 0

# counting for n(t)
last_word = None
last_nt_label = None
last_nt_count = 0

# with open('./letmesese', 'r') as f:
#     content = f.readlines()

for key_value_pair in sys.stdin:
    # for key_value_pair in content:
    if re.match('W\*.*', key_value_pair):  # if there is a star, it is for n(t)
        word, label, _ = key_value_pair.split(',')
        word = 'W=' + word.split('=')[-1]  # get rid of *
        if last_word is None:
            last_word = word
            last_nt_count = 1
        if last_nt_label is None:
            last_nt_label = label
        if word != last_word:  # if word change, we print the result out
            sys.stdout.write('{0},D=*,{1}\n'.format(last_word, last_nt_count))
            last_word = word
            last_nt_label = label
            last_nt_count = 1
        elif label != last_nt_label:  # word appear in different doc
            last_nt_count += 1
            last_nt_label = label
    elif re.match('D=.*,1.*', key_value_pair):  # class counter
        label = key_value_pair.rsplit(',')
        if last_label is None:
            last_label = label
            last_label_total = 1
        if label != last_label:
            last_label = label
            last_label_total += 1
    else:
        key, value = key_value_pair.rsplit(',', 1)
        value = int(value)
        if last_key is None:
            last_key = key
            last_value += value
        elif last_key == key:
            last_value += value
        else:
            sys.stdout.write('{0},{1}'.format(last_key, last_value) + '\n')
            last_key = key
            last_value = value
sys.stdout.write('{0},{1}\n'.format(last_key, last_value))  # last instance
sys.stdout.write('{0},{1}\n'.format('All', last_label_total))  # total label numbers
sys.stdout.write('{0},D=*,{1}\n'.format(last_word, last_nt_count))  # for last nt count
