from socket import *
from time import *
s = socket(AF_INET, SOCK_STREAM)
port = 1337
s.bind(("",port))
s.listen(0)
ZERO = 0.025
ONE = 0.5
print("Server Online")
c, addr = s.accept()
msg = "My Brain is in pain \n"
for i in msg:
    c.send(i.encode())
    sleep(0.1)

c.send("EOF".encode())
print("<essage Sent")
c.close()
