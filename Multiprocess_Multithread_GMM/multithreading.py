import time
import warnings
from concurrent import futures

import matplotlib.pyplot as plt
import numpy as np
import urllib3

import sys

def visit_url(url):
    start = time.time()
    # create pool Manager
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http_Manager = urllib3.PoolManager()
    content = http_Manager.urlopen('GET', url)
    end = time.time()
    return [start, end]


def visualize_runtimes(results, image_name):
    start, stop = np.array(results).T
    min_start = min(start)
    plt.barh(range(len(start)), stop - start, left=start - min_start)
    plt.grid(axis='x')
    plt.ylabel("Tasks")
    plt.xlabel("Seconds")
    plt.savefig(image_name)
    plt.show(image_name)


if __name__ == "__main__":
    warnings.filterwarnings(action='once')
    urls = sys.stdin.readlines()
    # one processor
    with futures.ThreadPoolExecutor(max_workers=1) as executor:
        url_time_multi = [data for data in executor.map(visit_url, urls)]
    visualize_runtimes(url_time_multi, "1_thread.png")
    # two processor
    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        url_time_multi = [data for data in executor.map(visit_url, urls)]
    visualize_runtimes(url_time_multi, "2_thread.png")
    # four processor
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        url_time_multi = [data for data in executor.map(visit_url, urls)]
    visualize_runtimes(url_time_multi, "4_thread.png")
