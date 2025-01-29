from pwn import *

while True:
    r = remote("host1.dreamhack.games", 20014)
    r.recvuntil(b'can u guess me?\n')
    r.send(b'\0')
    res = r.recvline()
    r.close()
    if b'DH' in res:
        print(res)
        break