#!/usr/bin/env python3
import string
import random
letters = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]
random.shuffle(letters)
alpha = ""
for letter in letters:
    alpha += letter
print(alpha)
