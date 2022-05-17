from datetime import datetime, timedelta
from hashlib import md5
import sys, time

# for each time given, encode and print
for line in sys.stdin:
    # calculate time delta
    a = datetime.strptime("2017 04 23 18 02 30", "%Y %m %d %H %M %S")
    if time.localtime(time.mktime(a.timetuple())).tm_isdst:
        print("A DST")
        a -= timedelta(hours=1)

    e = datetime.strptime(line.strip(), "%Y %m %d %H %M %S")
    if time.localtime(time.mktime(e.timetuple())).tm_isdst:
        print("E DST")
        e -= timedelta(hours=1)

    print(a)
    print(e)

    t = a - e
    t -= timedelta(seconds=t.total_seconds()%60)
    tt = str(int(t.total_seconds()))
    print(tt)

    # nested hash
    h = md5(tt.encode()).hexdigest()
    h = md5(h.encode()).hexdigest()
    print(h)

    # get code
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
