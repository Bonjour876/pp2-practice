# write_files.py
# write, append, with, open

with open("sample.txt", "w") as f:  # create and write
    f.write("Hello Python!\n")
    f.write("This is a sample file.\n")

with open("sample.txt", "a") as f:  # append
    f.write("Appending new line.\n")