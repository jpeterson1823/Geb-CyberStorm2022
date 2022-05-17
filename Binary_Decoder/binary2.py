#!/usr/bin/python3
from sys import stdin, argv

if not stdin.isatty():
    data = stdin.read().strip()
elif len(argv) == 2:
    if argv[1] in ['-h', '--help']:
        print(f"Usage: {argv[0]} <string_to_decode>")
        print(f"       {argv[0]} < binary_text_file.ext")
    data = argv[1]
else:
    print("Please provide binary string to decode.")
    exit()

dlen = len(data)

s = ''
if dlen % 7 == 0:
    print("Seven Bit ASCII")
    for i in range(0, dlen, 7):
        s += chr(int(data[i:i+7], 2))

elif dlen % 8 == 0:
    print("Eight Bit ASCII")
    for i in range(0, dlen, 8):
        s += chr(int(data[i:i+8], 2))

else:
    print("Binary data is neither 7 or 8 bit ASCII.")

print(s)
