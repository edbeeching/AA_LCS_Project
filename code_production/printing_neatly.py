
from __future__ import print_function
import numpy
from operator import itemgetter
import sys
import random
import string


def _compute_extras(i, j, list_of_strings, lines_per_row):

    total = lines_per_row
    for string in list_of_strings[i:j+1]:
        total -= len(string)
    total -= (j-i)
    return total


def _compute_extras_dynamic(i, j, list_of_strings, lines_per_row, extrass):
    if i == j:
        return lines_per_row - len(list_of_strings[j])
    else:
        return extrass[i, j-1] - len(list_of_strings[j]) - 1


def _compute_line_cost(i, j, extras, n):

    if extras[i, j] < 0:
        # return sys.maxint This overflows in some cases, so better to use something smaller
        return 10000000
    if j+1 is n:
        return 0
    return extras[i, j]**3


def _compute_cost(j, costs, line_cost):
    if j is 0:
        return line_cost[0,0], 0

    tot = 10000000  # Best to avoid sys.maxint here as you get overflow later
    k = 0
    for i in range(0, j+1):
        if i is 0:
            if line_cost[i, j] < tot:
                tot = line_cost[i, j]
                k = i
        elif (costs[i - 1] + line_cost[i, j]) < tot:
            tot = costs[i - 1] + line_cost[i, j]
            k = i

    return tot, k


def print_neatly_greedy(list_of_strings, lines_per_row):
    # Function to print neatly using most basic way
    output = []
    line_counter = 0
    line_string = ""
    # print("----------------")
    for string in list_of_strings:
        line_counter += len(string) + 1
        if line_counter > lines_per_row+1:
            line_counter = len(string) + 1
            output.append(line_string[:-1])
            line_string = ""

        line_string += string
        line_string += " "
    output.append(line_string[:-1])

    return output


def print_neatly_dynamic(list_of_strings, lines_per_row):

    # The code below does printing neatly as per the definition in class

    # Computation of extras[i,j]
    n = len(list_of_strings)
    extras = numpy.zeros((n, n), dtype="int32")
    for i in range(0, n):
        for j in range(i, min(n, i + lines_per_row/2)):
            extras[i, j] = _compute_extras_dynamic(i, j, list_of_strings, lines_per_row, extras)
            # extras[i, j] = compute_extras(i, j, listOfStrings, numberOfLinesPerRow)

    # Computation of line costs
    line_cost = numpy.zeros((n, n), dtype="int32")
    line_cost[:] = 10000000
    for i in range(0, n):
        for j in range(i, min(n, i + lines_per_row / 2)):
            line_cost[i, j] = _compute_line_cost(i, j, extras, n)

    # Computation of best costs
    costs = numpy.zeros(n, dtype="int32")
    para = numpy.zeros(n, dtype="int32")
    for j in range(0,n):
        costs[j], para[j] = _compute_cost(j, costs, line_cost)

    # The word key contains the a map of which strings are on which row
    word_key = [len(list_of_strings)]
    val = para[n-1]
    word_key.insert(0, val)

    while val > 0:
        val = para[val-1]
        word_key.insert(0, val)

    output = []
    line_string = ""
    key_index = 0

    for i in range(0, len(list_of_strings)):
        if word_key[key_index+1] <= i:
            key_index += 1
            output.append(line_string[:-1])
            line_string = ""
        line_string += list_of_strings[i]
        line_string += " "
    output.append(line_string[:-1])
    return output

def find_num_words(list_of_strings, lines_per_row):
    #print("Find num words",list_of_strings)
    counter = 0
    index = 0
    while(index < len(list_of_strings)):
        counter += len(list_of_strings[index])
        if counter > lines_per_row:
            counter -= len(list_of_strings[index])
            break
        counter += 1
        index += 1
    return index

def print_neatly_recursive(list_of_strings, lines_per_row):
    result = []
    # Find max number of words for this row
    max_words_per_row = find_num_words(list_of_strings, lines_per_row)
    if max_words_per_row >= len(list_of_strings):
        return 0, [" ".join(list_of_strings)]
    # Iterate though options to find the best score
    best_score = 1000000000
    for i in range(1, max_words_per_row+1):
        subscore = 0
        for x in range(0, i):
            subscore += len(list_of_strings[x])
            subscore += 1

        subscore -= 1
        subscore = lines_per_row - subscore
        subscore = subscore * subscore * subscore

        score, res = print_neatly_recursive(list_of_strings[i:], lines_per_row)
        if score + subscore < best_score:
            result = [" ".join(list_of_strings[0:i])] + res
            best_score = score + subscore

    return best_score, result

def print_neatly_branch_and_bound(list_of_strings, lines_per_row, current_score, best_score):
    bound_threshold = 40

    result = []
    #print(list_of_strings,lines_per_row, current_score, best_score)
    max_words_per_row = find_num_words(list_of_strings, lines_per_row)
    if max_words_per_row >= len(list_of_strings):
        if current_score < best_score:
            best_score = current_score
        return 0, [" ".join(list_of_strings)]

    bound_list = []

    for i in range(max_words_per_row, 0, -1):
        subscore = 0
        for x in range(0, i):
            subscore += len(list_of_strings[x])
            subscore += 1
        subscore -= 1
        subscore = lines_per_row - subscore
        subscore = (subscore ** 3)

        bound = get_greedy_bound(list_of_strings[i:], lines_per_row)

        if current_score + bound + subscore < best_score + bound_threshold:
            #print("adding bound", [i, current_score +bound + subscore, subscore])
            bound_list.append([i, current_score +bound + subscore, subscore])
    #print("-------------------------------------")
    best = 1000000000
    best_i = -1
    #print("rec")
    for i, bound, subscore in sorted(bound_list, key=itemgetter(2)):
        if bound < best_score + bound_threshold:
            score, res = print_neatly_branch_and_bound(list_of_strings[i:], lines_per_row, current_score + subscore, best_score)

            if score <= best_score:
                result = res
                best = score + subscore
                best_i = i
    #print("best is ",best, [" ".join(list_of_strings[:best_i])] + result)
    return best, [" ".join(list_of_strings[:best_i])] + result

def get_greedy_bound(list_of_strings, lines_per_row):
    total_score = 0
    subscore = 0
    for line in print_neatly_greedy(list_of_strings, lines_per_row):
        subscore = lines_per_row - len(line)
        total_score += (subscore ** 3)

    return total_score - (subscore ** 3)

def generate_random_word(min_word_length, max_word_length):
    word_length = random.randint(min_word_length, max_word_length)
    word = ""

    for i in range(word_length):
        word += random.choice(string.ascii_uppercase)
    return word

def generate_random_word_list(num_words, min_word_length, max_word_length):

    word_list = []
    for i in range(num_words):
        word_list.append(generate_random_word(min_word_length, max_word_length))

    return word_list



if __name__ == '__main__':
    # run the following if this is the main program
    # There are a few test strings that can be compared.

    # print(generate_random_word_list(10,2,10))
    words = generate_random_word_list(10, 2, 10)
    words = ['TKSGHVLAJ', 'PK', 'XKEBDCKHHU', 'LWSU', 'MVZWQBD', 'CLJW', 'WRKAHNBZV', 'FKKHGDO']
    print(words)
    print("---------------------------------------------------")
    line_length = 15
    print("Recursive", print_neatly_recursive(words, line_length))

    greedy_estimate = get_greedy_bound(words, line_length)

    print("bnb", greedy_estimate)
    print("Branch and bound", print_neatly_branch_and_bound(words, line_length, 0, greedy_estimate + 1))

    print("Dynamic", print_neatly_dynamic(words, line_length))



    print("---------------------------------------------------")
    line_length = 15
    words = ["This", "is", "a", "test", "of", "strings"]
    #words = ["of", "strings"]
    print(find_num_words(["of", "strings"], line_length))
    print("Recursive", print_neatly_recursive(words, line_length))
    print("Dynamic", print_neatly_dynamic(words, line_length))

    print("Greedy", print_neatly_greedy(words, line_length))

    greedy_estimate = get_greedy_bound(words, line_length)
    greedy_estimate -1
    print("bnb", greedy_estimate)
    print("Branch and bound", print_neatly_branch_and_bound(words, line_length, 0, greedy_estimate+1))

    print("Sorting test")
    list1 = []
    list1.append([1, 120])
    list1.append([2, 70])
    list1.append([3, 40])
    list1.append([4, 10])
    list1.append([5, 20])

    print(list1)
    print(sorted(list1, key=itemgetter(0)))
    print(sorted(list1,  key=itemgetter(1)))






