#!/usr/bin/python3
from ftplib import FTP
import sys

# Debug mode enables logs
DEBUG=True
out = ""
# Default connection credintials
DEFAULT = {
        "MODE"   : 8,
        "DIR"    : "FILES",
        "IP"     : "10.0.0.125",
        "PORT"   : 21,
        "USER"   : "ra",
        "PSWD"   : "fatherofcreation",
        "PASSIVE": False,
}


# displays help message to console
def display_help():
    print(f"Usage: {sys.argv[0]} [-s, -t, -P, -i <ip>, -p <port>, -u <user:pswd>, -d <directory>]")
    print(f"\tConnection Information:")
    print(f"\t-P:              enable passive mode")
    print(f"\t-i <ip>:         ip address of the desired FTP server")
    print(f"\t-p <port>:       port on which the FTP server is held")
    print(f"\t-u <user:pswd>:  username credintial")
    print(f"\t-d <directory>:  directory in which the covert data lies")
    print("")
    print("\tEncoding format:")
    print(f"\t-s :       seven-bit encoding format")
    print(f"\t-t :       ten-bit encoding format")


# prints msg to console if DEBUG is enabled
def log(msg):
    if DEBUG:
        print(msg)


# connects to a ftp server and returns a FTP object
def ftp_connect(address, port, user, password, passive):
    # create FTP connection obj and attempt connection
    ftp = FTP()
    log(f"Attempting to connect to FTP server @ {address} with credintials:")
    log(f"  Addr: {address}")
    log(f"  Port: {port}")
    log(f"  User: {user}")
    log(f"  Pass: {password}")
    ftp.connect(address, port)
    # login with provided user and password
    ftp.login(user, password)
    # set desired passive state
    ftp.set_pasv(passive)
    log("SUCCESS\n")
    return ftp


# connects to a FTP server and returns the contents of the requested directory
def ftpll(creds):
	# Create list to store list info
    ll = []
	
    # connect to FTP server
    ftp = ftp_connect(
            creds["IP"], 
            creds["PORT"],
            creds["USER"],
            creds["PSWD"],
            creds["PASSIVE"]
        )

    # move to directory and save data
    log(f"Moving to directory: '{creds['DIR']}'")
    ftp.cwd(creds["DIR"])
    log("  SUCCESS")

    log("Saving list output")
    ftp.dir(ll.append)
    log("  SUCCESS\n")
    ftp.quit()
    log("FTP quit successfully")
    return ll


# cleans ftp directory list data
def clean(mode, ll):
    # 10-bit encoding method
            

        
    if mode == 10:
        # isolate file permissions
        data = [line[:10] for line in ll]
        #print([line[14] for line in ll])
        return data

    # 8-bit encoding method
    elif mode == 8:
        # isolate file permissions
        data = [line[:10] for line in ll]
        # only keep file permissions with first 3 bits set to 0
        cleaned = [d for d in data if d[:3] == '---']
        return cleaned

    # unknown mode provided
    else:
        print(f"Unknown mode: {mode}")
        display_help()
        exit()

		
# decodes covert message from list data
def decode(mode, cleaned):
    # 10-bit encoding method
    if mode == 10:
        # join all elements into a string
        cstr = "".join(cleaned)
        #print(cstr)
        # make sure cstr length is a factor of 8; add fluff if not
        while len(cstr) % 8 != 0:
            cstr = '0' + cstr

        # create binary data
        binary = "".join(['0' if c == '-' else '1' for c in cstr])
        
        
        # split into 8bit chars
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]

        # convert each binary number to ascii
        counter = 0
        out = ""
        string = "110111110000110000011110101110000110001010011111110111101000111110000110000111100110111001010001101010010110001000110110000010111011010110101000110100011011100101100111001001110000111011011101011100000100000010001001010100111000011110011011100101111010100001110100111011111010100110000110001010100011010101101010111101011010000111110001100101010110101101010101001001000100100010101001010100100010011110001001000101000010110111000100100010111101011001010101000010000001110000110100110111001110100001010010100011101000111100011100001010000111001110001001010"
        
        print("DATA={", end='')
        for c in chars:
            if string[counter] == '0':
                print(chr(int(c, 2)), end='')
            counter += 1
        print("}")

    # 8-bit encoding method
    elif mode == 8:
        print("DATA={", end='')
        for s in cleaned:
            b = '0b'
            for c in s:
                if c != '-':
                    b += '1'
                else:
                    b += '0'
            print(chr(int(b, 2)), end="")
        print('}');
	
    # unknown mode provided
    else:
        print(f"Unknown mode: {mode}")
        display_help()
        exit()


# main code
def main():
    # create default credintials dict
    creds = DEFAULT

    # check for help flags
    if "-h" in sys.argv or "--help" in sys.argv:
        display_help()
        exit(0)

    # check for mode
    if "-s" in sys.argv:
        creds["MODE"] = 8
    elif "-t" in sys.argv:
        creds["MODE"] = 10
    else:
        print("[ERROR] A encoding method must be specified!")
        exit()
    
    # check optional flags
    if "-P" in sys.argv:
        creds["PASSIVE"] = True
    if "-i" in sys.argv:
        creds["IP"] = sys.argv[sys.argv.index("-i") + 1]
    if "-p" in sys.argv:
        creds["PORT"] = int(sys.argv[sys.argv.index("-p") + 1])
    if "-d" in sys.argv:
        creds["DIR"] = sys.argv[sys.argv.index("-d") + 1]
    if "-u" in sys.argv:
        s = sys.argv[sys.argv.index("-u") + 1].split(":")
        if len(s) != 2:
            print("[ERROR] User flag info was not submitted in user:password format!")
            display_help()
            exit()
        creds["USER"] = s[0]
        creds["PSWD"] = s[1]
    log(f"Credintials: {creds}")

    # connect to FTP server
    files = ftpll(creds)
    [print(f) for f in files]
    log("FTP directory data retrieved.")

    # clean data
    cleaned = clean(creds["MODE"], files)
    #[print(c) for c in cleaned]
    log(f"Directory data cleand. MODE={creds['MODE']}")
    
    # decode
    log(f"Decoding, MODE={creds['MODE']}...")
    decode(creds["MODE"], cleaned)

if __name__ == "__main__":
    for f in ["-h", "help", "--help"]:
        if f in sys.argv:
            display_help()
            exit()
    main()
