import shutil

# just move sample.txt to subfolder
shutil.move("sample.txt", "test_dir/sample.txt")
print("Moved sample.txt -> test_dir/sample.txt")