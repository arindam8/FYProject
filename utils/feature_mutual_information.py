"""
This script is responsible for processing the dataset and caclculating
the values necessary for the calculation of the mutual information
feature
"""

import subprocess
import os
import random
import shutil
import matplotlib.pyplot as plt
import csv
import pandas as pd



def getRandomFileSet(path, comparison_size):
  """
  Returns a list of n random files, chosen among the files of the given path.
  """
  files = os.listdir(path)
  byte_files = []
  for file in files:
      if file.endswith(".bytes"):
          byte_files.append(file)

  indices = random.sample(range(0, len(byte_files)), comparison_size)
  print (indices)
  reference_file_set = []
  index = 0
  for i in indices:
      reference_file_set.append(byte_files[i])
  return (reference_file_set)

def concat_files(path_f, path_s, file_dest):
    new_filename = getFileName(path_f) + '+' + getFileName(path_s)
    file_f = open(path_f, "r")
    file_s = open(path_s, "r")
    f = open(file_dest+new_filename+'.bytes', "w")
    f.write(file_f.read())
    f.write(file_s.read())
    new_file_path = file_dest+new_filename+'.bytes'
    return (new_file_path)


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



def processFile(filepath, reference_data_dir_path,ref_compressed_length_dict):
    file_processed = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_p/"+filepath
    s_i = os.path.getsize(file_processed)
    file_dir = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/File Compression/"+getFileName(filepath)+'/'
    distance = {}
    try:
        os.mkdir(file_dir)
        os.chdir(file_dir)
        comp_file_length = compress_file(file_processed,file_dir)
    except OSError:
        print ("Creation of the directory failed")
    for file in os.listdir(reference_data_dir_path):
        if file.endswith(".bytes"):
            concatenated_file_path = concat_files(reference_data_dir_path+file,file_processed,file_dir)
            concatenated_file_path_rev = concat_files(file_processed,reference_data_dir_path+file,file_dir)
            concat_file_comp_length = compress_file(concatenated_file_path,file_dir)
            concat_file_comp_length_rev = compress_file(concatenated_file_path_rev,file_dir)
            s_j = os.path.getsize(reference_data_dir_path+file)
            print ('s_j '+str(s_j))
            cs_j = ref_compressed_length_dict[getFileName(file)]
            print ('comp s_j '+str(cs_j))
            cs_i = comp_file_length
            print ('comp s_i '+str(cs_i))
            cs_js_i = concat_file_comp_length
            print ('comp s_j s_i '+str(cs_js_i))

            cs_is_j = concat_file_comp_length_rev
            print ('comp s_i s_j '+str(cs_is_j))
            H_si_sj = (cs_js_i - cs_j)/s_i
            print ('H s_i s_j '+str(H_si_sj))
            H_sj_si = (cs_is_j - cs_i)/s_j
            print ('H s_j s_i '+str(H_sj_si))
            H_si = cs_i/s_i
            print ('H s_i '+str(H_si))
            H_sj = cs_j/s_j
            print ('H s_j '+str(H_sj))
            nr = max(H_si_sj,H_si_sj)
            dr = max(H_si,H_si)
            distance[getFileName(file)] = nr/dr
    return (distance)





def compute_distance(s_js_i,s_j,s_i):
    return ((s_js_i-s_j)/s_i)





def compress_file(filepath,compressed_file_dest):
    filename_with_ext = os.path.basename(filepath)
    filename, file_extension = os.path.splitext(filename_with_ext)
    # Execute following command
    # 7z a archive.7z *.txt -m0=PPMd
    output = (subprocess.check_output(['7z', 'a', compressed_file_dest+filename+'.7z', filepath, '-m0=PPMd']))
    # output = (subprocess.check_output(['7z', 'a', compressed_file_dest+filename+'.7z', filepath]))

    printable_output = output.decode("utf-8")
    return (os.path.getsize(compressed_file_dest+filename+'.7z'))

def main():
    base_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/"
    mutual_info_dist = {}
    ref_compressed_length_dict = {}
    data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/train_n/"
    reference_file_set = getRandomFileSet(data_dir_path,5)
    reference_data_dir_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/Reference Set/"
    try:
        os.mkdir(reference_data_dir_path)
        file_compression_dir = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/File Compression/"
        os.mkdir(file_compression_dir)
    except OSError:
        print ("Creation of the directory failed")
    reference_file_dict = {}
    i=1;
    # Move the files selected for reference set to the new Reference Set directory
    for file in reference_file_set:
        reference_file_dict[i] = (getFileName(file))
        i=i+1
        shutil.move(data_dir_path+file,reference_data_dir_path)

    # Create compressed version of each file in the reference set
    for file in os.listdir(reference_data_dir_path):
        ref_compressed_length_dict[getFileName(file)] = compress_file(reference_data_dir_path+file,reference_data_dir_path)
    # Process each file from the training set after the reference files have been removed
    for file in os.listdir(data_dir_path):
        if file.endswith(".bytes"):
            print ('\n')
            print ('Processing File:'+file)
            mutual_info_dist[getFileName(file)] = processFile(file,reference_data_dir_path,ref_compressed_length_dict)

    output_dict_to_csv(base_path+'mutual_info_distances.csv',mutual_info_dist,base_path+'mutual_info_distances.png')
    print ('The output csv file is: '+ base_path+'mutual_info_distances.csv')
    # test()




# def test():
#     base_path = "/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/0G4hwobLuAzvl1PWYfmd.bytes"
#     concatenated_file_path = concat_files(base_path,base_path,"/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/")
#     concat_file_comp_length = compress_file(concatenated_file_path,"/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/")
#     comp_file_length = compress_file(base_path,"/Users/arindamsharma/Desktop/FY/FY Project/Dataset/Microsoft MCC/")
#     s_i = os.path.getsize(base_path)
#     print ('concat file length '+ str(concat_file_comp_length))
#     print ('s_i '+str(s_i))
#     print ('cs_i'+str(comp_file_length))



if __name__ == "__main__":
    main()
