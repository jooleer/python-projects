import os
import hashlib
import logging

# set logging file parameter
logging.basicConfig(filename="folderhash_log.txt")

# define the paths of the two network folders to compare
folder1_path = r"\\PoesNAS\\Plex Library\\Testing"
folder2_path = r"\\CatNAS\\Plex Library\\Testing"

# function to generate the hash value of a file
def generate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_hash = hashlib.sha256(file_data).hexdigest()
        return file_hash

# function to recursively get a list of all files in a folder and its subfolders
def get_all_files(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            all_files.append(file_path)
    return all_files

# generate hash values for each file in folder 1
folder1_hashes = {}
for file_path in get_all_files(folder1_path):
    file_hash = generate_file_hash(file_path)
    relative_path = os.path.relpath(file_path, folder1_path)
    folder1_hashes[relative_path] = file_hash

# generate hash values for each file in folder 2
folder2_hashes = {}
for file_path in get_all_files(folder2_path):
    file_hash = generate_file_hash(file_path)
    relative_path = os.path.relpath(file_path, folder2_path)
    folder2_hashes[relative_path] = file_hash

# compare the hash values for each file in both folders
for relative_path in set(folder1_hashes.keys()).intersection(set(folder2_hashes.keys())):
    if folder1_hashes[relative_path] != folder2_hashes[relative_path]:
        print(f"Hash values for {relative_path} do not match.")
