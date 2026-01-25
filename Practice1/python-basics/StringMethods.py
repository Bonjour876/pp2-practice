s = "  Hello World 123  "
# Case conversion
print(s.upper())       # '  HELLO WORLD 123  '
print(s.lower())       # '  hello world 123  '
print(s.capitalize())  # '  hello world 123  '
# Checks (boolean results)
print(s.isalpha())         # False -> contains spaces and numbers, not only letters
print("Hello".isalpha())   # True -> only letters
print(s.isspace())         # False -> contains letters and numbers, not only spaces
print("   ".isspace())     # True -> only spaces
print("123".isdigit())     # True -> only digits
print("Hello123".isalnum())# True -> letters and numbers only
print(s.islower())         # False -> some uppercase letters
print("hello".islower())   # True -> all letters lowercase
print("HELLO".isupper())   # True -> all letters uppercase
# Split and join
print(s.split())           # ['Hello', 'World', '123'] -> split by spaces
print(" ".join(["Hello", "World"])) # 'Hello World' -> join list with space
# Modifying strings
print(s.strip())           # 'Hello World 123' -> removes spaces from both ends
print(s.replace("World", "Python")) # '  Hello Python 123  ' -> replaces substring
# String formatting
print("My name is {name}".format(name="John"))  # 'My name is John' -> insert value
