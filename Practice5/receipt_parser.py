import re

# read raw.txt
with open("raw.txt", "r") as f:
    text = f.read()

# findall > return list all matches
print("findall (prices):", re.findall(r"\d+\.\d{2}", text))

# search > find first match
date = re.search(r"\d{4}-\d{2}-\d{2}", text)
if date:
    print("search (date):", date.group())

# split >splits text into parts by spaces
print("split:", re.split(r"\s+", text))

# sub > replaces spaces with "-"
print("sub:", re.sub(r"\s+", "-", text))

# match > checks match at the beginning of the text
print("match:", re.match(r"[A-Za-z]+", text))