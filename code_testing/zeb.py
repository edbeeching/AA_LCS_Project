from __future__ import print_function

import random
import string

from nltk.corpus import stopwords


def generate_random_list(length):

    words = [None]*length
    for i in range(length):
        words[i] = (random.choice(string.ascii_uppercase))

    return words


if __name__ == '__main__':


    words = stopwords.words("english")
    print(words)

    # words1 = generate_random_list(10)
    # words2 = generate_random_list(12)
    # print(words1)
    # print(words2)
    # #words1 = ['C', 'Z', 'G', 'G', 'G', 'G', 'V', 'W', 'K', 'K']
    # #words2 = ['J', 'H', 'C', 'A', 'C', 'N', 'V', 'T', 'F', 'T', 'N', 'Z']
    # lcs_rec = lcs_recursive.lcs_recursive(words1, words2)
    # lcs_bnb = lcs_branch_and_bound.branch_n_bound(words1, words2)
    # lcs_dyn = prototype.LCSclassic([" "]+words1, [" "]+words2)
    #
    # print(lcs_rec, len(lcs_rec))
    # print(lcs_bnb, len(lcs_bnb))
    # print(lcs_dyn, len(lcs_dyn))
