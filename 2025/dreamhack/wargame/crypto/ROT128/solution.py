#!/usr/bin/env python3

hex_list = [(hex(i)[2:].zfill(2).upper()) for i in range(256)]

with open('encfile', 'r', encoding='utf-8') as f:
    enc_data = f.read()

enc_list = [enc_data[i:i+2] for i in range(0, len(enc_data), 2)]

dec_list = list(range(len(enc_list)))

for i in range(len(enc_list)):
    hex_b = enc_list[i]
    index = hex_list.index(hex_b)
    dec_list[i] = hex_list[(index - 128) % len(hex_list)]

dec_bytes = bytes([int(hex_val, 16) for hex_val in dec_list])

with open('dec_flag.png', 'wb') as f:
    f.write(dec_bytes)

print("Decryption complete!")