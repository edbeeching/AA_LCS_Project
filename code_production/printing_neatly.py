"""
Created by Edward Beeching

This module implements the following printing neatly algorithms:
    1. print_neatly_greedy(list_of_strings, lines_per_row)
        This fills each line with as many lines as possible without consideration of the overall cost
        This approach is linear, but does not produce an optimal solution

    2. print_neatly_dynamic(list_of_strings, lines_per_row)
        This produces and optimal solution using a dynamic approach, the compute extras function has both a dynamic,
        and non-dynnamic version, and the line costs are only computed where appropriate.

    3. print_neatly_recursive(list_of_strings, lines_per_row)
        This enumerates every possible solution with a recursive approach, the solution returned is optimal
        but run-time is exponential

    4. print_neatly_branch_and_bound(list_of_strings, lines_per_row)
        This makes an initial estimate of the cost of a solution using the greedy approach, solutions are explored
        recursively and estimates of a bound are make with remaining words with a greedy approach, in order to cut
        solutions. Unfortunately the resulting solutions are always optimal.
    5. print_neatly_branch_and_bound2(list_of_strings, lines_per_row)

        This is a second branch and bound approach, the difference here is the greedy function is only used at the start
        in order to get an upper bound, solutions are the explored recursively and solutions are cut when the
        accumulated cost exceeds the greedy estimate. The result return by this algorithm is optimal.

"""
from __future__ import print_function
import numpy
from operator import itemgetter
import random
import string
import time


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
    # Function to find maximum number of words that cna fit on a line
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

def print_neatly_branch_and_bound2(list_of_strings, lines_per_row, current_score, best_score):
    result = []
    max_words_per_row = find_num_words(list_of_strings, lines_per_row)
    if max_words_per_row >= len(list_of_strings):
        return current_score, [" ".join(list_of_strings)]

    best = 1000000000
    for i in range(1, max_words_per_row+1):
        subscore = 0
        for x in range(0, i):
            subscore += len(list_of_strings[x])
            subscore += 1

        subscore -= 1
        subscore = lines_per_row - subscore
        subscore = subscore * subscore * subscore
        if subscore + current_score > best_score:
            #print("score is",i,subscore, subscore + current_score, "continuing", list_of_strings)
            continue

        score, res = print_neatly_branch_and_bound2(list_of_strings[i:], lines_per_row,current_score + subscore, best_score)
        if score < best_score:
            result = [" ".join(list_of_strings[0:i])] + res
            best = score
            best_score = score

    return best, result



def print_neatly_branch_and_bound(list_of_strings, lines_per_row, current_score, best_score):
    bound_threshold = 0

    result = []
    #print(list_of_strings,lines_per_row, current_score, best_score)
    max_words_per_row = find_num_words(list_of_strings, lines_per_row)
    if max_words_per_row >= len(list_of_strings):
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

            if score < best_score:
                best_score = score
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
    words = ['ODP', 'WPR', 'TKSGHVLAJ', 'PK', 'XKEBDCKHHU', 'LWSU', 'MVZWQBD', 'CLJW', 'WRKAHNBZV', 'FKKHGDO']




    print(words)
    print("---------------------------------------------------")
    line_length = 15
    print("Recursive", print_neatly_recursive(words, line_length))

    greedy_estimate = get_greedy_bound(words, line_length)

    print("bnb", greedy_estimate)
    print("Branch and bound", print_neatly_branch_and_bound(words, line_length, 0, greedy_estimate + 1))
    print("Branch and bound2", print_neatly_branch_and_bound2(words, line_length, 0, greedy_estimate + 1))

    print("Dynamic", print_neatly_dynamic(words, line_length))



    print("---------------------------------------------------")
    print("------ RUNTIME COMPARISON TESTS")

    #exit()

    num_tests = 40
    num_vals = 60
    time_dict_dyn = {}
    time_dict_rec = {}
    time_dict_bnb = {}
    time_dict_greed = {}
    for j in range(num_vals):
        time_dict_dyn[j] = 0
        time_dict_rec[j] = 0
        time_dict_bnb[j] = 0
        time_dict_greed[j] = 0

    for i in range(num_tests):
        print("Test", i)
        for j in range(2, num_vals):
            words = generate_random_word_list(j, 2, 10)
            start = time.time()
            print_neatly_dynamic(words, 20)
            time_dict_dyn[j] += time.time() - start

            # start = time.time()
            # print_neatly_recursive(words, 20)
            # time_dict_rec[j] += time.time() - start

            start = time.time()
            print_neatly_branch_and_bound2(words, line_length, 0, get_greedy_bound(words, line_length) + 1)
            time_dict_bnb[j] += time.time() - start

            start = time.time()
            print_neatly_greedy(words, 20)
            time_dict_greed[j] += time.time() - start

    print("Dynamic runtimes")
    for i in range(0, num_vals):
        print(i, time_dict_dyn.get(i)/40)
    print("---------------------------------------------------")

    # print("Recursive runtimes")
    # for i in range(0, num_vals):
    #     print(i, time_dict_rec.get(i)/40)
    # print("---------------------------------------------------")

    print("Branch and bound runtimes")
    for i in range(0, num_vals):
        print(i, time_dict_bnb.get(i)/40)
    print("---------------------------------------------------")

    print("Greedy runtimes")
    for i in range(0, num_vals):
        print(i, time_dict_greed.get(i)/40)
    print("---------------------------------------------------")




