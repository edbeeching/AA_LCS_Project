# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 11:14:33 2016

@author: jerem
"""
import random
import string
import time
import os
import numpy
import re
import math

#takes file as input, outputs list of words
def make_array(file1):
    X = []
    X.append(" ")     # to make indexing correct for algorthm (algorithm assumes base-1 indexing, Python is base-2
    file1 = open(file1)
    for word in file1.read().split():
        X.append(word)
    return X

def make_array_nostopwords(file1, stopwords):
    X = []
    X.append(" ")     # to make indexing correct for algorithm (algorithm assumes base-1 indexing, Python is base-0
    file1 = open(file1)
    for word in file1.read().split():
        if (not(word in stopwords)):
            X.append(word)
    return X

#takes file as input, outputs list of lists (sentences)
def make_sentence_array(file1):
    sentences = []
    file1 = open(file1)
    fin_sent = False        #boolean for special case of acronyms (ex: "i.e." or "N.B.A.")
    for sentence in filter(None, re.split("[,.]+", file1.read())):
        if (len(sentence) == 1):    #if in the middle of an acronym
            sentences[len(sentences)-1].append(sentence)
            fin_sent = True
        else:
            if fin_sent:            #if last period was an acronym and not the end of a sentence
                for word in sentence.split():
                    sentences[len(sentences)-1].append(word)
            else:
                new_sent = []
                new_sent.append(" ")     # to make indexing correct for algorithm (algorithm assumes base-1 indexing, Python is base-0
                for word in sentence.split():
                    new_sent.append(word)
                sentences.append(new_sent)
            fin_sent = False
    return sentences

#takes file as input, outputs list of words stripped of all punctuation 
#for use in sentence by sentence LCS
def make_compsentence_array(file1):
    words = []
    words.append(" ")       # to make indexing correct for algorithm (algorithm assumes base-1 indexing, Python is base-0
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

#Divide and conquer with space efficiency
def LCS_DivideConquer(X,Y):
    length_X = len(X)
    length_Y = len(Y)
    if ((length_X - 1)*(length_Y-1) == 0): #if one of the texts is empty
        return []    
    elif (length_X - 1 <= 2) or (length_Y - 1 <= 2): 
        LCS = LCSclassic(X,Y)
        return LCS
    else:
        breakpoint = int(math.floor(length_Y / 2))
        length, c = LCS_linear_space(X, Y[0:breakpoint+1])
        Y2 = Y[breakpoint:]
        Y2.insert(0," ") #lining indices up for algorithm
        length2, g  = LCS_linear_space_backward(X,Y2)
        q = get_max_index(c, g, X, Y[breakpoint])
        X2 = X[q+1:]
        X2.insert(0," ")
        X = X[0:q+1]
        Y2 = Y[breakpoint+1:]
        Y2.insert(0," ")
        Y = Y[0:breakpoint+1]        
        LCSL = LCS_DivideConquer(X,Y)
        LCSR = LCS_DivideConquer(X2,Y2)
        return LCSL + LCSR

#function to return optimal index for splitting during divide and conquer                             
def get_max_index(c, g, X, word):
    max = 0
    index = 0
    r = len(c)
    for i in range(0,r):
        if (c[i] + g[i]) > max:
            max = c[i] + g[i]
            index = i
        elif (c[i] + g[i] == max) and (X[i] == word):
            index = i
                   
    return index
    
def LCSclassic_backward(file1,file2):#This is the LCS classic in Backward
    X = make_array(file1)
    Y = make_array(file2)
    length_X = len(X)
    length_Y = len(Y)
    
    b = numpy.empty((length_X,length_Y), dtype = "str")
    c = numpy.empty((length_X,length_Y), dtype = "int")
    
    for i in range(length_X-2,-1,-1):
        c[length_X-1,0]= 0
        for j in range(length_Y-2,-1,-1):
            if (i==length_X-2 and j==length_Y-2):
                c[i,j] = 1
                b[i,j] = "d"    #for diagonal
            elif (i<length_X-2 and j<length_Y-2 and X[i+1]==Y[j+1]):
                c[i,j] = c[i+1,j+1]+1
                b[i,j] = "u"    #for up
            else:
                c[i,j] = max(c[i+1,j],c[i,j+1])
                b[i,j] = "l"    #for up
    length = c[0,0]
    #LCS_List = LCS_list(b,X,length_X-1,length_Y-1,[])
    return c, b, length #, LCS_List

    
def LCS_linear_space_backward(X,Y): #This is the backward LCS in linear space which allow 
#to perform a LCS in a smaller space and time. Matrix of [2,length_Y]
    length_X = len(X)
    length_Y = len(Y)
    
    c = numpy.zeros((2,length_Y), dtype = "int")
    column = []
    column.append(0)
    for i in range(length_X-2,-1,-1):
        for j in range(length_Y-2,-1,-1):
            if (i<=length_X-2 and j<=length_Y-2 and X[i+1]==Y[j+1]):
                c[1,j] = c[0,j+1]+1
            else:
                c[1,j] = max(c[0,j],c[1,j+1])
        for j in range(0,length_Y):
            c[0,j] = c[1,j]
        column.insert(0,c[1,0])
    
    length = c[1,0]
    return length, column

def LCS_linear_space(X,Y): #This is the regular LCS in linear space which allow 
#to perform a LCS in a smaller space and time. Matrix of [2,length_Y]
    length_X = len(X)
    length_Y = len(Y)
    c = numpy.zeros((2,length_Y), dtype = "int")
    column = []
    column.append(0)
    for i in range(1,length_X):
        c[1,0]= 0
        for j in range(1,length_Y):
            if (X[i]==Y[j]):
                c[1,j] = c[0,j-1] + 1
            elif (c[1,j-1]<=c[0,j]):
                c[1,j] = c[0,j]
            else:
                c[1,j] = c[1,j-1]
        for j in range(0,length_Y):
            c[0,j] = c[1,j]
        column.append(c[1,length_Y - 1])
        
    length = c[1,length_Y-1]
    return length, column

#driver for LCS
def LCS(file1,file2,mode):
    X = make_array(file1)
    Y = make_array(file2)
    length = len(X) - 1
    if mode == "classic":
        LCSLIST = LCSclassic(X,Y)
    elif mode == "DC":
        LCSLIST = LCS_DivideConquer(X,Y)
    return length, len(LCSLIST), LCSLIST

#driver for LCS without stop words
def LCS_nostops(file1,file2,mode):
    cwd = os.getcwd()
    parent = os.path.abspath(os.path.join(cwd, os.pardir))
    stops = make_array(parent + "\\text_preprocessing\\LongListStopWords.txt")
    X = make_array_nostopwords(file1, stops)
    Y = make_array_nostopwords(file2, stops)
    length = len(X) - 1
    if mode == "classic":
        LCSLIST = LCSclassic(X,Y)
    elif mode == "DC":
        LCSLIST = LCS_DivideConquer(X,Y)
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
        elif mode == "DC":
            LCS_List = LCS_DivideConquer(sentence,Y)
        totalLength = totalLength + len(sentence) - 1
        totalLCSlength = totalLCSlength + len(LCS_List)
        for word in LCS_List:
            totalLCS.append(word)
    return totalLength, totalLCSlength, totalLCS


#This function gets the LCS and ratio of every file in the corpus
#inputs are algorithm (mode)
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
    scores = []
    for each in file_list:
        task = each[9]
        file_end = each[10:]
        file1 = parent + "\\" + folder + "\\" + each
        file2 = parent + "\\" + folder + "\\orig_task" + task + file_end
        if sentence:
            Length, LCSlength, LCSLIST = LCS_Sentence(file1,file2,mode)
        else:
            Length, LCSlength, LCSLIST = LCS(file1,file2,mode) 
        lengths.append(LCSlength)
        ratios.append(float(LCSlength) / Length)
        percent, numsent, copysent = plagiarism1(LCSLIST, file1, 70)
        scores.append(percent)
    return lengths[:-5], ratios[:-5], scores[:-5] #last 5 elements are LCS of original files vs. themselves
    
        
def generate_random_list(length):

    words = [None]*length
    for i in range(length):
        words[i] = (random.choice(string.ascii_uppercase))

    return words


#copy of sentence plagarism threshold function
#used to gather data on the corpus when testing
def plagiarism1(lcs_text,corpus_text,treshold):
    def same_as(word1,word2):
         word1 = word1.replace(",","")
         word1 = word1.replace(".","")
         word2 = word2.replace(",","")
         word2 = word2.replace(".","")
         return word1 == word2

    index = 0
    length_sentence = 0
    number_sentences_corpus= -1
    copied_word_in_sentence = []
    copied_sentence = 0

    corpus_text = make_sentence_array(corpus_text)
    
    for sentence in corpus_text:
        if length_sentence != 0:
            percentage_copied_sentence = ((len(copied_word_in_sentence)*100)/length_sentence)
            if percentage_copied_sentence >=treshold:
                copied_sentence +=1
        copied_word_in_sentence = []
        length_sentence = 0
        number_sentences_corpus += 1
        for word in sentence:
            if index < len(lcs_text) and same_as(word, lcs_text[index]):
                #print("passage1")
                copied_word_in_sentence.append(word)
                index += 1
                length_sentence+=1
            else:
                #print("passage3")
                length_sentence += 1
        
    percentage_copied = ((copied_sentence *100)/number_sentences_corpus)
    return percentage_copied, number_sentences_corpus,copied_sentence

#copy of the word grouping plagarism score function
#used for gathering data on the corpus for testing
def scoretest(lcs_text, corpus_text):
    def same_as(word1, word2):
        word1 = word1.replace(".", "")
        word1 = word1.replace(",", "")
        word2 = word2.replace(".", "")
        word2 = word2.replace(",", "")
        return word1 == word2

    if len(lcs_text) == len(corpus_text):
        return 1
    
    corpus_text = make_compsentence_array(corpus_text)
    index = 0
    add = False
    score = 0
    side_by_side = 1
    for word in corpus_text:

        if index < len(lcs_text) and same_as(word, lcs_text[index]):
            # bold_text.append("<b>" + word + "</b>")
            index += 1
            if (add == False):
                add = True
                side_by_side = 1
            else:
                side_by_side += 1
        else:
            if (add == True):
                add = False
                score += (side_by_side * side_by_side)
            # bold_text.append(word)
    return float(score) / (len(corpus_text)*len(corpus_text))
##########################################################################################
# Testing
if __name__ == "__main__":
##    cwd = os.getcwd()
##    file1 = cwd + "\\dummy_file.txt"
##    sentences = make_sentence_array(file1)
##    for sentence in sentences:
##        print sentence

    lengths, ratios, scores = getLCSdata("classic","corpus-adv_preprocessed",False)
##    for each in lengths:
##        print each
##    for each in ratios:
##        print round(each,5)
    for each in scores:
        print each
##   
##    print("Runtime comparisons")
##    time_dict_rec = {}
##    for i in range(0, 9):
##        time_dict_rec[i] = 0
##        for _ in range(0, 40):
##            list1 = generate_random_list(int(math.pow(2, i+1)))
##            list1.insert(0," ")
##            list2 = generate_random_list(int(math.pow(2, i+1)))
##            list2.insert(0," ")
##            start = time.time()
##            lcs = LCS_DivideConquer(list1, list2)
##            time_dict_rec[i] += time.time() - start
##
##    for i in range(0, 9):
##        print time_dict_rec.get(i) / 40
##
##    time_dict = {}
##    for i in range(0, 9):
##        time_dict[i] = 0
##        for _ in range(0, 40):
##            list1 = generate_random_list(int(math.pow(2, i+1)))
##            list1.insert(0," ")
##            list2 = generate_random_list(int(math.pow(2, i+1)))
##            list2.insert(0," ")
##            start = time.time()
##            lcs = LCSclassic(list1, list2)
##            time_dict[i] += time.time() - start
##    for i in range(0, 9):
##        print time_dict.get(i) / 40
##    



    
