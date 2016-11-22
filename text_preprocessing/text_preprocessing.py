# coding=utf-8
import os
import platform
import re
def read_file(path):
    file_object = open(path)
    file_string = file_object.read()
    file_object.close()
    return file_string

def write_file(file, path):
    file_object = open(path, 'w')
    file_object.write(file)
    file_object.close()
    return
def preprocessing_file(file):
    file = file.replace('‘', '\'')
    file = file.replace('’', '\'')
    file = file.replace('“', '\"')
    file = file.replace('”', '\"')
    file = file.replace('\n\n', '\n')
    file = file.replace('  ', ' ')

    preprocessed_file = file
    return preprocessed_file
def adv_preprocessing_file(file):

    # removing enumerated lists:
    file = re.sub(r'^\s*\d+\.?\s*','\n',file,flags=re.MULTILINE)

    # removing all non-ascii characters:
    file = re.sub(r'[^\x00-\x7F]+',' ', file)

    file = file.lower()
    file = file.replace('‘', '\'')
    file = file.replace('’', '\'')
    file = file.replace('“', '\"')
    file = file.replace('”', '\"')
    file = file.replace('"', '\"')
    file = file.replace("'", '\'')
    file = file.replace('\n\n', '\n')
    file = file.replace('\t', '')
    file = file.replace('  ', ' ')
    file = file.replace('\'', '')
    file = file.replace('\"', '')
    file = file.replace('/', '')
    file = file.replace(';', '')
    file = file.replace('(', '')
    file = file.replace(')', '')
    file = file.replace('-', ' ')
    file = file.replace('+', ' ')

    preprocessed_file =file
    return preprocessed_file

def swr_preprocessing_file(file):
    file = adv_preprocessing_file(file)
    StopWords = read_file("./LongListStopWords.txt").split()
    for stopWord in StopWords:
        file = file.replace(' '+stopWord+',', ',')
        file = file.replace(' '+stopWord+'.', '.')
        file = file.replace(' '+stopWord+' ', ' ')

    file=' '.join(file.split())
    return file

def WO_preprocessing_file(file):
    file = adv_preprocessing_file(file)
    Sentence_List= file.split('.')
    file_Sorted=""
    for Sentence in Sentence_List:
        word_list = Sentence.split(' ')
        word_list.sort()
        sorted_setence = ' '.join(word_list)
        file_Sorted += sorted_setence+'.'
    return file_Sorted

def wrinting_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep)-2] = 'corpus-preprocessed'
    pathsep[len(pathsep)-1] = pathsep[len(pathsep)-1].replace('.txt', '_preprocessed.txt')
    filepath_preprocessed = os.path.join('/'.join(pathsep))
    directory = ".." + os.path.sep + pathsep[len(pathsep) - 2]
    if not os.path.exists(directory):
        os.makedirs(directory)
    write_file(preprocessing_file(file), filepath_preprocessed)
    return

def wrinting_adv_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep)-2] = 'corpus-adv_preprocessed'
    pathsep[len(pathsep)-1] = pathsep[len(pathsep)-1].replace('.txt', '_adv_preprocessed.txt')
    filepath_preprocessed = os.path.join('/'.join(pathsep))
    directory = ".." + os.path.sep + pathsep[len(pathsep) - 2]
    if not os.path.exists(directory):
        os.makedirs(directory)
    write_file(adv_preprocessing_file(file), filepath_preprocessed)
    return

def wrinting_swr_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep) - 2] = 'corpus-swr_preprocessed'
    pathsep[len(pathsep) - 1] = pathsep[len(pathsep) - 1].replace('.txt', '_swr_preprocessed.txt')
    filepath_preprocessed = os.path.join('/'.join(pathsep))
    directory = ".."+os.path.sep+pathsep[len(pathsep) - 2]+os.path.sep
    if not os.path.exists(directory):
        os.makedirs(directory)
    write_file(swr_preprocessing_file(file), filepath_preprocessed)
    return

def wrinting_word_ordering_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep) - 2] = 'corpus-WordOrdering_preprocessed'
    pathsep[len(pathsep) - 1] = pathsep[len(pathsep) - 1].replace('.txt', '_WordOrdering_preprocessed.txt')
    filepath_preprocessed = os.path.join('/'.join(pathsep))
    directory = ".."+os.path.sep+pathsep[len(pathsep) - 2]+os.path.sep
    if not os.path.exists(directory):
        os.makedirs(directory)
    write_file(WO_preprocessing_file(file), filepath_preprocessed)
    return

sep=os.path.sep
file_list = os.listdir('..'+sep+'corpus-20090418')
for each in file_list:
    wrinting_preprocessed_file('..'+sep+'corpus-20090418'+sep+each)

for each in file_list:
    wrinting_adv_preprocessed_file('..'+sep+'corpus-20090418'+sep+each)

for each in file_list:
    wrinting_swr_preprocessed_file('..'+sep+'corpus-20090418'+sep+each)

for each in file_list:
    wrinting_word_ordering_preprocessed_file('..'+sep+'corpus-20090418'+sep+each)
