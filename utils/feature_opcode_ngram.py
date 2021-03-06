from pyparsing import Word, hexnums, WordEnd, Optional, alphas, alphanums
import collections
import os
from nltk.util import ngrams
import nltk
import matplotlib.pyplot as plt
import csv
import pandas as pd




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


def output_dict_to_csv(filepath,dict,imgpath):

    with open(filepath, 'w') as f:
        # w = csv.DictWriter(f, dict.keys())
        # w.writeheader()
        # w.writerow(dict)
        df = pd.DataFrame(dict)
        df.to_csv(filepath)
        df.convert_objects(convert_numeric=True).plot()
        plt.savefig(imgpath)


def getNgramList(path):
    ngram_list = []
    files = os.listdir(path)
    for file in files:
        if file.endswith(".asm"):
            ngram_list.extend(getNgramFromFile(path+file))
    return (set(ngram_list))


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
    print ('Computing ngram list for corpus')
    print ('\n')
    data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_n/"
    ngram_set = set()
    ngram_set = getNgramList(data_dir_path)
    print ('Ngram list computed')

    file_frequency_dict = {}
    for file in os.listdir(data_dir_path):
        if file.endswith(".asm"):
            print ('\n')
            print ('Getting ngram frequency for:'+ file)
            ngram_freq = {}
            ngram_list = getNgramFromFile(data_dir_path+file)
            for ngram in ngram_set:
                count = ngram_list.count(ngram)
                # for i in range(0,len(opcode_list)-2):
                #     item = opcode_list[i]+' '+opcode_list[i+1]
                #     if (ngram == str(item)):
                #         count = count + 1
                ngram_freq[ngram] = count
            file_frequency_dict[getFileName(file)] = ngram_freq
    output_dict_to_csv(base_path+'byte_ngram.csv',file_frequency_dict,base_path+'byte_ngram.png')
    print ('The output csv file is: '+ base_path+'byte_ngram.csv')
if __name__ == "__main__":
    main()
