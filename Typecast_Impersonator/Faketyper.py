from pynput.keyboard import Key, Controller
from time import sleep
from sys import stdin
DEBUG = True

if not stdin.isatty():
    print("[ERROR] STDIN not at ty! Pipe input via STDIN!")
sdata = input().split(',')
tdata = input().split(',')

if DEBUG:
    print("Chars and Pairs:  %s" % sdata)
    print("Timings:   %s" % tdata)

slen = len(sdata)
string = "".join(sdata[:slen // 2 + 1])

tlen = len(tdata)
ktp = [float(x) for x in tdata[:tlen // 2 + 1]]
ktd = [float(x) for x in tdata[tlen // 2 + 1:]]
ktd.append(0)

print(f"Key Time Press: {ktp}")
print(f"Key Time Delay: {ktd}")

# type chars matching how they were typed
DELAY = 5
print(f"Config loaded. Beginning type replication in {DELAY} seconds...")
sleep(DELAY)
print("Starting!")
i = 0
keyboard = Controller()
for c in string:
    keyboard.press(c)
    sleep(ktp[i])
    keyboard.release(c)
    sleep(ktd[i])
    i+=1
keyboard.press(Key.enter)
keyboard.release(Key.enter)
print("Finished!")
