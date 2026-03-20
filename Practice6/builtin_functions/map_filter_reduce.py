# map_filter_reduce.py
# map, filter, reduce, lambda
from functools import reduce  # reduce is in functools module

nums = [1, 2, 3, 4, 5]  # sample list

# MAP -> apply a function to each item
mapped = list(map(lambda x: x*2, nums))
print("map x*2:", mapped)

# FILTER -> keep only items that match a condition
filtered = list(filter(lambda x: x>3, nums))
print("filter >3:", filtered)

# REDUCE -> combine all items into one value
summed = reduce(lambda x, y: x+y, nums)
print("reduce sum:", summed)