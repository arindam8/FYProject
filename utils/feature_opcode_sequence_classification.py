from pyparsing import Word, hexnums, WordEnd, Optional, alphas, alphanums
import collections
import os
from nltk.util import ngrams
import nltk
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np



def getNgramFromFile(source_path):
    file = open(source_path,'r',encoding = "ISO-8859-1")
    opcode_list = []
    source = list(file)
    # use WordEnd to avoid parsing leading a-f of non-hex numbers as a hex

    hex_integer = Word(hexnums) + WordEnd()
    line = ".text:" + hex_integer + Optional((hex_integer*(1,))("instructions") + Word(alphas,alphanums)("opcode"))

    for source_line in source:
        if (source_line.startswith('.text')):
            result = line.parseString(source_line)
            if "opcode" in result:
                opcode_list.append((result.instructions.asList()[0]).strip())
    ngram_listof_tuple = (list(ngrams(opcode_list,2)))
    ngram_listof_string = [' '.join(item) for item in ngram_listof_tuple]

    return (ngram_listof_string)






def getFileName(path):
    filename_with_ext = os.path.basename(path)
    filename, file_extension = os.path.splitext(filename_with_ext)
    return (filename)


def output_dict_to_csv(filepath,dict):

    with open(filepath, 'w') as f:
        # w = csv.DictWriter(f, dict.keys())
        # w.writeheader()
        # w.writerow(dict)
        df = pd.DataFrame(dict, index=[0])
        df.to_csv(filepath)
        # df.convert_objects(convert_numeric=True).plot()
        # plt.savefig(imgpath)


def getWordsForDict(path):
    word_list = []
    files = os.listdir(path)
    for file in files:
        if file.endswith(".asm"):
            word_list.extend(getNgramFromFile(path+file))
    return (set(word_list))


def getOpcodeForFile(source_path):
    opcode_list = []
    file = open(source_path,'r',encoding = "ISO-8859-1")
    source = list(file)
    # use WordEnd to avoid parsing leading a-f of non-hex numbers as a hex

    hex_integer = Word(hexnums) + WordEnd()
    line = ".text:" + hex_integer + Optional((hex_integer*(1,))("instructions") + Word(alphas,alphanums)("opcode"))

    for source_line in source:
        if (source_line.startswith('.text')):
            result = line.parseString(source_line)
            if "opcode" in result:
                opcode_list.append((result.instructions.asList()[0]).strip())

    return (opcode_list)

# def test(file):
#     print (getNgramFromFile(file))


def main():
    # test('/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_n/0A32eTdBKayjCWhZqDOQ.asm')
    base_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/"
    print ('Computing dictionary for corpus')
    print ('\n')
    data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_op/"
    img_dir = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_op/images/"
    word_dict = set()
    word_dict = getWordsForDict(data_dir_path)
    word_dict_list = list(word_dict)

    print ('Word list for dictionary computed')
    one_hot_vec_len = len(word_dict_list)
    file_region_dict = {}
    # try:
    #     os.mkdir(img_dir)
    #
    # except OSError:
    #     print ("Creation of the directory failed")
    for file in os.listdir(data_dir_path):
        if file.endswith(".asm"):
            print ('\n')
            print ('Getting region matrix for:'+ file)
            ngram_freq = {}
            regions_list = getNgramFromFile(data_dir_path+file)
            region = []
            region_matrix = []
            for i in range(len(regions_list)-1):
                region.append(regions_list[i]+' '+regions_list[i+1])
                first_element_vec = [0]* one_hot_vec_len
                second_element_vec = [0]* one_hot_vec_len
                first_element_vec[word_dict_list.index(regions_list[i])] = 1
                second_element_vec[word_dict_list.index(regions_list[i+1])] = 1
                first_element_vec.extend(second_element_vec)
                region_matrix.append(first_element_vec)

            file_region_dict[getFileName(file)] = np.asmatrix(np.array(region_matrix))
            print (file_region_dict[getFileName(file)].shape)
            # plt.imshow(file_region_dict[getFileName(file)])
            # plt.savefig(img_dir+getFileName(file)+'.png')

    # output_dict_to_csv(base_path+'opcode_region_stats.csv',file_region_dict)
    print ('The output image directory is: '+ img_dir)
if __name__ == "__main__":
    main()
