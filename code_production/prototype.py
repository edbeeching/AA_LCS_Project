
import os
import numpy
import re

#takes file as input, outputs list of words
def make_array(file1):
    X = []
    X.append(" ")     # to make indexing correct for algorthm (algorithm assumes base-1 indexing, Python is base-2
    file1 = open(file1)
    for word in file1.read().split():
        X.append(word)
    return X


#takes file as input, outputs list of lists (sentences)
def make_sentence_array(file1):
    sentences = []
    file1 = open(file1)
    for sentence in filter(None, re.split("[,.]+", file1.read())):
        new_sent = []
        new_sent.append(" ")     # to make indexing correct for algorthm (algorithm assumes base-1 indexing, Python is base-2
        for word in sentence.split():
            new_sent.append(word)
        sentences.append(new_sent)
    return sentences

#takes file as input, outputs list of words stripped of all punctuation 
#for use in sentence by sentence LCS
def make_compsentence_array(file1):
    words = []
    words.append(" ")       # to make indexing correct for algorthm (algorithm assumes base-1 indexing, Python is base-2
    file1 = open(file1)
    for sentence in filter(None, re.split("[,.]+", file1.read())):
        for word in sentence.split():
            words.append(word)
    return words

#classic dynamic progamming algorithm
def LCSclassic(X,Y):
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
    return LCS_List

#driver for LCS
def LCS(file1,file2,mode):
    X = make_array(file1)
    Y = make_array(file2)
    length = len(X) - 1
    if mode == "classic":
        LCSLIST = LCSclassic(X,Y)

    return length, len(LCSLIST), LCSLIST

#Driver for Sentence by sentence LCS
def LCS_Sentence(file1,file2, mode):
    X = make_sentence_array(file1)
    Y = make_compsentence_array(file2)
    totalLCS = []
    totalLCSlength = 0
    totalLength = 0
    for sentence in X:
        if mode == "classic":
            LCS_List = LCSclassic(sentence, Y)
        totalLength = totalLength + len(sentence) - 1
        totalLCSlength = totalLCSlength + len(LCS_List)
        for word in LCS_List:
            totalLCS.append(word)
    return totalLength, totalLCSlength, totalLCS


#uses b array to construct actual LCS list
#X is first text, m is length of X, n is length of Y (second text), S is list of LCS (empty at first function call)
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


#This function gets the LCS and ratio of every file in the corpus
#inputs are algorithm (only classic is implemented as of now 15/11)
#folder = corpus-20090418, corpus-adv_preprocessed, corpus-preprocessed, or corpus-swr_preprocessed
#whether to use sentence by sentence or not (sentence = False, True)
#outputs are one list containing all the LCS(alphabetical order by file name)
#and LCS ratio list (also alphabetical)
def getLCSdata(mode, folder, sentence):
    cwd = os.getcwd()
    parent = os.path.abspath(os.path.join(cwd, os.pardir))
    file_list = os.listdir('..\\' + folder)
    lengths = []
    ratios = []
    file_end = ""
    if folder == "corpus-20090418":
        file_end = ".txt"
    elif folder == "corpus-adv_preprocessed":
        file_end = "_adv_preprocessed.txt"
    elif folder == "corpus-preprocessed":
        file_end = "_preprocessed.txt"
    elif folder == "corpus-swr_preprocessed":
        file_end = "_swr_preprocessed.txt"
    if file_end == "":
        print "Invalid folder name"
        exit()
    for each in file_list:
        task = each[9]
        file1 = parent + "\\" + folder + "\\" + each
        file2 = parent + "\\" + folder + "\\orig_task" + task + file_end
        if sentence:
            Length, LCSlength, LCSLIST = LCS_Sentence(file1,file2,mode)
        else:
            Length, LCSlength, LCSLIST = LCS(file1,file2,mode) 
        lengths.append(LCSlength)
        ratios.append(float(LCSlength) / Length)
    return lengths[:-5], ratios[:-5]  #last 5 elements are LCS of original files vs. themselves
    
        

    
##########################################################################################
# Testing
if __name__ == "__main__":
   
    lengths, ratios = getLCSdata("classic","corpus-adv_preprocessed",True)
    for each in lengths:
        print each
    for each in ratios:
        print round(each,5)


    

    






