""" This modules implements longest common subsequence with a branch and bound approach
    Created by Edward Beeching 09/11/2016 """
from __future__ import print_function
import Queue
import copy
import time

def find_bounds(list1, list2):
    if len(list1) > len(list2):
        return find_bounds(list2, list1)

    list1_dict = {}
    list2_dict = {}

    # Use a dictionary (Hash table) to map occurrences of words
    for word in list1:
        if list1_dict.get(word) == None:
            list1_dict[word] = 1
        else:
            list1_dict[word] += 1

    for word in list2:
        if list2_dict.get(word) == None:
            list2_dict[word] = 1
        else:
            list2_dict[word] += 1

    combined_dict = {}
    for word, value in list1_dict.iteritems():
        if list2_dict.get(word) == None:
            continue
        else:
            combined_dict[word] = min(value, list2_dict[word])

    lower_bound = 0
    upper_bound = 0
    for word, value in combined_dict.iteritems():
        upper_bound += value
        lower_bound = max(lower_bound, value)

    return lower_bound, upper_bound


def find_index_of_first(first, start, list):
    if start>len(list):
        return 1000000000
    for index, word in enumerate(list[start:]):
        if word == first:
            return start + index
    return 1000000000 # if the word is not found return a very high value


def find_sub_lcs_length(solution1, index, length):
    # print("find sub lcs length", solution1, index, length)
    total = 0
    for i in range(0, index+1):
        # Bit shift to find if index is in solution
        # print(length, (1 << ((length -1) - i)))
        if solution1 & (1 << ((length -1) - i)) > 0:
            total += 1
    return total


def explore(node, words1, words2):
    if len(words1) > len(words2):
        return explore(node, words2, words1)
    # [starting_solution, solution_index, tracker_index, best]
    max_lcs_length = min(len(words1), len(words2))
    # explore node on left
    node1 = copy.deepcopy(node)
    node1[4] = 1
    node1[1] += 1
    # print(node1[1])
    # print(words1[node1[1]], node1[1])
    next_index = find_index_of_first(words1[node1[1]], node1[2]+1, words2)
    if next_index == 1000000000:
        # if this is the case the we will not be using this solution
        node1[2] = -2
        node1[3] = -2
    else:
        node1[2] = next_index
        lower, upper = find_bounds(words1[node1[1]+1:], words2[node1[2]+1:])
        node1[3] = find_sub_lcs_length(node1[0], node1[1], max_lcs_length) + upper

    # explore node on right
    node2 = copy.deepcopy(node)
    node2[4] = 2
    node2[1] += 1
    # tracker index does not change here
    # print(node2)
    node2[0] -= (1 << ((max_lcs_length-1) - node2[1]))
    # print(node2)
    lower, upper = find_bounds(words1[node2[1]+1:], words2[node2[2]+1:])
    node2[3] = find_sub_lcs_length(node2[0], node2[1], max_lcs_length) + upper

    return node1, node2


def get_solution(list1, list2, best_solution):
    if len(list1) > len(list2):
        return get_solution(list2, list1, best_solution)

    max_length = len(list1)
    solution = []
    for index, word in enumerate(list1):
        if best_solution & (1 << ((max_length -1) - index)) > 0:
            solution.append(word)

    return solution


if __name__ == '__main__':
    print("Branch and Bound Testing")
    lb, ub = find_bounds(["g","a","e","b","c","e","e"],["e","e","f","g","d"])
    file1 = open("../corpus-adv_preprocessed/ex1.txt")
    file2 = open("../corpus-adv_preprocessed/ex2.txt")

    words1 = file1.read().split()
    words2 = file2.read().split()

    # words1 = ["A","D","A","B","A"]
    #words2 = ["A","C","D","B","B"]
    # words2 = ["A", "D","E","F","E"]
    # words1 = [ "P","F","E","H","G"]

    lb, ub = find_bounds(words1, words2)

    max_lcs_length = min(len(words1), len(words2))
    # print("{0:0512b}".format(sol))
    best, _upper = find_bounds(words1, words2)

    starting_solution = (1 << max_lcs_length) -1
    best_solution = starting_solution*0
    # print("{0:0512b}".format(starting_solution))
    # print("{0:0512b}".format(best_solution))
    solution_index = -1
    tracker_index = -1

    # a solution is defined as [solution, index in solution, tracker that tracks this index with a letter in the other string, the upper bound of this solution]

    lifo_queue = Queue.LifoQueue()
    lifo_queue.put([starting_solution, solution_index, tracker_index, best,1])
    best = max(best -1,0)
    print("estimate of best is ", best)
    print("max length is ", max_lcs_length)
    print("--")
    logfile = open('log.txt','w')
    logfile.write("estimate of best is " + str(best)+"\n")
    logfile.write("max length is "+ str(max_lcs_length)+"\n")
    logfile.write("--------------------------------"+"\n")

    while not lifo_queue.empty():
        node = lifo_queue.get()
        # print(node+ "\n")
        if node[3] > best:
            logfile.write(str(get_solution(words1, words2, node[0])) + str(node) + "\n")
        else:
            logfile.write(" CUT "+str(get_solution(words1, words2, node[0])) + str(node) + " CUT\n")

        if node[3] > best and node[1] < max_lcs_length-1:
            node1, node2 = explore(node, words1, words2)
            if node1[3] > node2[3]:
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
            if node[1] == (max_lcs_length - 1):
                print("at end of tree")
            if node[3] > best and node[1] == (max_lcs_length - 1):
                print("New Best found", node)
                logfile.write("--------------------------------" + "\n")
                best = node[3]
                best_solution = node[0]



    solution = get_solution(words1, words2, best_solution)
    print("{0:016b}".format(best_solution))
    print(solution)
    logfile.close()
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