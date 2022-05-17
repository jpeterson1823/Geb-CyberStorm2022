# a quick script I wrote to hash items in a list from a text file
# used this for the Amnesia challenge during Cyber Storm
import sys
import hashlib

#print(hashlib.sha256("123".encode()))


list = []
for line in sys.stdin:
    list.append(line)

#print(list[165])
    
newlist = []
for i in range(len(list)):
    list[i]=list[i].strip()
    newlist.append(hashlib.sha256(list[i].encode()))

for i in range(len(list)):
    print(hashlib.sha256(list[i].encode()).hexdigest())

print(newlist)
