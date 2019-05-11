#!/usr/bin/env python
import sys


# def reducer(value_pairs):
#     last_key = None
#     last_value = 0
#     for v in value_pairs:
#         key, value = v.rsplit(',', 1)
#         value = int(value)
#         if last_key is None:
#             last_value += value
#             last_key = key
#         elif last_key == key:
#             last_value += value
#         else:
#             sys.stdout.write(('{0},{1}'.format(last_key, last_value)) + '\n')
#             last_key = key
#             last_value = value
#     sys.stdout.write(('{0},{1}'.format(last_key, last_value)) + '\n')
#
#
# if __name__ == "__main__":
#     value_pairs = sys.stdin.readlines()
#     # with open('../10605_F18_HW2/train_reducer.txt', 'r') as f:
#     #     value_pairs = f.readlines()
#     reducer(value_pairs)

last_key = None
last_value = 0
for v in sys.stdin:
    key, value = v.rsplit(',', 1)
    value = int(value)
    if last_key is None:
        last_value += value
        last_key = key
    elif last_key == key:
        last_value += value
    else:
        sys.stdout.write(('{0},{1}'.format(last_key, last_value)) + '\n')
        last_key = key
        last_value = value
sys.stdout.write(('{0},{1}'.format(last_key, last_value)) + '\n')
