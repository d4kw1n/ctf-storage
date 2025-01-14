# .rdata:00405064 _flag_encrypted db 0FEh                 ; DATA XREF: _decrypt_flag+6↑o
# .rdata:00405064                                         ; _decrypt_flag+21↑o ...
# .rdata:00405065                 db 0F9h
# .rdata:00405066                 db 0E9h
# .rdata:00405067                 db 0D1h
# .rdata:00405068                 db 0E3h
# .rdata:00405069                 db 0F5h
# .rdata:0040506A                 db 0FEh
# .rdata:0040506B                 db 0C2h
# .rdata:0040506C                 db 0C3h
# .rdata:0040506D                 db 0C4h
# .rdata:0040506E                 db 0C1h
# .rdata:0040506F                 db 0F5h
# .rdata:00405070                 db 0D3h
# .rdata:00405071                 db 0C5h
# .rdata:00405072                 db 0DFh
# .rdata:00405073                 db 0F5h
# .rdata:00405074                 db 0ECh
# .rdata:00405075                 db 0C3h
# .rdata:00405076                 db 0D2h
# .rdata:00405077                 db 0F5h
# .rdata:00405078                 db  98h
# .rdata:00405079                 db 0C5h
# .rdata:0040507A                 db 0C7h
# .rdata:0040507B                 db 0CFh
# .rdata:0040507C                 db 0F5h
# .rdata:0040507D                 db  99h
# .rdata:0040507E                 db 0D8h
# .rdata:0040507F                 db 0D8h
# .rdata:00405080                 db 0C5h
# .rdata:00405081                 db 0D8h
# .rdata:00405082                 db 0D7h

flag = [0xFE, 0xF9, 0xE9, 0xD1, 0xE3, 0xF5, 0xFE, 0xC2, 0xC3, 0xC4, 0xC1, 0xF5, 0xD3, 0xC5, 0xDF, 0xF5, 0xEC, 0xC3, 0xD2, 0xF5, 0x98, 0xC5, 0xC7, 0xCF, 0xF5, 0x99, 0xD8, 0xD8, 0xC5, 0xD8, 0xD7]

for i in range(len(flag)):
    flag[i] ^= 0xAA
    
print(''.join([chr(x) for x in flag]))