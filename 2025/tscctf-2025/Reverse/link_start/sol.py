# s2              db ';sDs'               ; DATA XREF: main+37C↑o
# .rodata:0000000000002024                 db  1Fh
# .rodata:0000000000002025                 db  10h
# .rodata:0000000000002026                 db  49h ; I
# .rodata:0000000000002027                 db  45h ; E
# .rodata:0000000000002028                 db  1Fh
# .rodata:0000000000002029                 db  72h ; r
# .rodata:000000000000202A                 db  24h ; $
# .rodata:000000000000202B                 db  55h ; U
# .rodata:000000000000202C                 db  71h ; q
# .rodata:000000000000202D                 db  7Fh ; 
# .rodata:000000000000202E                 db  71h ; q
# .rodata:000000000000202F                 db  7Ch ; |
# .rodata:0000000000002030                 db  24h ; $
# .rodata:0000000000002031                 db  6Bh ; k
# .rodata:0000000000002032                 db  7Eh ; ~
# .rodata:0000000000002033                 db    3
# .rodata:0000000000002034                 db  75h ; u
# .rodata:0000000000002035                 db  6Ch ; l
# .rodata:0000000000002036                 db  4Fh ; O
# .rodata:0000000000002037                 db  79h ; y
# .rodata:0000000000002038                 db  21h ; !
# .rodata:0000000000002039                 db  7Fh ; 
# .rodata:000000000000203A                 db  64h ; d
# .rodata:000000000000203B                 db  7Dh ; }
# .rodata:000000000000203C                 db  12h
# .rodata:000000000000203D                 db  74h ; t
# .rodata:000000000000203E                 db  63h ; c
# .rodata:000000000000203F                 db  55h ; U
# .rodata:0000000000002040                 db  21h ; !
# .rodata:0000000000002041                 db  60h ; `
# .rodata:0000000000002042                 db  4Fh ; O
# .rodata:0000000000002043                 db  5Bh ; [
# .rodata:0000000000002044                 db  0Dh
# .rodata:0000000000002045                 db  6Ch ; l
# .rodata:0000000000002046                 db  4Fh ; O
# .rodata:0000000000002047                 db  7Ch ; |
# .rodata:0000000000002048                 db  3Dh ; =
# .rodata:0000000000002049                 db  5Eh ; ^
# .rodata:000000000000204A                 db  6Eh ; n
# .rodata:000000000000204B                 db  4Eh ; N

s2 = [0x3B, 0x73, 0x44, 0x73, 0x1F, 0x10, 0x49, 0x45, 0x1F, 0x72, 0x24, 0x55, 0x71, 0x7F, 0x71, 0x7C, 0x24, 0x6B, 0x7E, 0x03, 0x75, 0x6C, 0x4F, 0x79, 0x21, 0x7F, 0x64, 0x7D, 0x12, 0x74, 0x63, 0x55, 0x21, 0x60, 0x4F, 0x5B, 0x0D, 0x6C, 0x4F, 0x7C, 0x3D, 0x5E, 0x6E, 0x4E]
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

def sub_1249(a1, a2):
    # Tạo một node mới
    v3 = Node(a2)
    
    # Thiết lập các liên kết giữa node
    v3.prev = a1.prev
    v3.next = a1
    if a1.prev:
        a1.prev.next = v3
    a1.prev = v3
    
    # Trả về a1
    return a1

def sub_12C5(a1):
    ptr = a1[0]
    
    a1[0] = ptr.next
    if ptr.next:
        ptr.next.prev = None
    
    v2 = ptr.prev
    del ptr  
    
    return v2