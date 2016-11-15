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
    file = file.replace('?', '')
    file = file.replace('!', '')
    file = file.replace(';', '')
    file = file.replace('(', '')
    file = file.replace(')', '')
    StopWords = read_file("./LongListStopWords.txt").split()
    for stopWord in StopWords:

        file = file.replace(stopWord+' ', ' ')
        file = file.replace(' '+stopWord+',', ',')
        file = file.replace(' '+stopWord+'.', '.')
        file = file.replace(' '+stopWord+' ', ' ')

    preprocessed_file =file
    return preprocessed_file



def wrinting_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep)-2] = 'corpus-preprocessed'
    pathsep[len(pathsep)-1] = pathsep[len(pathsep)-1].replace('.txt', '_preprocessed.txt')
    filepath_preprocessed = os.path.join('/'.join(pathsep))
    write_file(preproceesing_file(file), filepath_preprocessed)
    return

def wrinting_adv_preprocessed_file(filepath):
    filepath = os.path.join(filepath)
    file = read_file(filepath)
    pathsep = filepath.split(os.path.sep)
    pathsep[len(pathsep)-2] = 'corpus-adv_preprocessed'
    pathsep[len(pathsep)-1] = pathsep[len(pathsep)-1].replace('.txt', '_adv_preprocessed.txt')
    filepath_preprocessed = os.path.join('/'.join(pathsep))
    write_file(adv_preproceesing_file(file), filepath_preprocessed)
    return


sep=os.path.sep
file_list = os.listdir('..'+sep+'corpus-20090418')
for each in file_list:
    wrinting_preprocessed_file('..'+sep+'corpus-20090418'+sep+each)

for each in file_list:
    wrinting_adv_preprocessed_file('..'+sep+'corpus-20090418'+sep+each)
