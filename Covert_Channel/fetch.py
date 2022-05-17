# Name: Gregory Whitehurst
# Class: CYEN 301-001
# File: fetch.py
# Team: Geb
# Date: 3/28/2022
# Description: A Python script that can access an FTP server and take read/write permissions
#              and convert them into a 10 bit or 7 (righmost) bit binary string and decrypt the
#              the string into ASCII characters

from ftplib import FTP

#####CONSTANTS######
DEBUG = False
IP = "138.47.128.12"
PORT = 21
USER = "osirus"
PASSWORD = "encryptiongods"
FOLDER = "/"
USE_PASSIVE = True
METHOD = 7

# a function that checks if the first 3 indices
# of a permission have r,x, or w (this is only used if METHOD == 7)
def check(permission):
    for i in range(3):
        if (permission[i] != '-'):
            return False
    return True

# a function to take the permissions and put them in an array
def list_of_perm(files):
    list = []
    # 7 rightmost bits
    if(METHOD == 7):
        for i in range(len(files)):
            str = files[i]
            str = str[:10]
            if (check(str) == True):
                list.append(str)
    # all 10 bits
    elif(METHOD == 10):
        for i in range(len(files)):
            str = files[i]
            str = str[:10]
            list.append(str)
    return list

# this is mostly the same from Binary.py, except I included
# another case to account for 10 bits
def Input_to_array(line):
    dic = {}
    # 7 bit
    if(Case(line) == 7):
        step = 7
        for i in range(0, len(line), 7):
            slice = line[i:step]
            step += 7
            dic[i] = slice
        return list(dic.values())
    # 10 bit
    elif(Case(line) == 10):
        step = 10
        for i in range(0, len(line), 10):
            slice = line[i:step]
            step += 10
            dic[i] = slice
        return list(dic.values())

# checks the case of the input by checking with the
# length of the input string
def Case(line):
    if ((len(line) % 7) == 0):
        return 7
    elif ((len(line) % 10) == 0):
        return 10
    else:
        print("ERROR: string is not 7, or 10 bit binary")
        return 0

# this is exactly the same as Binary.py
def Decrypt(array):
    string = ""
    # Converts binary strings to base 10 integers within the same array
    # Converts each integer into their respective ASCII character.
    for i in range(len(array)):
        array[i] = int(array[i], 2)
        array[i] = chr(array[i])
        string += array[i]
    return string


##########MAIN###########

# FTP setup we did in class
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

ftp.quit()

list_perm = list_of_perm(files)

# based on whether we are using 7 rightmost bits or all 10
# make a string of all the permissions
perm = ""
if(METHOD == 7):
    for f in list_perm:
        perm += f[:10]
else:
    for f in list_perm:
        perm += f[:10]

# converts the string to binary by checking if there is an r, x,
# or an x at that index and adds a 0 or a 1
perm_bin = ""
for i in range(len(perm)):
    if (perm[i] != '-'):
        perm_bin += '1'
    else:
        perm_bin += '0'

# printing input from server as a string
print(f"Input from {IP} in {FOLDER}:\n{perm}")


if(DEBUG == True):
    print("DEBUG on")
    print(f"Input as {METHOD} bit binary:\n{perm_bin}")

# printing the decrypted binary string if no error is thrown
if(Case(perm_bin) != 0):
    arr = Input_to_array(perm_bin)
    if(DEBUG==True):
        print(f"Input as an array:\n{list_perm}")
        print(f"Input as an array in binary:\n{arr}")
    print(f"{Decrypt(arr)}")
else:
    exit()