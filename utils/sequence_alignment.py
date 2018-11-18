"""
This script is meant for extracting the global sequence alignment based feature set
from the binaries in the corpus.
"""
from pyparsing import Word, hexnums, WordEnd, Optional, alphas, alphanums
import collections
import os
import random
import shutil
import matplotlib.pyplot as plt
import csv
import pandas as pd
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
import edit_distance



def getRandomFileSet(path, comparison_size):
  """
  Returns a list of n random files, chosen among the files of the given path.
  """
  files = os.listdir(path)
  byte_files = []
  for file in files:
      if file.endswith(".asm"):
          byte_files.append(file)

  indices = random.sample(range(0, len(byte_files)), comparison_size)
  print (indices)
  reference_file_set = []
  index = 0
  for i in indices:
      reference_file_set.append(byte_files[i])
  return (reference_file_set)



def getFileName(path):
    filename_with_ext = os.path.basename(path)
    filename, file_extension = os.path.splitext(filename_with_ext)
    return (filename)

def process_dataset(path):
    dist_dict={}

    files = os.listdir(path)
    for file in files:
        distance =[]
        opcodes = getOpcodesFromFile(file)
    return (dist_dict)




def output_dict_to_csv(filepath,dict,imgpath):

    with open(filepath, 'w') as f:
        # w = csv.DictWriter(f, dict.keys())
        # w.writeheader()
        # w.writerow(dict)
        df = pd.DataFrame(dict)
        df.to_csv(filepath)
        df.convert_objects(convert_numeric=True).plot()
        plt.savefig(imgpath)


def processFile(filepath, reference_data_dir_path):
    file_processed = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_p/"+filepath
    distance = {}

    for file in os.listdir(reference_data_dir_path):
        i=1
        if file.endswith(".asm"):
            score = calc_global_alignment(reference_data_dir_path+file,file_processed)
            print ('Alignment score with reference file '+str(i)+' '+str(score))
            distance[getFileName(file)] = score
        i=int(i)+1
    return (distance)




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
                opcode_str = str(result.opcode)
                opcode_list.append(opcode_str.strip())

    return (opcode_list)

#
# def getOpcodeList(path,opcodes):
#     opcodes = set()
#     files = os.listdir(path)
#     os.chdir(path)
#     for file in files:
#         if file.endswith(".asm"):
#             file_o = open(source_path,'r')
#             source = list(file_o)
#             hex_integer = Word(hexnums) + WordEnd()
#             line = ".text:" + hex_integer + Optional((hex_integer*(1,))("instructions") + Word(alphas,alphanums)("opcode"))
#
#             for source_line in source:
#                 if (source_line.startswith('.text')):
#                     result = line.parseString(source_line)
#                     if "opcode" in result:
#                         opcodes.add(result.opcode)
#     print (opcodes)
#     return (opcodes)

#
#
# def compute_distance_vector():
#     return



def main():
    base_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/"
    alig_dist = {}
    data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_n/"
    reference_file_set = getRandomFileSet(data_dir_path,5)
    reference_data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/Reference Set For Seq Ali/"

    reference_file_dict = {}
    i=1;
    try:
        os.mkdir(reference_data_dir_path)

    except OSError:
        print ("Creation of the directory failed")
    # Move the files selected for reference set to the new Reference Set directory
    for file in reference_file_set:
        reference_file_dict[i] = (getFileName(file))
        i=i+1
        shutil.move(data_dir_path+file,reference_data_dir_path)


    # Process each file from the training set after the reference files have been removed
    for file in os.listdir(data_dir_path):
        if file.endswith(".asm"):
            print ('\n')
            print ('Processing File:'+file)
            alig_dist[getFileName(file)] = processFile(file,reference_data_dir_path)
    output_dict_to_csv(base_path+'alig_dist.csv',alig_dist,base_path+'alig_dist.png')
    print ('The output csv file is: '+ base_path+'alig_dist.csv')
    # test()


"""
    Implementation of the Needleman-Wunsch algorithm (or other distance algorithms) and the score calculation method
"""
def calc_global_alignment(file_f,file_s):
    opcodes_f = getOpcodeForFile(file_f)
    opcodes_s = getOpcodeForFile(file_s)
    # alignments = pairwise2.align.globalms(opcodes_f,opcodes_s,2,-1,-0.5,-0.1, gap_char=["-"],one_alignment_only=True)
    #
    # for a in alignments:
    #     score = a[2]
    #     print (score)
    sm = edit_distance.SequenceMatcher(a=opcodes_f, b=opcodes_s)

    return (sm.ratio())

    # (alig_f,alig_s) = nw.global_align(str(opcodes_s), str(opcodes_f), gap_open=-10, gap_extend=-4)
    # return (alig_f,alig_s)

# def global_alignment_score(alig_f,alig_s):
#     score = nw.score_alignment(alig_f, alig_s, gap_open=-10,gap_extend=-4)
#     return (score)

# def test():
#     fruits = ["orange","pear", "apple","pear","orange"]
#
#     fruits1 = ["pear","apple"]
#
#     # alignments = pairwise2.align.globalms(fruits,fruits1,2,-1,-0.5,-0.1, gap_char=["-"],one_alignment_only=True)
#     #
#     # for a in alignments:
#     #     print (a[2])
#     #     print(format_alignment(*a))
#     sm = edit_distance.SequenceMatcher(a=fruits, b=fruits1)
#     print (sm.get_opcodes())
#     print (sm.ratio())
#     for i in (sm.get_matching_blocks()):
#         print (i)


if __name__ == "__main__":
    main()
