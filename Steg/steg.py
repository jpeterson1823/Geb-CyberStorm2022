from enum import Enum
import sys

# Create mode enum
class Mode(Enum):
    STORE = 0
    RETRIEVE = 1
    BIT = 2
    BYTE = 3

# Create 
class Config():
    def __init__(self):
        self.mode = None
        self.method = None
        self.offset = 0
        self.interval = 1
        self.wrapper = None
        self.hidden = None
        self.sentinel = bytearray([0x0, 0xff, 0x0, 0x0, 0xff, 0x0])
        self.slen = len(self.sentinel)

def display_help():
    print(f"Usage: {sys.argv[0]} -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]")
    print("    -s          store mode")
    print("    -r          retrieve mode")
    print("    -b          bit mode")
    print("    -B          byte mode")
    print("    -o<val>     set offset to <val>   (default is 0)")
    print("    -i<val>     set interval to <val> (default is 1)")
    print("    -w<val>     set wrapper file to <val>")
    print("    -h<val>     set hidden file to <val>")

def verify_config(config):
    if config.mode == None:
        print("[ERROR] No operation mode set!")
        return False
    elif config.method == None:
        print("[ERROR] No operation method set!")
        return False
    elif config.wrapper == None:
        print("[ERROR] No wrapper file provided!")
        return False
    return True

def parse_config(args):
    # check for help flag
    if len(args) == 2:
        if args[1] == '-h':
            display_help()
            exit(0)
    # make sure mode and size args are set
    if len(args) < 3:
        print("Incorrect number of arguments.")
        print("Use flag '-h' to view help string.")
        exit(1)

    # loop through args and set options
    config = Config()
    for arg in args[1:]:
        if arg == '-s':
            config.mode = Mode.STORE
        elif arg == '-r':
            config.mode = Mode.RETRIEVE
        elif arg == '-b':
            config.method = Mode.BIT
        elif arg == '-B':
            config.method = Mode.BYTE
        elif "-o" in arg:
            config.offset = int(arg[2:])
        elif "-i" in arg:
            config.interval = int(arg[2:])
        elif "-w" in arg:
            config.wrapper = arg[2:]
        elif "-h" in arg:
            config.hidden = arg[2:]
        else:
            print(f"[ERROR] Unrecognized flag '{arg}'.")
            print("Use flag '-h' to view help string.")

    # check config to make sure mission critical flags are set
    if not verify_config(config):
        print("[ERROR] Missing critical arguments.\nUse '-h' to see help string.")

    # return config object
    return config

def _bit_store(config: Config) -> bytearray:
    wrapper = bytearray(open(config.wrapper, "rb").read())
    hidden  = bytearray(open(config.hidden,  "rb").read())
    offset = config.offset
    hlen = len(hidden)
    i = 0

    while i < hlen:
        for j in range(0, 8):
            wrapper[offset] &= 0xFE
            wrapper[offset] |= ((hidden[i] & 0x80) >> 7)
            hidden[i] = (hidden[i] << 1) & (2 ** 8 - 1)
            offset += config.interval
        i+=1
    i = 0
    while i < config.slen:
        for j in range(0, 8):
            wrapper[offset] &= 0xFE
            wrapper[offset] |= ((config.sentinel[i] & 0x80) >> 7)
            config.sentinel[i] = (config.sentinel[i] << 1) & (2 ** 8 - 1)
            offset += config.interval
        i+=1
    return wrapper

def _byte_store(config: Config) -> bytearray:
    # Read wrapper and hidden files as bytearray
    wrapper = bytearray(open(config.wrapper, "rb").read())
    hidden  = bytearray(open(config.hidden,  "rb").read())
    # create index counters
    wptr = config.offset
    hptr = 0
    # store hidden byte-wise into wrapper
    while wptr < len(wrapper) and hptr < len(hidden):
        wrapper[wptr] = hidden[hptr]
        wptr += config.interval
        hptr += 1

    # add sentinel value to wrapper
    for byte in config.sentinel:
        wrapper[wptr] = byte
        wptr += config.interval

    # return modified wrapper bytearray
    return wrapper

def _bit_retrieve(config: Config) -> bytearray:
    wrapper = bytearray(open(config.wrapper, "rb").read())
    hidden  = bytearray()
    offset  = config.offset
    wlen = len(wrapper)
    n = 0
    while offset < wlen:
        b = 0
        for j in range(0, 8):
            if offset >= wlen:
                break
            b |= (wrapper[offset] & 0x01)
            if j < 7:
                b <<= 1
                offset += config.interval
        hidden.append(b)
        offset += config.interval
        n+=1
        if n >= config.slen:
            if hidden[n-config.slen:n] == config.sentinel:
                return hidden[:n-config.slen]
    sys.stderr.write("[WARN] Did not find sentinel!")
    sys.stderr.flush()
    return hidden

def _byte_retrieve(config: Config) -> bytearray:
    wrapper = bytearray(open(config.wrapper, "rb").read())
    hidden  = bytearray()
    offset = config.offset
    n = 0
    while offset < len(wrapper):
        b = wrapper[offset]
        hidden.append(b)
        n+=1

        if n >= config.slen:
            if hidden[n-config.slen:n] == config.sentinel:
                return hidden[:n-config.slen]
        offset += config.interval
    sys.stderr.write("[WARN] Did not find sentinel!")
    sys.stderr.flush()
    return hidden

def print_bytearray(b: bytearray):
    if len(b) == 0:
        print("Bytearray is empty...")
    else:
        for byte in b:
            sys.stdout.buffer.write(byte.to_bytes(1, "big"))
        sys.stdout.flush()


def main():
    # parse configs
    config = parse_config(sys.argv)

    if config.mode == Mode.STORE:
        # byte mode
        if config.method == Mode.BYTE:
            print_bytearray(_byte_store(config))
        # bit mode
        elif config.method == Mode.BIT:
            print_bytearray(_bit_store(config))
        # unknown mode
        else:
            print(f"[ERROR] Unknown storage method provided: {config.method}")

    elif config.mode == Mode.RETRIEVE:
        # byte mode
        if config.method == Mode.BYTE:
            print_bytearray(_byte_retrieve(config))
        # bit mode
        elif config.method == Mode.BIT:
            print_bytearray(_bit_retrieve(config))
        # unknown mode
        else:
            print(f"[ERROR] Unknown storage method provided: {config.method}")

    # idk how this could happen, but just incase
    else:
        print(f"[ERROR] Unknown operation mode: {config.mode}")

if __name__ == "__main__":
    main()
