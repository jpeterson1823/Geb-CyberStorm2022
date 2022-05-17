import sys


def decode(data): #function that decodes binary data to ascii
    sevenbit = "7 bit ascii decoding:\n"
    eightbit = "8bit ascii decoding:\n"
    output = ""
    if(len(data) % 7 == 0):

        for i in range(0, len(data), 7): # for 7 bit ascii
            # converts 7 digits of binary from string type to base 2 binary, chr converts it to the ascii equivalent
            sevenbit += chr(int(data[i:i + 7], 2))
        output += sevenbit + "\n"
    if (len(data) % 8 == 0):

        for i in range(0, len(data), 8): # for 8 bit ascii
            # converts 8 digits of binary from string type to base 2 binary, chr converts it to the ascii equivalent
            eightbit += chr(int(data[i:i + 8], 2)) # converts 8 digits of binary from string type to base 2 binary, chr converts it to the ascii equivalent
        output += eightbit
    return(output)

# start of the program
input = sys.stdin.readlines() # read input
input = [line.rstrip() for line in input] #strips new lines from input

sys.stdout.write(decode(input[0])) # outputs decoded input
