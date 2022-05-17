m = "HELLO"
k = "mykey"
i = 0
out = ""
#for only lower alppha
alp = "abcdefghijklmnopqrstuvwxyz"
alpU = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for c in m:
    if c == " ":
        out += " "
    elif c in alp:
        out += alp[((26 + alp.find(c) + alp.find(k[i]))%26)]
        i += 1
        i = i%(len(k))
    elif c in alpU:
        
        out += alpU[((alpU.find(c) + alp.find(k[i]))%26)]
        i += 1
        i = i%(len(k))
    else: 
        out += c
        i += 0
        i = i%(len(k))
print(out)

# for all of ascii
##i = 0
##out2 = ""
##for c in m:
##    if c == " ":
##        out += " "
##    else: 
##        out2 += chr(ord(c) + ord(k[i]))
##        i += 1
##        i = i%(len(k))
##
##print(out2)

#decrpt
crpt = out
out3 = ""
i = 0
for c in crpt:
    if c == " ":
        out3 += " "
    elif c in alp:
        out3 += alp[((26 + alp.find(c) - alp.find(k[i]))%26)]
        i += 1
        i = i%(len(k))
    elif c in alpU:
        out3 += alpU[((26 + alpU.find(c) - alp.find(k[i]))%26)]
        i += 1
        i = i%(len(k))
    else: 
        out3 += c
        i += 0
        i = i%(len(k))
print(out3)

##i = 0
##crpt = out2
##out4 = ""
##for c in crpt:
##    out4 += chr((256 + ord(c) - ord(k[i]))%256)
##    i += 1
##    i = i%(len(k))
##
##print(out4)


