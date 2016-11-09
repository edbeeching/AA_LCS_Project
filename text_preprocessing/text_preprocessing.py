# coding=utf-8
import os
def preproceesing_file(file):
    file = file.replace('‘', '\'')
    file = file.replace('’', '\'')
    file = file.replace('“', '\"')
    file = file.replace('”', '\"')
    file = file.replace('\n\n', '\n')
    file = file.replace('  ', ' ')
    #file = file.replace('\'', '')
    #file = file.replace('\"', '')
    #file = file.replace('.', '')
    #file = file.replace(',', '')
    #file = file.replace('/', '')
    #file = file.replace('?', '')
    #file = file.replace('!', '')
    #file = file.replace(';', '')

    preprocessed_file = file
    return preprocessed_file
def adv_preproceesing_file(file):
    file = file.replace('‘', '\'')
    file = file.replace('’', '\'')
    file = file.replace('“', '\"')
    file = file.replace('”', '\"')
    file = file.replace('\n\n', '\n')
    file = file.replace('  ', ' ')
    file = file.replace('\'', '')
    file = file.replace('\"', '')
#    file = file.replace('.', '')
#    file = file.replace(',', '')
    file = file.replace('/', '')
    file = file.replace('?', '')
    file = file.replace('!', '')
    file = file.replace(';', '')
    file = file.replace('(', '')
    file = file.replace(')', '')

    preprocessed_file =file
    return preprocessed_file

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

def wrinting_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep)-2] = 'corpus-preprocessed'
    pathsep[len(pathsep)-1] = pathsep[len(pathsep)-1].replace('.txt','_adv_preprocessed.txt')
    filepath_preprocessed = os.path.join('\\'.join(pathsep))
    write_file(adv_preproceesing_file(file), filepath_preprocessed)
    return

file_list = os.listdir('..\\corpus-20090418')

for each in file_list:
    wrinting_preprocessed_file('..\\corpus-20090418\\'+each)


