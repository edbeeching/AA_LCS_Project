
#classic forward LCS dynamic prog implemented. naive user input just for testing purposes (should change). 
#assumes the two text files to compare are in/nested in the same directory as the script

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
    m = len(X)  #X[m-1] is the last element of X (since python is 0 indexed)
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
    file1 = raw_input("Please enter first file name with path from current working directory ")
    file2 = raw_input("Please enter second file name with path from current working directory ")

    cwd = os.getcwd()
    file1 = cwd + "\\" + file1
    file2 = cwd + "\\" + file2

    mode = raw_input("Please enter which LCS algorithm to use (classic, linear-space, or recursive): ")

    c, b, length, LCSLIST = LCS(file1,file2,mode)
    print "The longest common subsequence is " + str(length)
    print "Here is the LCS: "
    for x in LCSLIST:
        print x






