
import sys


def decode(data): #function that decodes binary data to ascii
    sevenbit = "7 bit ascii decoding:\n"
    eightbit = "8 bit ascii decoding:\n"
    output = ""
    if(len(data) % 7 == 0):

        for i in range(0, len(data), 7): # for 7 bit ascii
            # converts 7 digits of binary from string type in base 2 binary to int base 10
            # chr converts it to the ascii equivalent
            sevenbit += chr(int(data[i:i + 7], 2))
        output += sevenbit + "\n"
    if (len(data) % 8 == 0):

        for i in range(0, len(data), 8): # for 8 bit ascii
            # converts 8 digits of binary from string type in base 2 binary to int base 10
            # chr converts it to the ascii equivalent
            eightbit += chr(int(data[i:i + 8], 2))
        output += eightbit
    return(output)

# start of the program
input = sys.stdin.readlines() # read input
input = [line.rstrip() for line in input] #strips new lines from input

sys.stdout.write(decode(input[0])) # outputs decoded input
