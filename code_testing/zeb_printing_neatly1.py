
from __future__ import print_function
import numpy
import sys

def compute_extras(i,j,listOfStrings, numberOfLinesPerRow):

    sum = numberOfLinesPerRow

    for string in listOfStrings[i:j+1]:
        sum -=len(string)
    sum-= (j-i)

    ##print(listOfStrings[i:j + 1]," = ", sum)

    return sum

def compute_line_cost(i, j, extras,n):
    if extras[i,j]<0:
        ##return sys.maxint
        return 10000
    if j+1 is n:
        return 0
    return extras[i,j]**3


def compute_cost(j,costs,line_cost):
    if j is 0:
        return line_cost[0,0], 0


    sum = 10000
    k = 0
    for i in range(0,j+1):
        if i is 0 :
            if line_cost[i,j] < sum:
                sum =  line_cost[i, j]
                k = i
        elif (costs[i - 1] + line_cost[i, j]) < sum:
            sum = costs[i - 1] + line_cost[i, j]
            k = i

    return sum, k

def print_neatly(listOfStrings, numberOfLinesPerRow):

    ## Function to print neatly using most basic way

    line_counter = 0
    print("----------------")
    for string in listOfStrings:
        line_counter += len(string) + 1
        if(line_counter > numberOfLinesPerRow):
            print()
            line_counter = len(string) + 1
        print(string,end=" ")
    print("\n----------------")

    ## Computation of extras[i,j]
    n = len(listOfStrings)
    extras = numpy.zeros((n, n), dtype="int32")
    for i in range(0,n):
        for j in range(i,min(n, i + numberOfLinesPerRow/2)):
            extras[i,j] = compute_extras(i, j, listOfStrings, numberOfLinesPerRow)
    ##print(extras)
    ## Computation of line costs
    line_cost = numpy.zeros((n, n), dtype="int32")
    line_cost[:] = 100000
    for i in range(0, n):
        for j in range(i, min(n, i + numberOfLinesPerRow / 2)):
            line_cost[i, j] = compute_line_cost(i, j, extras, n)
    print(line_cost)
    costs = numpy.zeros(n, dtype="int32")
    print(costs)
    para = numpy.zeros(n, dtype="int32")
    for j in range(0,n):
        costs[j], para[j]  = compute_cost(j, costs, line_cost)

    print(costs)
    print(para)



if __name__ == '__main__':
    ## run this following if this is the main program
    testString = ["This", "is", "a", "test", "string", "for", "printing", "neatly"]
    print_neatly(testString, 16)
