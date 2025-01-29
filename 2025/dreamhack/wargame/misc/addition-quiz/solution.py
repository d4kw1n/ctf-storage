from pwn import *

io = remote("host1.dreamhack.games", 23176)

while True:
    res = io.recvline().decode()
    if "Nice!" in res:
        print(res)
        break
    res = res.split("=")[0]
    res = eval(res)
    print(res)
    io.sendline(str(res).encode())

print(f"Flag: {io.recvline().decode()}")
io.close()