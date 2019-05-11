if __name__ == "__main__":
    with open('./part-00000', 'r') as f:
        value_pairs = f.readlines()

    last_label = None
    top_list = []
    tmp_value_list = []
    for v in value_pairs:
        split_result = v.split(',')
        if split_result[0] == 'Y=*' or len(split_result) != 3 or split_result[1] == 'W=*':
            continue
        label, word, value = split_result[0], split_result[1], split_result[2]
        label = label[2:]
        word = word[2:]
        value = int(value)
        if last_label is None:
            last_label = label
        if label == last_label:
            tmp_value_list.append((label, word, value))
        else:
            if last_label != 'other':
                top_result = sorted(tmp_value_list, key=lambda a: a[2], reverse=1)[:10]
                for top in top_result:
                    top_list.append(top)
            tmp_value_list = []
            last_label = label
            tmp_value_list.append((label, word, value))

    if tmp_value_list[0][0] != 'other':
        top_result = sorted(tmp_value_list, key=lambda a: a[2], reverse=1)[:10]
        for top in top_result:
            top_list.append(top)

    with open('./top10.txt', 'w') as f:
        for i in range(len(top_list)):
            f.write('{0}\t{1}\t{2}\n'.format(top_list[i][0], top_list[i][1], top_list[i][2]))
            print('{0}\t{1}\t{2}\n'.format(top_list[i][0], top_list[i][1], top_list[i][2]))
