#!/usr/bin/python3
import sys, select

# create alphabet string; will be used as reference for encoding and decoding
ALPH = 'abcdefghijklmnopqrstuvwxyz'

# create help message string to print when the help flag is raised or an error occurs
HELP_STR = \
'''Usage: vigenere.py <-e, -d> <key, cipher>
       -e        encode mode, requires cipher key
       -d        decode mode, requires cipher key
'''

# encodes a data string using the provided key
def encode(data, key):
    # get len of key and set the key index to 0
    klen = len(key)
    k = 0
    
    # loop through every char in the provided data string
    cipher = ''
    for d in data:
        # if the char is not in the alphabet list, don't encode it
        if d.lower() in ALPH:
            if d.isupper():     # keep track of case
                cipher += ALPH[(26 + ALPH.index(d.lower()) + ALPH.index(key[k])) % 26].upper()
            
            else:
                cipher += ALPH[(26 + ALPH.index(d) + ALPH.index(key[k])) % 26]

            # increment key index
            k += 1
            k %= klen   # credit to Benjamin for this little trick
        else:
            # do not encode char that isn't in alphabet
            cipher += d
    # return the encoded ciphertext
    return cipher


# decodes a ciphertext string using the provided key
def decode(cipher, key):
    # get len of key and set the key index to 0
    klen = len(key)
    k = 0
    
    # loop through every char in the provided ciphertext
    data = ''
    for c in cipher:
        # if the char is not in the alphabet list, don't decode it
        if c.lower() in ALPH:
            if c.isupper():     # keep track of case
                data += ALPH[(26 + ALPH.index(c.lower()) - ALPH.index(key[k])) % 26].upper()
            else:
                data += ALPH[(ALPH.index(c) - ALPH.index(key[k])) % 26]
            # increment key index
            k += 1
            k %= klen   # credit to Benjamin for this little trick
        else:
            # do not decode char that isn't in alphabet
            data += c
    # return decoded data string
    return data


# core logic of script
def main():
    # check for help request
    if len(sys.argv) == 2:
        print(f"{HELP_STR}")
        exit(0)

    # check to make sure there are 3 arguments provided
    elif len(sys.argv) != 3:
        print("[ERROR] Insufficient values provided: ", end="")
        if "-e" in sys.argv:
            print("encoding requires a cipher key!")
        elif "-d" in sys.argv:
            print("decoding requires a cipher key!")
        else:
            print("incorrect number of arguments!")
        print("        Use '-h' flag for help.")
        exit()

    # note the flag and key, then format key accordingly
    flag = sys.argv[1]
    key = sys.argv[2].replace(' ', '').lower()

    # display help screen if help option is given
    if flag == '-h':
        print(HELP_STR)
        exit(0)
    
    # encode mode
    elif flag == '-e':
        # check for stdin and encode if found
        if select.select([sys.stdin,],[],[],0.0)[0]:
            print(encode(sys.stdin.read(), key))

        # enter infinite loop of waiting for input to encode
        while True:
            print(encode(input(), key) + '\n')

    # decode mode
    elif flag == '-d':
        # check for stdin and decode if found
        if select.select([sys.stdin,],[],[],0.0)[0]:
            print(decode(sys.stdin.read(), key))
        
        # enter infinite loop of waiting for input to encode
        while True:
            print(decode(input(), key) + '\n')
    else:
        # if unknown flag is provided, display error message along with help message
        print(f"[ERROR] Unrecognized flag '{flag}'\n{HELP_STR}")


if __name__ == '__main__':
    # wrapper for main method, preventing crash-out from common interrupts
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except EOFError:
        exit()
