#!/usr/bin/python3
import sys, subprocess, os, math, threading

POWER_MAX = 15
ODIR = "brute_out"
BYTE_FLAG = "-B"
BIT_FLAG  = "-b"
BRUTE_TABLE_FORMAT = "{:<4} | {:>8} | {:>8}"
TSTRS = [""] * (POWER_MAX-1)

def perror(msg, context=None):
    sys.stderr.write(f"[ERROR] {msg}:\n")
    if context != None:
        sys.stderr.write(f"{context}\n")
    sys.stderr.flush()

def init_filetree():
    ftree = [
        f"./{ODIR}", 
        f"./{ODIR}/byte_mode", 
        f"./{ODIR}/bit_mode"
    ]

    for path in ftree:
        if not os.path.exists(path):
            os.mkdir(path)

def brute(offset, interval, mode, file):
    s = ""
    if mode == BYTE_FLAG:
        cmd = f"./steg.py -r -B -o{offset} -i{interval} -w{file}"
        mstr = "BTYE"
        out = f"./{ODIR}/byte_mode/o{offset}i{interval}"
    else:
        cmd = f"./steg.py -r -b -o{offset} -i{interval} -w{file}"
        mstr = "BIT"
        out = f"./{ODIR}/bit_mode/o{offset}i{interval}"

    s += BRUTE_TABLE_FORMAT.format(mstr, offset, interval)
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.stderr.decode() == "":
        s += " | {: >7}\n".format("SUCCESS")
        with open(out, "wb+") as f:
            f.write(result.stdout)
    else:
        s += " | {: <7}\n".format("FAILED")
    return s

def thread(i, file):
    for o in range(i, POWER_MAX-1):
        offset = powers[o]
        interval = powers[i]
        TSTRS[i] += brute(offset, interval, mode, file)

if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"Usage: {sys.argv[0]} [-b, -B] <target_file>")
        exit(0)

    elif len(sys.argv) != 3:
        msg = "INCORRECT NUMBER OF ARGUMENTS"
        if BIT_FLAG not in sys.argv and BYTE_FLAG in sys.argv:
            context = "Must provide a data mode (bit or byte)!"
        elif BYTE_FLAG not in sys.argv and BIT_FLAG in sys.argv:
            context = "Must provide a data mode (bit or byte)!"
        else:
            context = "Must provide a target file!"
        perror(msg, context)
        exit(1)

    if BYTE_FLAG in sys.argv:
        mode = BYTE_FLAG
    else:
        mode = BIT_FLAG
    file = sys.argv[len(sys.argv)-1]

    if not os.path.exists(file):
        perror("INCORRECT FILE PATH", f"Could not find file '{file}'")
        exit(1)

    init_filetree()
    powers = [int(math.pow(2, p)) for p in range(1, POWER_MAX)]

    threads = []
    for i in range(0, POWER_MAX-1):
        t = threading.Thread(target=thread, args=(i,file,))
        threads.append(t)
        t.start()

    last = len(threads)
    l = len(threads)
    print(f"Active Threads: {l}", end="")
    while (l != 0):
        for t in threads:
            if not t.is_alive():
                t.join()
                threads.remove(t)
                l -= 1

        if last != l:
            print(f"\r{' '*50}\rActive Threads: {l}", end="")
            last = l

    successes = ["\n".join([y for y in x.split("\n") if "SUCCESS" in y]).strip() for x in TSTRS]
    for s in [x for x in successes if x != ""]:
        print(s)
