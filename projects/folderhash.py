import os
import hashlib
import time

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

# define the paths of the two network folders to compare
folder1_path = r""
folder2_path = r""

# function to generate the hash value of a file
def generate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_hash = hashlib.sha256(file_data).hexdigest()
        return file_hash

# get the list of files in each folder
folder1_files = os.listdir(folder1_path)
folder2_files = os.listdir(folder2_path)

# generate hash values for each file in folder 1
folder1_hashes = {}
for filename in folder1_files:
    file_path = os.path.join(folder1_path, filename)
    if os.path.isfile(file_path):
        file_hash = generate_file_hash(file_path)
        folder1_hashes[filename] = file_hash

# generate hash values for each file in folder 2
folder2_hashes = {}
for filename in folder2_files:
    file_path = os.path.join(folder2_path, filename)
    if os.path.isfile(file_path):
        file_hash = generate_file_hash(file_path)
        folder2_hashes[filename] = file_hash

# compare the hash values for each file in both folders
for filename in set(folder1_files).intersection(set(folder2_files)):
    if folder1_hashes.get(filename) != folder2_hashes.get(filename):
        print(f"\033[93mHash values for {filename} do not match.\033[0m")
    else:
        print(f"\033[92m{folder1_path}{filename} OK\033[0m")