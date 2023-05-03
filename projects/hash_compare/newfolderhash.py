import os
import hashlib
import logging
import time

# define the paths of the two network folders to compare
folder1_path = r"\\PoesNAS\\Plex Library\\Testing"
folder2_path = r"\\CatNAS\\Plex Library\\Testing"

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

# function to generate the hash value of a file
def generate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_hash = hashlib.md5(file_data).hexdigest() #test w/ sha256 / md5
        return file_hash

# function to recursively get a list of all files in a folder and its subfolders
def get_all_files(folder_path):
    global files_amount
    all_files = []
    for root, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            all_files.append(file_path)
            files_amount += 1
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



# check for missing files in folder 1
for file_path in get_all_files(folder2_path):
    relative_path = os.path.relpath(file_path, folder2_path)
    if relative_path not in folder1_hashes:
        print(bcolors.WARNING + f"{relative_path} is missing from {folder1_path}." + bcolors.ENDC)
        files_missing += 1

# check for missing files in folder 2
for file_path in get_all_files(folder1_path):
    relative_path = os.path.relpath(file_path, folder1_path)
    if relative_path not in folder2_hashes:
        print(bcolors.WARNING + f"{relative_path} is missing from {folder2_path}." + bcolors.ENDC)
        files_missing += 1


# compare the hash values for each file in both folders
for relative_path in set(folder1_hashes.keys()).intersection(set(folder2_hashes.keys())):
    if folder1_hashes[relative_path] != folder2_hashes[relative_path]:
        print(bcolors.FAIL + f"Hash values for {relative_path} do not match." + bcolors.ENDC)
        logging.error("[ERROR - NO MATCH]: " + relative_path)
        files_errors += 1
    else:
        print(bcolors.OKGREEN + f"Hash values for {relative_path} match." + bcolors.ENDC)
        logging.info("[OK]: " + relative_path)
        files_completed += 1

# end time
end = time.time()

# process output information
print("\nProcess finished in {:.2f}".format(round((end - start), 2)) + " seconds")
print(f"Processed {files_amount} file(s): "
+ bcolors.OKGREEN + f"\n{files_completed} file(s) OK" + bcolors.ENDC
+ bcolors.FAIL + f"\n{files_errors} file(s) FAILED" + bcolors.ENDC
+ bcolors.WARNING + f"\n{files_missing} file(s) MISSING" + bcolors.ENDC)
