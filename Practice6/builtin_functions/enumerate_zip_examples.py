# enumerate_zip_examples.py
# enumerate, zip, type conversion

names = ["Alice", "Bob", "Charlie"]  # sample names
ages = [25, 30, 35]  # sample ages

# ENUMERATE -> get index and value
for i, name in enumerate(names):
    print(f"{i}: {name}")  # print index and name

# ZIP -> combine two lists element-wise
for name, age in zip(names, ages):
    print(name, "is", age, "years old")  # pair name and age

# TYPE CONVERSIONS -> change types
print("str to int:", int("123") + 1)  # convert string to integer
print("int to str:", str(456) + " ok")  # convert integer to string