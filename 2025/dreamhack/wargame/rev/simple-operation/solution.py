from pwn import *

io = remote("host1.dreamhack.games", 13428)

data = io.recvline().decode().split(":")[1].strip()
key = int(data, 16)

result = 0x7d1c4b0a ^ key

io.sendlineafter(b"? ", str(result).encode())
io.interactive()