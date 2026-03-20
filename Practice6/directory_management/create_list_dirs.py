# create_list_dirs.py
# keywords: os, mkdir, listdir, getcwd

import os  # module to work with files and folders

# create folders test_dir and sub_dir inside it
os.mkdir("test_dir")  # create folder "test_dir"
os.mkdir("test_dir/sub_dir")  # create subfolder "sub_dir" inside "test_dir"
print("Directories created")  # print message

# show all files and folders in current directory
print("List current folder:", os.listdir())  # listdir() -> returns list of files/folders

# show current working directory
print("Current working directory:", os.getcwd())  # getcwd() -> current folder path