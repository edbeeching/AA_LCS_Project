# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:30:37 2016

@author: jerem

This implements the plagiarism detector function, which returns true or false based on a combination of number of
and how many lcs words are grouped together in each sentence.
"""
import math
import re


def make_compsentence_array(text1):
    words = []
    words.append(" ")       # to make indexing correct for algorithm (algorithm assumes base-1 indexing, Python is base-0

    for sentence in filter(None, re.split("[,.]+", text1)):
        for word in sentence.split():
            words.append(word)
    return words

def plagiarised_sentences(lcs_text, corpus_text, treshold=70.0):
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

    corpus_text.replace("."," .")    
    
    for sentence in corpus_text.split(". "):
        if length_sentence != 0:
            percentage_copied_sentence = ((len(copied_word_in_sentence)*100)/length_sentence)
            if percentage_copied_sentence >=treshold:
                copied_sentence +=1
        copied_word_in_sentence = []
        length_sentence = 0
        number_sentences_corpus += 1
        for word in sentence.split():
            if index < len(lcs_text) and same_as(word, lcs_text[index]):
                copied_word_in_sentence.append(word)
                index += 1
                length_sentence+=1
            else:
                length_sentence += 1
        
    percentage_copied = ((copied_sentence *100)/number_sentences_corpus)
    return percentage_copied, number_sentences_corpus,copied_sentence

def score(lcs_text, corpus_text):
    def same_as(word1, word2):
        word1 = word1.replace(".", "")
        word1 = word1.replace(",", "")
        word2 = word2.replace(".", "")
        word2 = word2.replace(",", "")
        return word1 == word2

    corpus_text = make_compsentence_array(corpus_text)

    if len(lcs_text) == len(corpus_text)-1:
        return 1


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
    return math.sqrt(float(score) / (len(corpus_text) * len(corpus_text)))

def is_plagisised(lcs_text, corpus_text, threshold=70.0):

    percentage_copied, number_sentences_corpus, copied_sentence = plagiarised_sentences(lcs_text, corpus_text, threshold)

    word_score = score(lcs_text, corpus_text)
    percent_threshold = 20.0
    group_score_threshold = 0.2

    threshold_sum = (percent_threshold / 200.0) + (group_score_threshold / 2.0)
    print(threshold_sum, percentage_copied, word_score)

    return (percentage_copied/100.0) + word_score > threshold_sum


#Call function
#plagiarism(LCSLIST,corpus_text,70) #70 is the treshold for plagiarism