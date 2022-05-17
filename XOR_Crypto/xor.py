#!/usr/bin/python3
from sys import argv, stdin, stdout

def access_bit(data, num):
    base = int(num//8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1

if len(argv) != 2:
    print("Must provide a key file as argument.")
    exit()

# get key and text in byte-form as bytearray
key  = bytearray(open(argv[1], "rb").read())
text = bytearray(stdin.buffer.read())

# calc len of key and text
klen = len(key)
tlen = len(text)

# encode/decode
kp = 0
tp = 0
for i in range(tlen):
    if tp >= tlen:
        tp = 0
    if kp >= klen:
        kp = 0

    c = (text[tp] ^ key[kp])
    #print(f"{bin(text[tp])[2:].zfill(8)}     {bin(key[kp])[2:].zfill(8)}     {bin(c)[2:].zfill(8)}")
    stdout.buffer.write(c.to_bytes(1, byteorder='big'))
    #stdout.write(bin(c)[2:].rjust(8,'0'))
    tp += 1
    kp += 1
stdout.buffer.flush()
