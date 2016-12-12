# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:30:37 2016

@author: jerem

This implements the plagiarism detector function, which returns true or false based on a combination of number of
and how many lcs words are grouped together in each sentence.
"""
import math
def plagiarised_sentences(lcs_text, corpus_text, treshold):
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

def score(self, lcs_text, corpus_text):
    def same_as(word1, word2):
        word1 = word1.replace(".", "")
        word1 = word1.replace(",", "")
        word2 = word2.replace(".", "")
        word2 = word2.replace(",", "")
        return word1 == word2

    index = 0
    add = False
    score = 0
    side_by_side = 1
    for word in corpus_text.split():

        if index < len(lcs_text) and same_as(word, lcs_text[index]):
            index += 1
            if add == False:
                add = True
                side_by_side = 1
            else:
                side_by_side += 1
        else:
            if add == True:
                add = False
                score += (side_by_side * side_by_side)
    return score

def is_plagisised(lcs_text, corpus_text, threshold):
    print("Computing plagiarism score")
    percentage_copied, number_sentences_corpus, copied_sentence = plagiarised_sentences(lcs_text, corpus_text, threshold)

    word_score = math.sqrt(score(lcs_text, corpus_text))
    percent_threshold = 20
    group_score_threshold = 0.2

    threshold_sum = (percent_threshold / 200) * (group_score_threshold / 2)

    return ((percentage_copied/100)*word_score > threshold_sum)


#Call function
#plagiarism(LCSLIST,corpus_text,70) #70 is the treshold for plagiarism