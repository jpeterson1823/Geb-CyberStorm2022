#!/usr/bin/python3
from datetime import datetime, timedelta
from hashlib import md5
import sys, time

TFORMAT = "%Y %m %d %H %M %S"

# check for help string
if '-h' in sys.argv or '--help' in sys.argv:
    print(f"Usage: {sys.argv[0]} epoch_string")
    print(f"       {sys.argv[0]} < file")
    exit(0)


# for each time given, encode and print
if len(sys.argv) != 1:
    enput = sys.argv[1:]
elif not sys.stdin.isatty():
    enput = sys.stdin
else:
    print("[ERROR] No input provided! See '-h' for more info.")
    exit(1)

for line in enput:
    # calculate time delta
    now = datetime.now().strftime(TFORMAT)
    a = datetime.strptime(now, TFORMAT)
    if time.localtime(time.mktime(a.timetuple())).tm_isdst:
        print("CURRENT DST")
        a -= timedelta(hours=1)

    e = datetime.strptime(line.strip(), TFORMAT)
    if time.localtime(time.mktime(e.timetuple())).tm_isdst:
        print("EPOCH DST")
        e -= timedelta(hours=1)

    print("{: <7}:    {:<}".format("CURRENT", str(a)))
    print("{: <7}:    {:<}".format("EPOCH", str(e)))

    t = a - e
    t -= timedelta(seconds=t.total_seconds()%60)
    tt = str(int(t.total_seconds()))
    #print(tt)

    # nested hash
    h = md5(tt.encode()).hexdigest()
    h = md5(h.encode()).hexdigest()
    print("{: <7}:    {:<}".format("Hash", h))

    # get code
    sys.stdout.write("{:<7}:    ".format("Code"))
    s = ""
    cnt = 0
    for c in h:
        if c.isalpha() and cnt < 2:
            s += c
            cnt += 1
        if cnt == 2:
            cnt = 0
            break
    for c in reversed(h):
        if c.isdigit() and cnt < 2:
            s += c
            cnt += 1
        if cnt == 2:
            break

    sys.stdout.write(s + "\n")
sys.stdout.flush()
