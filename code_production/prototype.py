
#classic forward LCS dynamic prog implemented. naive user input just for testing purposes (should change). 

import os
import numpy
import re

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
    LCSlength = c[m-1,n-1]
    LCS_List = LCS_list(b,X,m-1,n-1,[])
    return c.shape[0], c, b, LCSlength, LCS_List

#takes file as input, outputs list of arrays (sentences)
def make_sentence_array(file1):
    sentences = []
    file1 = open(file1)
    for sentence in filter(None, re.split("[,.]+", file1.read())):
        new_sent = []
        new_sent.append(" ")
        for word in sentence.split():
            new_sent.append(word)
        sentences.append(new_sent)
    return sentences

#takes file as input, outputs list of words stripped of all punctuation 
#for use in sentence by sentence LCS
def make_compsentence_array(file1):
    words = []
    words.append(" ")
    file1 = open(file1)
    for sentence in filter(None, re.split("[,.]+", file1.read())):
        for word in sentence.split():
            words.append(word)
    return words

#classic dynamic progamming algorithm done sentence by sentence
def LCS_SentenceDP(file1,file2):
    X = make_sentence_array(file1)
    Y = make_compsentence_array(file2)
    totalLCS = []
    totalLCSlength = 0
    totalLength = 0
    for sentence in X:
        m = len(sentence)
        totalLength = totalLength + (m-1) #m - 1 because of empty string at beginning of each array
        n = len(Y)
        b = numpy.empty((m,n), dtype = "str")
        c = numpy.empty((m,n), dtype = "int")
        for i in range(0,m):
            c[i,0] = 0
        for j in range(1,n):
            c[0,j] = 0
        for i in range(1,m):
            for j in range(1,n):
                if (sentence[i]==Y[j]):
                    c[i,j] = c[i-1,j-1] + 1
                    b[i,j] = "d"    #for diagonal
                elif (c[i-1,j] >= c[i,j-1]):
                    c[i,j] = c[i-1,j]
                    b[i,j] = "u"    #for up
                else:
                    c[i,j] = c[i,j-1]
                    b[i,j] = "l"    #for left
        LCSlength = c[m-1,n-1]
        LCS_List = LCS_list(b,sentence,m-1,n-1,[])
        totalLCSlength = totalLCSlength + LCSlength
        for word in LCS_List:
            totalLCS.append(word)
        
    
    return totalLength, c, b, totalLCSlength, totalLCS


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
        length, c, b, lengthLCS, LCSLIST = LCSclassic(file1,file2)

    return length, c, b, lengthLCS, LCSLIST


##########################################################################################
# Should change this part later (put together for testing purposes)
if __name__ == "__main__":

##    mode = "classic"
##    
##    file1 = "C:\\Users\\Joe\\AA_LCS_Project\\corpus-20090418\\g0pA_taska.txt"
##    file2 = "C:\\Users\\Joe\\AA_LCS_Project\\corpus-20090418\\orig_taska.txt"
##    '''
##    file1 = "C:\\Users\\Joe\\Documents\\Programming\\Mixcraft_math\\a.txt"
##    file2 = "C:\\Users\\Joe\\Documents\\Programming\\Mixcraft_math\\b.txt"
##    '''
##    c, b, length, LCSLIST = LCS_SentenceDP(file1,file2)
##    print length
##    print LCSLIST
##    c, b, length, LCSLIST = LCS(file1,file2,mode)
##    print length
##    print LCSLIST

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
        Length, c, b, LCSlength, LCSLIST = LCS_SentenceDP(file1,file2)
        lengths.append(LCSlength)
        ratios.append(float(LCSlength) / Length)

    for each in lengths:
        print each
    for each in ratios:
        print round(each,5)
        




    

    






