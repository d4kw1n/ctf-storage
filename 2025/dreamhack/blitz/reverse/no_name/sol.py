
unk_2004 = [0xde, 0xad,0xbe,0xef]  

def decrypt():
    with open('encrypted', 'rb') as encrypted_file:
        with open('flag.png', 'wb') as output_file:
            v5 = 0 

            while True:
                byte = encrypted_file.read(1)
                if not byte:
                    break  

                ptr = byte[0]
                
                ptr -= 19  
                ptr ^= unk_2004[v5 % 4] 

                ptr = ptr % 256 

                output_file.write(bytes([ptr]))
                v5 += 1  

decrypt()

        