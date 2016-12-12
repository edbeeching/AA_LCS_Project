from __future__ import print_function

import random
import string
import time

import lcs_branch_and_bound
import lcs_recursive


def generate_random_list(length):

    words = [None]*length
    for i in range(length):
        words[i] = (random.choice(string.ascii_uppercase))

    return words


if __name__ == '__main__':
    print("Runtime comparisons")
    start = time.time()
    print("hello")
    end = time.time()
    print(end - start)
    time_dict_rec = {}
    for i in range(0, 14):
        time_dict_rec[i] = 0
        for _ in range(0, 40):
            list1 = generate_random_list(i)
            list2 = generate_random_list(i)
            start = time.time()
            lcs = lcs_recursive.lcs_recursive(list1, list2)
            time_dict_rec[i] += time.time() - start

    for i in range(0, 14):
        print(i, time_dict_rec.get(i))

    time_dict = {}
    print("-----------------------")
    for i in range(0, 40):
        time_dict[i] = 0
        for _ in range(0, 40):

            list1 = generate_random_list(i)
            list2 = generate_random_list(i)
            start = time.time()
            lcs_branch_and_bound.branch_n_bound(list1, list2)
            time_dict[i] += time.time() - start
    for i in range(0, 40):
        print(i, time_dict.get(i))
