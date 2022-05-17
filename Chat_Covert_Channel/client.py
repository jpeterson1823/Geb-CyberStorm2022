# use Python 3
import socket
from sys import stdout
from time import time

# enables debugging output
DEBUG = False

# set the default server's IP address and port
ip = "138.47.99.64"
port = 33333
#ip = "localhost"
#port = 1337

# specifies the default time delta in seconds
dt = 0.15

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))

# receive data until EOF
covert = ""
bcovert = ""
bitcounter = 0
data = s.recv(4096).decode()

while (data.rstrip("\n") != "EOF"):
    # output the data
    #stdout.write(data)
    #stdout.flush()

    # start the "timer", get more data, and end the "timer"
    t0 = time()
    data = s.recv(4096).decode()
    t1 = time()

    # calculate the time delta (and output if debugging)
    delta = round(t1 - t0, 3)
    if (DEBUG):
        stdout.write(" {}\n".format(delta))
        stdout.flush()

    # convert to covert message's 0s and 1s
    if delta >= dt:
        bcovert += '1'
    else:
        bcovert += '0'
    # increment bitcounter
    bitcounter += 1

    # every byte, decode char for covert message
    if bitcounter == 8:
        try:
            covert += chr(int(f'0b{bcovert}', 2))
        except:
            # failure to decode binary will result in printing this
            covert += "[?]"
        # reset bitcounter
        bitcounter = 0
        # reset bcovert
        bcovert = ""
    print(covert)

# close the connection to the server
s.close()

# print the decoded covert message
stdout.write("\nCOVERT={")
stdout.write(covert)
stdout.write("}\n")
stdout.flush()
