from pyparsing import Word, hexnums, WordEnd, Optional, alphas, alphanums
import collections
import os
from nltk.util import ngrams
import nltk



def getNgramFromFile(source_path):
    file = open(source_path,'r',encoding = "ISO-8859-1")
    opcode_list = []
    print (source_path)
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


def main():
    data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_n/"
    ngram_set = set()
    ngram_set = getNgramList(data_dir_path)
    file_frequency_dict = {}
    print (ngram_set)
    for file in os.listdir(data_dir_path):
        if file.endswith(".asm"):
            print ('\n')
            print ('Getting ngram frequency for:'+ file)
            ngram_freq = {}
            opcode_list = getOpcodeForFile(data_dir_path+file)
            for ngram in ngram_set:
                print (ngram)
                i = 0
                count = 0
                for i in range(0,len(opcode_list)-2):
                    item = opcode_list[i]+' '+opcode_list[i+1]
                    if (ngram == str(item)):
                        count = count + 1
                ngram_freq[ngram] = count
            file_frequency_dict[getFileName(file)] = ngram_freq
    print (file_frequency_dict)
if __name__ == "__main__":
    main()
