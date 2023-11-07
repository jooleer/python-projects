# script that takes all files in folders, renames the files to their parent folder names and moves them one folder up
# had a need for this when I had a bunch of usenet directories/files that had random named files in their directories and this seemed like the best solution for my use case

import os
import sys
import shutil

def rename_and_move_files(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            parent_folder = os.path.basename(root)
            new_filename = os.path.join(root, f'{parent_folder}_{filename}')
            
            # rename the file to include the parent folder name
            os.rename(file_path, new_filename)
            
            # move the renamed file one folder up
            destination_folder = os.path.dirname(root)
            destination_path = os.path.join(destination_folder, os.path.basename(new_filename))
            shutil.move(new_filename, destination_path)

if __name__ == "__main__":
    while True:
        directory = input("Enter the directory path: ")
        if os.path.isdir(directory):
            rename_and_move_files(directory)
            break
        else:
            print("Directory «",directory,"» does not exist.")
        
    print("Files renamed and moved successfully.")
    os.system("pause")
