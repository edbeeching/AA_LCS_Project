
from __future__ import print_function
import numpy
import sys

def compute_extras(i, j, listOfStrings, numberOfLinesPerRow):

    sum = numberOfLinesPerRow
    for string in listOfStrings[i:j+1]:
        sum -= len(string)
    sum -= (j-i)
    return sum

def compute_extras_dynamic(i, j, listOfStrings, numberOfLinesPerRow, extrass):
    if i == j:
        return numberOfLinesPerRow - len(listOfStrings[j])
    else:
        return extrass[i, j-1] - len(listOfStrings[j]) - 1


def compute_line_cost(i, j, extras, n):

    if extras[i,j]<0:
        # return sys.maxint This overflows in some cases, so better to use something smaller
        return 10000000
    if j+1 is n:
        return 0
    return extras[i,j]**3


def compute_extras_unit_test(listOfStrings, numberOfLinesPerRow):
    # line_counter = 0
    # print("----------------")
    # for string in listOfStrings:
    #     line_counter += len(string) + 1
    #     if (line_counter > numberOfLinesPerRow + 1):
    #         print()
    #         line_counter = len(string) + 1
    #     print(string, end=" ")
    # print("\n----------------")

    # The code below does printing neatly as per the definition in class

    # Computation of extras[i,j]
    n = len(listOfStrings)
    extras = numpy.zeros((n, n), dtype="int32")
    for i in range(0, n):
        for j in range(i, min(n, i + (numberOfLinesPerRow / 2))):
            extras[i, j] = compute_extras(i, j, listOfStrings, numberOfLinesPerRow)

    extras2 = numpy.zeros((n, n), dtype="int32")
    for i in range(0, n):
        for j in range(i, min(n, i + (numberOfLinesPerRow / 2))):
            extras2[i,j] = compute_extras_dynamic(i, j, listOfStrings, numberOfLinesPerRow, extras2)
    numpy.savetxt("extras.txt",extras,fmt='%10i',delimiter=',')
    numpy.savetxt("extras2.txt",extras2,fmt='%10i',  delimiter=',')
    print(extras)
    print()
    print(extras2)


def compute_cost(j, costs, line_cost):
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

def print_neatly_greedy(listOfStrings, numberOfLinesPerRow):
    # Function to print neatly using most basic way
    output = []
    line_counter = 0
    line_string = ""
    # print("----------------")
    for string in listOfStrings:
        line_counter += len(string) + 1
        if line_counter > numberOfLinesPerRow+1:
            # print()
            line_counter = len(string) + 1
            output.append(line_string[:-1])
            line_string = ""

        line_string += string
        line_string += " "
        # print(string, end=" ")
    output.append(line_string[:-1])
    # print("\n----------------")

    # print(output)

    return output

def print_neatly_dynamic(listOfStrings, numberOfLinesPerRow):



    # The code below does printing neatly as per the definition in class

    # Computation of extras[i,j]
    n = len(listOfStrings)
    extras = numpy.zeros((n, n), dtype="int32")
    for i in range(0, n):
        for j in range(i, min(n, i + numberOfLinesPerRow/2)):
            extras[i, j] = compute_extras_dynamic(i, j, listOfStrings, numberOfLinesPerRow, extras)
            # extras[i, j] = compute_extras(i, j, listOfStrings, numberOfLinesPerRow)

    # Computation of line costs
    line_cost = numpy.zeros((n, n), dtype="int32")
    line_cost[:] = 10000000
    for i in range(0, n):
        for j in range(i, min(n, i + numberOfLinesPerRow / 2)):
            line_cost[i, j] = compute_line_cost(i, j, extras, n)

    # Computation of best costs
    costs = numpy.zeros(n, dtype="int32")
    para = numpy.zeros(n, dtype="int32")
    for j in range(0,n):
        costs[j], para[j] = compute_cost(j, costs, line_cost)

    # The word key contains the a map of which strings are on which row
    word_key = [len(listOfStrings)]
    val = para[n-1]
    word_key.insert(0, val)

    while val > 0:
        val = para[val-1]
        word_key.insert(0, val)
    #print (word_key)
    #print("----------------")

    output = []
    line_string = ""
    key_index = 0

    for i in range(0, len(listOfStrings)):
        if word_key[key_index+1] <= i:
            # print()
            key_index += 1
            output.append(line_string[:-1])
            line_string = ""
        # print(listOfStrings[i], end=" ")
        line_string += listOfStrings[i]
        line_string += " "
     # print("\n----------------")
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
