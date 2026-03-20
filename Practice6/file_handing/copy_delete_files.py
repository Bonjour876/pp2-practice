# copy_delete_files.py
# shutil, copy

import shutil

# copy sample.txt to sample_copy.txt
shutil.copy("sample.txt", "sample_copy.txt")
print("Copied sample.txt -> sample_copy.txt")

# return the sample copy text
with open("sample_copy.txt", "r") as f:
    print("Content of copy:")
    print(f.read())