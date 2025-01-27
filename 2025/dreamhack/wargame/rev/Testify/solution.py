from pwn import *

io = remote('host1.dreamhack.games', 22957)

io.recvline()

wordlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}!@#$%^&*()_+"

data = "c99" # d6371f1cfc993067093f493684c7341647831143523e91d8c2c89808553bdea0
index = 0

while True:
    if index == len(wordlist):
        break
    io.sendlineafter(b"t:" , b"1")
    io.sendlineafter(b"1:" , (wordlist[index] + data).encode())
    result = io.recvline().decode().strip()
    
    if "pure" in result:
        data = wordlist[index] + data
        print(f"[+] Found: {data}")
        index = 0
    else:
        index += 1
    
    io.sendlineafter(b"n]:", b"y")
    
print(data)

