# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:30:08 2016
@author: jeremie BLANCHARD
"""


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

    
def LCS_linear_space(file1,file2):
    X = make_array(file1)
    Y = make_array(file2)
    length_X = len(X)
    length_Y = len(Y)
    
    b = numpy.empty((length_X,length_Y), dtype = "str")
    c = numpy.empty((length_X,length_Y), dtype = "int")

    for i in range(1,length_X):
        c[i,0]= 0
        for j in range(1,length_X):
            if (X[i]==Y[j]):
                c[i,j] = c[i-1,j-1] + 1
                b[i,j] = "d"    #for diagonal
            elif (c[i-1,j] >= c[i,j-1]):
                c[i,j] = c[i-1,j]
                b[i,j] = "u"    #for up
            else:
                c[i,j] = c[i,j-1]
                b[i,j] = "l"    #for left
        for j in range(0,length_X):
            c[0,j] = c[1,j]
    length = c[length_X-1,length_Y-1]
    #LCS_List = LCS_list(b,X,length_X-1,length_Y-1,[])
    return c, b, length#, LCS_List
    

#driver for LCS
def LCS(file1,file2,mode):
    if mode =="linear-space":
        c, b, length = LCS_linear_space(file1,file2)
        return c, b, length

    


##########################################################################################
# Should change this part later (put together for testing purposes)
file1 = input("Please enter first file name with path from current working directory ")
file2 = input("Please enter second file name with path from current working directory ")

cwd = os.getcwd()
file1 = cwd + "\\" + file1
file2 = cwd + "\\" + file2

mode = input("Please enter which LCS algorithm to use (classic, linear-space, or recursive): ")

c, b, length = LCS(file1,file2,mode)
print ("The longest common subsequence is " + str(length))