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

    
def LCS_linear_space_backward(file1,file2):
    X = make_array(file1)
    Y = make_array(file2)
    length_X = len(X)
    length_Y = len(Y)
    
    b = numpy.empty((2,length_Y), dtype = "str")
    c = numpy.empty((2,length_Y), dtype = "int")

    for i in range(length_X-2,-1,-1):
        c[1,0]= 0
        for j in range(length_Y-2,-1,-1):
            if (i==length_X-2 and j==length_Y-2):
                c[1,j] = 1
                print ("Passage 1")
            elif (i<length_X-2 and j<length_Y-2 and X[i+1]==Y[j+1]):
                c[1,j] = c[1,j+1]+1
                print ("Passage 2")
            else:
                c[1,j] = max(c[0,j],c[1,j+1])
                print ("Passage 3")
        for j in range(0,length_Y):
            c[0,j] = c[1,j]               
                
    length = c[0,0]
    #LCS_List = LCS_list(b,X,length_X-1,length_Y-1,[])
    return c, b, length#, LCS_List
    
#Retournez tous les indices ( De bas droit à haut gauche)
    
#driver for LCS
def LCS(file1,file2,mode):
    if mode =="lsb":
        c, b, length = LCS_linear_space_backward(file1,file2)
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