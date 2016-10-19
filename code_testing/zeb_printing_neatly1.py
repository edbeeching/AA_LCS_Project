
from __future__ import print_function
import numpy

def print_neatly(ListOfStrings, NumberOfLinesPerRow):

    ## Function to print neatly using most basic way

    line_counter = 0
    print("----------------")
    for string in ListOfStrings:
        line_counter += len(string) + 1
        if(line_counter > NumberOfLinesPerRow):
            print()
            line_counter = len(string) + 1

        print(string,end=" ")
    print("\n----------------")

    ## Computation of extras[i,j]
    n = len(ListOfStrings)
    extras = numpy.empty((n, n), dtype="int")


if __name__ == '__main__':
    ## run this following if this is the main program
    testString = ["This", "is", "a", "test", "string", "for", "printing", "neatly"]
    print_neatly(testString, 16)
