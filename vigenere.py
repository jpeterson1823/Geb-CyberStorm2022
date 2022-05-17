#Benjamin Sanguinetti
#GEB
#CSC 442
#
import sys
mode = sys.argv[1]
key = sys.argv[2]
k = key.lower()
k = k.replace(" ", "") #Removes spaces and set key to lower case
alp = "abcdefghijklmnopqrstuvwxyz"
alpU = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


if mode == "-e": #encrypt mode
    while True:
        m = input("")
        out = ""
        i = 0
        for c in m: # if char is a space
            if c == " ":
                out += " "
            elif c in alp:
                out += alp[((26 + alp.find(c) + alp.find(k[i]))%26)] # if char is in lower alpha
                i += 1
                i = i%(len(k))
            elif c in alpU:
                out += alpU[((26 + alpU.find(c) + alp.find(k[i]))%26)] # if char is in upper alpha
                i += 1
                i = i%(len(k))
            else:               # if char is other add it to out string but do not incriment key
                out += c
                i += 0
                i = i%(len(k))
        print (out)

if mode == "-d":        #decrypt mode
    while True:
        try:                # when reading form file and end of file is found input throws and error this is to end the program
            crpt = input("")
        except:
            break
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
