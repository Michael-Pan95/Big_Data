import sys


def decorator_next(f):
    def wrapper_next(*args, **kwargs):
        c = f(*args, **kwargs)
        next(c)
        return c

    return wrapper_next


@decorator_next
def coroutine_toASCII(child):
    while True:
        word = yield
        for w in word:
            child.send(ord(w))


@decorator_next
def coroutine_avg(file_name):
    total = 0
    n = 0
    try:
        while True:
            ascii_num = yield
            total += ascii_num
            n += 1
    except GeneratorExit:
        print('{0} : {1}'.format(file_name, total / n))


@decorator_next
def coroutine_word_splitter(child):
    while True:
        line = yield
        words = line.split(' ')
        for w in words:
            child.send(w.strip())


def line_splitter(doc_list, child):
    for line in doc_list:
        child.send(line)


if __name__ == "__main__":
    # get input from standard input stream
    line_splitter(sys.stdin.readlines(),
                  child=coroutine_word_splitter(child=coroutine_toASCII(child=coroutine_avg(file_name="Average ASCII"))))