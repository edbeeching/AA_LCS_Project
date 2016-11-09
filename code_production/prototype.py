
#classic forward LCS dynamic prog implemented. naive user input just for testing purposes (should change). 

import os
import numpy

#takes file as input, outputs array of words
def make_array(file1):
    X = []
    X.append(" ")    #python is 0 indexed, and we want first element to start at X[1]
    file1 = open(file1)
    for word in file1.read().split():
        X.append(word)
    return X

#classic dynamic progamming algorithm
def LCSclassic(file1,file2):
    X = make_array(file1)
    Y = make_array(file2)
    m = len(X) #X[m-1] is the last element of X (since python is 0 indexed)
    n = len(Y)
    b = numpy.empty((m,n), dtype = "str")
    c = numpy.empty((m,n), dtype = "int")
    for i in range(0,m):
        c[i,0] = 0
    for j in range(1,n):
        c[0,j] = 0
    for i in range(1,m):
        for j in range(1,n):
            if (X[i]==Y[j]):
                c[i,j] = c[i-1,j-1] + 1
                b[i,j] = "d"    #for diagonal
            elif (c[i-1,j] >= c[i,j-1]):
                c[i,j] = c[i-1,j]
                b[i,j] = "u"    #for up
            else:
                c[i,j] = c[i,j-1]
                b[i,j] = "l"    #for left
    length = c[m-1,n-1]
    LCS_List = LCS_list(b,X,m-1,n-1,[])
    return c, b, length, LCS_List
    
#uses b array to construct actual LCS list
#X is first text, m is length of X, n is length of Y, S is list of LCS
def LCS_list(b,X,m,n,S):
    if ((m == 0)or(n==0)):
        return S
    if (b[m,n] == "d"):
        S = LCS_list(b,X,m-1,n-1,S)
        S.append(X[m])
        return S
    elif (b[m,n] == "u"):
        return LCS_list(b,X,m-1,n,S)
    else:
        return LCS_list(b,X,m,n-1,S)

#driver for LCS
def LCS(file1,file2,mode):
    if mode == "classic":
        c, b, length, LCSLIST = LCSclassic(file1,file2)

    return c, b, length, LCSLIST


##########################################################################################
# Should change this part later (put together for testing purposes)
if __name__ == "__main__":


    #########################################################
    ## Script to get LCS data on corpus w/ advanced preprocessing
    mode = "classic"
    cwd = os.getcwd()
    parent = os.path.abspath(os.path.join(cwd, os.pardir))
    file_list = os.listdir('..\\corpus-adv_preprocessed')
    lengths = []
    ratios = []

    
    for each in file_list:
        task = each[9]
        file1 = parent + "\\corpus-adv_preprocessed\\" + each
        file2 = parent + "\\corpus-adv_preprocessed\\orig_task" + task + "_adv_preprocessed.txt"
        c, b, length, LCSLIST = LCS(file1,file2,mode)
        totallength = c.shape[0] - 1
        lengths.append(length)
        ratios.append(float(length) / totallength)

    for each in lengths:
        print each
    for each in ratios:
        print round(each,5)
        




    
##    preprocess = raw_input("Press y for preprocessed text or n for not preprocessed text ")   
##            
##    group = raw_input("Please enter the group ")
##    person = raw_input("Please enter the person ")
##    task = raw_input("Please enter the task ")
##
##    cwd = os.getcwd()
##    if preprocess == "n":
##        file1 = cwd + "\\..\\corpus-20090418\\g" + str(group) + "p" + str(person) + "_task" + str(task) + ".txt"
##        file2 = cwd + "\\..\\corpus-20090418\\orig_task" + str(task) + ".txt"
##    else:
##        file1 = cwd + "\\..\\corpus-preprocessed\\g" + str(group) + "p" + str(person) + "_task" + str(task) + "preprocessed.txt"
##        file2 = cwd + "\\..\\corpus-preprocessed\\orig_task" + str(task) + "corpus-preprocessed.txt"
##
##    mode = raw_input("Please enter which LCS algorithm to use (classic, linear-space, or recursive): ")
##
##    c, b, length, LCSLIST = LCS(file1,file2,mode)
##    print "The longest common subsequence is " + str(length)
    






