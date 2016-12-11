# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:30:37 2016

@author: jerem
"""

def plagiarism(lcs_text,corpus_text,treshold):
    def same_as(word1,word2):
         word1 = word1.replace(",","")
         word2 = word2.replace(",","")
         return word1 == word2
    
    index = 0
    length_sentence = 0
    number_sentences_corpus= 0
    copied_word_in_sentence = []
    copied_sentence = 0

    for word in corpus_text.split():
        if index < len(lcs_text) and same_as(word, lcs_text[index]) and (word != "." or lcs_text[index] != "."):
            length_sentence += 1
            copied_word_in_sentence.append(word)
            index += 1
        elif index < len(lcs_text) and same_as(word, lcs_text[index]) and (word == "." or lcs_text[index] == ".") :
            number_sentences_corpus += 1
            percentage_copied_sentence = ((len(copied_word_in_sentence)*100)/length_sentence)
            if percentage_copied_sentence >=treshold:
                copied_sentence +=1
            length_sentence = 0
            copied_word_in_sentence = []
        else:
            length_sentence += 1
    
    percentage_copied = ((copied_sentence *100)/number_sentences_corpus)
    print(percentage_copied)
    return percentage_copied
    
#Call function
#plagiarism(LCSLIST,corpus_text,70) #70 is the treshold for plagiarism