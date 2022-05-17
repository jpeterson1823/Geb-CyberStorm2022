from pynput.keyboard import Key, Listener, Controller
from time import sleep
from sys import stdin, stdout
from random import randint

DEBUG = False



password = input()
timings =  input()
if DEBUG:
    print(f"{password}")
    print(F"{timings}")

password = password.split(",")
timings = timings.split(",")
kpt = []
kit = []

passwd = "".join(password[:(len(timings)//2)+1])
lp = "".join(password[(len(timings)//2)+1:])
i = 0
for x in timings:
    if i < ((len(timings)//2)+1):
        kpt.append(x)
    else:
        kit.append(x)
    i +=1
#kit = [float(x) for x in timings[(len(timings)/2)+1:]]



l = 0
for c in kpt:
    kpt[l] = float(c)
    l +=1
l = 0
for c in kit:
    kit[l] = float(c)
    l +=1
    
if DEBUG:
    print(password)
    print(timings)
    print(passwd)
    print(lp)
    print(kpt)
    print(kit)

sleep(5)

keyboard = Controller()

string = passwd
c = 0
for char in string:
    keyboard.press(char)
    sleep(kpt[c])
    keyboard.release(char)
    if c < len(kit):
        sleep(kit[c])
    c += 1

