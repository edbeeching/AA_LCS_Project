"""
    This module implements longest common subsequence with a branch and bound approach
    Created by Edward Beeching 09/11/2016

    The only "public" function is the branch_n_bound(words1, words2) which takes two lists of words / chars / etc and
    returns the longest common subsequence using a the branch a bound method.

    The method itself uses a last in first out queue (LIFO Queue) to traverse the tree looking for solutions.


    The function _find_bounds(list1, list2)
        The upper and lower bounds of the LCS are computed using a hash table for efficiency.

        For example strings A,B,C,D,C,E  & C,D,E,F,G,C

        Lower bound:
        Maximum occurence of a single letter is [C,C] therefore this is the length of the smallest possible substring


        Upper bound:
        Sum of occurences of letters in common better both strings, in this case this will be
        [C,C] + [D] + [E] = 4
        This will be the length of the longest possible subsequence

    The function _find_index_of_first(first, start, wordlist)
        This looks for a character or word "first" in the wordlist starting at the index "start"

        For Example A,B,C,A,B,C

        if first=A, start=0 the function returns 0
        if first=B, start=0 the function returns 1
        if first=A, start=1 the function returns 3
        if first=D, start=0 the function returns 10^9



"""
from __future__ import print_function
import Queue
import copy


def branch_n_bound(words1, words2):
    """
    This function computes the LCS using a branch and bound method. See comments at start of module for further details.

    :param words1: The first list of strings to compare
    :param words2: The second list of strings to compare
    :return: The LCS, returned as a list of strings
    """

    max_lcs_length = min(len(words1), len(words2))
    best, _upper = _find_bounds(words1, words2)

    starting_solution = (1 << max_lcs_length) - 1
    best_solution = starting_solution * 0

    solution_index = -1
    tracker_index = -1

    # Potential solutions are stored in a LIFO queue to be searched depth first
    # Solutions are defined in a list as follows:
    # [starting_solution, solution_index, tracker_index, best, left/right of tree]
    lifo_queue = Queue.LifoQueue()
    lifo_queue.put([starting_solution, solution_index, tracker_index, best, 1])

    best = max(best - 1, 0)
    # logfile = open('log.txt', 'w')
    # logfile.write("estimate of best is " + str(best) + "\n")
    # logfile.write("max length is " + str(max_lcs_length) + "\n")
    # logfile.write("--------------------------------" + "\n")

    while not lifo_queue.empty():
        node = lifo_queue.get()
        # if node[3] > best:
        #     logfile.write(str(_get_solution(words1, words2, node[0])) + str(node) + "\n")
        # else:
        #     logfile.write(" CUT " + str(_get_solution(words1, words2, node[0])) + str(node) + " CUT\n")

        if node[3] > best and node[1] < max_lcs_length - 1:
            node1, node2 = _explore(node, words1, words2)
            if node1[3] >= node2[3]:
                if node2[3] > best:
                    lifo_queue.put(node2)
                if node1[3] > best:
                    lifo_queue.put(node1)
            else:
                if node1[3] > best:
                    lifo_queue.put(node1)
                if node2[3] > best:
                    lifo_queue.put(node2)
        else:
            # if node[1] == (max_lcs_length - 1):
            #     # print("at end of tree")
            if node[3] > best and node[1] == (max_lcs_length - 1):
                # print("New Best found", node)
                # logfile.write("--------------------------------" + "\n")
                best = node[3]
                best_solution = node[0]
    # logfile.close()
    return _get_solution(words1, words2, best_solution)


def _find_bounds(list1, list2):
    """
    See intro for details of this function.

    :param list1: The first list of strings to compare
    :param list2: The second list of strings to compare
    :return: returns two integers, the lower and upper bounds
    """
    if len(list1) > len(list2):
        return _find_bounds(list2, list1)

    list1_dict = {}
    list2_dict = {}

    # Use a dictionary (Hash table) to map occurrences of words
    for word in list1:
        if list1_dict.get(word) is None:
            list1_dict[word] = 1
        else:
            list1_dict[word] += 1

    for word in list2:
        if list2_dict.get(word) is None:
            list2_dict[word] = 1
        else:
            list2_dict[word] += 1

    combined_dict = {}
    for word, value in list1_dict.iteritems():
        if list2_dict.get(word) is None:
            continue
        else:
            combined_dict[word] = min(value, list2_dict[word])

    lower_bound = 0
    upper_bound = 0
    for word, value in combined_dict.iteritems():
        upper_bound += value
        lower_bound = max(lower_bound, value)

    return lower_bound, upper_bound


def _find_index_of_first(first, start, word_list):
    """
    Finds the first index of a characted/string in a list of strings, if the char does not exist, return 10^9

    :param first:
    :param start:
    :param word_list:
    :return:
    """

    if start > len(word_list)-1:
        return 1000000000
    for index, word in enumerate(word_list[start:]):
        if word == first:
            return start + index
    return 1000000000  # if the word is not found return a very high value


def _find_sub_lcs_length(solution1, index, length):
    total = 0
    for i in range(0, index+1):
        # Bit shift to find if index is in solution
        if solution1 & (1 << ((length - 1) - i)) > 0:
            total += 1
    return total


def _explore(node, words1, words2):
    if len(words1) > len(words2):
        return _explore(node, words2, words1)
    # [starting_solution, solution_index, tracker_index, best]
    max_lcs_length = min(len(words1), len(words2))
    # explore node on left
    node1 = copy.deepcopy(node)
    node1[4] = 1
    node1[1] += 1
    # print(node1[1])
    # print(words1[node1[1]], node1[1])
    next_index = _find_index_of_first(words1[node1[1]], node1[2] + 1, words2)
    if next_index == 1000000000:
        # if this is the case the we will not be using this solution
        node1[2] = -2
        node1[3] = -2
    else:
        node1[2] = next_index
        lower, upper = _find_bounds(words1[node1[1] + 1:], words2[node1[2] + 1:])
        node1[3] = _find_sub_lcs_length(node1[0], node1[1], max_lcs_length) + upper

    # explore node on right
    node2 = copy.deepcopy(node)
    node2[4] = 2
    node2[1] += 1
    # tracker index does not change here
    # print(node2)
    node2[0] -= (1 << ((max_lcs_length-1) - node2[1]))
    # print(node2)
    lower, upper = _find_bounds(words1[node2[1] + 1:], words2[node2[2] + 1:])
    node2[3] = _find_sub_lcs_length(node2[0], node2[1], max_lcs_length) + upper

    return node1, node2


def _get_solution(list1, list2, best_solution):
    if len(list1) > len(list2):
        return _get_solution(list2, list1, best_solution)

    max_length = len(list1)
    solution = []
    for index, word in enumerate(list1):
        if best_solution & (1 << ((max_length - 1) - index)) > 0:
            solution.append(word)
    return solution


if __name__ == '__main__':
    print("Branch and Bound Testing")

    file1 = open("../corpus-adv_preprocessed/ex1.txt")
    file2 = open("../corpus-adv_preprocessed/ex2.txt")

    _words1 = file1.read().split()
    _words2 = file2.read().split()

    lcs = branch_n_bound(_words1, _words2)
    print(lcs)

    exit()
    # # Test functions to ensure expected results
    # # find_bounds(list1, list2):
    # print("Find bounds")
    # low, up = find_bounds(["A","A","C","D","D"],["A","A","D","D","E"])
    # print("Low:", low, "Up", up)
    # # find_index_of_first(first, start, list):
    # print(find_index_of_first("A",2,["D","A","C","D","A"]))
    # print("find_sub_lcs_length")
    # print(find_sub_lcs_length(1,1,2))
    # # find_sub_lcs_length(solution, index, length):
    # print("Sub LSC length")
    # print(find_sub_lcs_length(31, 4, 5))
    # # explore(node, words1, words2):
    # # get solution
    # print(get_solution(["A","B","C","D","E"],["A","B","C","D","E"],10))
    # print("{0:016b}".format(10))
