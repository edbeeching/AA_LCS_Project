
from __future__ import print_function
import numpy
import sys


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


if __name__ == '__main__':
    # run the following if this is the main program
    # There are a few test strings that can be compared.

    test_file = open('../corpus-20090418/orig_taska.txt')
    testString3 = []
    for word in test_file.read().split():
        testString3.append(word)
    line = print_neatly_dynamic(testString3, 30)
    print(line)
    # Add way to include paragraphs in printing neatly
