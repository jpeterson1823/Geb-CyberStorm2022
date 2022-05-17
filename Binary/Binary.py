# Name: Gregory Whitehurst
# Class: CYEN 301-001
# File: Binary.py
# Description: A Python script that takes input from stdin
#              (specifically a txt file with Binary) and decrypts
#              it into a string of ASCII characters that form a
#              message
import sys

# Actually decrypts the array and makes it into a string.
def Decrypt(array):
    string = ""
    # Converts binary strings to base 10 integers within the same array
    for i in range(len(array)):
        array[i] = int(array[i], 2)
    # Converts each integer into their respective ASCII character.
    for j in range(len(array)):
        array[j] = chr(array[j])
    # Adds each character to a string
    for h in range(len(array)):
        string += array[h]
    return string

# A function checking if we must decrypt in 7 or 8 bit binary. If
# neither, return an error.
def SevenOrEight(line):
    if ((len(line) % 8) == 0):
        return 8
    elif ((len(line) % 7) == 0):
        return 7
    else:
        print("ERROR: string is not 7 or 8 bit binary")
        return 0

# A function to take the string and put it into a dictionary,
# and then take the values from the dictionary and put them into
# a list.
def Input_to_array(line):
    dic = {}
    if (SevenOrEight(line) == 8):
        step = 8
        for i in range(0, len(line), 8):
            slice = line[i:step]
            step += 8
            dic[i] = slice
        return list(dic.values())
    else:
        step = 7
        for i in range(0, len(line), 7):
            slice = line[i:step]
            step += 7
            dic[i] = slice
        return list(dic.values())
        
######### MAIN #########
# input from stdin
for line in sys.stdin:
    if 'q' == line.rstrip():
        break
    # printing the input
    print(f'Input: {line}')

newline = line.strip()

# doesn't run if it is neither of the cases
if (SevenOrEight(newline) != 0):
    arr = Input_to_array(newline)
    print(f"This input is in {SevenOrEight(newline)} bit binary.")
    print(f"Decrypted Text: \n{Decrypt(arr)} ")