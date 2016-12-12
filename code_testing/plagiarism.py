# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:30:37 2016

@author: jerem
"""

def plagiarism(lcs_text,corpus_text,treshold):
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
    
    for sentence in corpus_text.split("."):
        if length_sentence != 0:
            percentage_copied_sentence = ((len(copied_word_in_sentence)*100)/length_sentence)
            #print("Length sentence = ")
            #print(length_sentence)
            #print("copied_word_in_sentence= ")
            #print(copied_word_in_sentence)
            if percentage_copied_sentence >=treshold:
                copied_sentence +=1
        copied_word_in_sentence = []
        length_sentence = 0
        number_sentences_corpus += 1
        for word in sentence.split():
            if index < len(lcs_text) and same_as(word, lcs_text[index]):
                #print("passage1")
                copied_word_in_sentence.append(word)
                index += 1
                length_sentence+=1
            else:
                #print("passage3")
                length_sentence += 1
        
    percentage_copied = ((copied_sentence *100)/number_sentences_corpus)
    print(percentage_copied)
    print(copied_sentence)
    print(number_sentences_corpus)
    return percentage_copied, number_sentences_corpus,copied_sentence
    
#Call function
#plagiarism(LCSLIST,corpus_text,70) #70 is the treshold for plagiarism
