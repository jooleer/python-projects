# this code is still WIP

import os
import sys
import hashlib
import subprocess
import zlib
import logging
import time
import threading

# define the paths of the two network folders to compare
folder1_path = r""
folder2_path = r""


# hash algorythm (CRC32, MD5, SHA256)
hash_algorithm = "CRC32"

# text markup
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# set logging file parameter
if not os.path.isdir("logs"):
    os.makedirs("logs")
logging.basicConfig(filename="logs/log_"+str(time.time())+".txt", level=logging.INFO)

# start time 
start = time.time()

# define counting variables
files_amount = 0
files_completed = 0
files_errors = 0
files_missing = 0
files = 0


#generate hash value of file
def generate_file_hash(file_path, hash_algorithm="CRC32"):
    with open(file_path, "rb") as f:
        global files
        files += 1
        # sys.stdout.write("Processing file %d of %d (%d%%)\r\n\033[K" % (files, files_amount, (files/files_amount)*100) )
        # sys.stdout.write("Generating hash for file: %s\r\033[F" % (file_path) )
        sys.stdout.flush()
        file_data = f.read()
        if hash_algorithm == "CRC32":
            file_hash = zlib.crc32(file_data)
        elif hash_algorithm == "MD5":
            file_hash = hashlib.md5(file_data).hexdigest()
        elif hash_algorithm == "SHA256":
            file_hash = hashlib.sha256(file_data).hexdigest()

        return file_hash


# function to recursively get a list of all files in a folder and its subfolders
def get_all_files(folder_path):
    global files_amount
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            all_files.append(file_path)
            files_amount += 1
    return all_files


def folder_generate_hashes(folder_path):
    # generate hash values for each file in folder
    folder_hashes = {}
    for file_path in get_all_files(folder_path):
        file_hash = generate_file_hash(file_path, hash_algorithm)
        relative_path = os.path.relpath(file_path, folder_path)
        folder_hashes[relative_path] = file_hash
        # print(f"Done: {relative_path}")
    return folder_hashes


folder1_hashes = {}
folder2_hashes = {}

def gen_folder1_hashes(folder_path=folder1_path):
    global folder1_hashes
    folder1_hashes = folder_generate_hashes(folder_path)
    
def gen_folder2_hashes(folder_path=folder2_path):
    global folder2_hashes
    folder2_hashes = folder_generate_hashes(folder_path)
    

t1 = threading.Thread(target=gen_folder1_hashes, args=(folder1_path,))
t2 = threading.Thread(target=gen_folder2_hashes, args=(folder2_path,))

t1.start()
t2.start()

t1.join()
t2.join()


''' 
# check for missing files in folder 1
for file_path in get_all_files(folder2_path):
    relative_path = os.path.relpath(file_path, folder2_path)
    if relative_path not in folder1_hashes:
        # print(bcolors.WARNING + f"{relative_path} is missing from {folder1_path}." + bcolors.ENDC)
        logging.info(f"[WARNING - MISSING FILE]: {relative_path}")
        files_missing += 1

# check for missing files in folder 2
for file_path in get_all_files(folder1_path):
    relative_path = os.path.relpath(file_path, folder1_path)
    if relative_path not in folder2_hashes:
        # print(bcolors.WARNING + f"{relative_path} is missing from {folder2_path}." + bcolors.ENDC)
        logging.info(f"[WARNING - MISSING FILE]: {relative_path}")
        files_missing += 1
'''

# compare the hash values for each file in both folders
for relative_path in set(folder1_hashes.keys()).intersection(set(folder2_hashes.keys())):
    if folder1_hashes[relative_path] != folder2_hashes[relative_path]:
        # print(bcolors.FAIL + f"Hash values for {relative_path} do not match." + bcolors.ENDC)
        logging.error(f"[FILE HASH ERROR]: {relative_path}")
        files_errors += 1
    else:
        # print(bcolors.OKGREEN + f"Hash values for {relative_path} match." + bcolors.ENDC)
        logging.info(f"[OK]: {relative_path}")
        files_completed += 1

# end time
end = time.time()

# process output information
print("\nProcess finished in {:.2f}".format(round((end - start), 2)) + " seconds")
print(f"Processed {files_amount} file(s): "
+ bcolors.OKGREEN + f"\n{files_completed} file(s) OK" + bcolors.ENDC
+ bcolors.FAIL + f"\n{files_errors} file(s) FAILED" + bcolors.ENDC
+ bcolors.WARNING + f"\n{files_missing} file(s) MISSING" + bcolors.ENDC)
