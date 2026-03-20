# read_files.py
# read, readline, readlines

with open("sample.txt", "r") as f:
    print("read():", f.read())  # read all

with open("sample.txt", "r") as f:
    print("readline():", f.readline())  # read first line

with open("sample.txt", "r") as f:
    print("readlines():", f.readlines())  # read all lines into list