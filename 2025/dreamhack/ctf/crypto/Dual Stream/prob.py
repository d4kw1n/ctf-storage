import os
from Crypto.Util.number import bytes_to_long

SIZE = 4
BSIZE = SIZE*8
FORM = f'{{0:0{BSIZE}b}}'

class LFSR:
    def __init__(self, iv: int, tap: list[int]):
        self.state = iv
        self.tap = tap

    def _xor(self, bits):
        res = 0
        for bit in bits:
            res ^= bit
        return res

    def get_bit(self):
        out = self.state & 1
        bit = self._xor([ ((self.state >> BSIZE-x) & 1) for x in self.tap ])
        self.state = (self.state >> 1) | (bit << BSIZE-1)
        return out

    def get_state(self):
        return self.state

class DualLFSR:
    def __init__(self, iv1: int, iv2: int, tap1: list[int], tap2: list[int]):
        self.lfsr1 = LFSR(iv1, tap1)
        self.lfsr2 = LFSR(iv2, tap2)

    def get_bit(self):
        bit1 = self.lfsr1.get_bit()
        bit2 = self.lfsr2.get_bit()
        return bit1 ^ bit2

    def get_state(self):
        return self.lfsr1.get_state(), self.lfsr2.get_state()

    def encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = b''
        for plaintext_char in plaintext:
            plaintext_char_bits = list(map(int, bin(plaintext_char)[2:].zfill(8)))
            stream_bits = [self.get_bit() for _ in range(8)]
            ciphertext_char_bits = [ x^y for x,y in zip(plaintext_char_bits, stream_bits)]
            ciphertext_char = int(''.join(map(str, ciphertext_char_bits)),2).to_bytes(1,'big')
            ciphertext += ciphertext_char
        return ciphertext


def main():
    iv1 = os.urandom(SIZE)
    iv2 = os.urandom(SIZE)
    assert iv1 != 0
    assert iv2 != 0
    iv1 = bytes_to_long(iv1)
    iv2 = bytes_to_long(iv2)
    tap1 = [32, 22, 2, 1]
    tap2 = [32, 31, 30, 10]
    stream = DualLFSR(iv1, iv2, tap1, tap2)

    with open('test', 'rb') as f:
        msg = f.read()
    print(msg)
    enc = stream.encrypt(msg)
    print(enc)

    cur_state1, cur_state2 = stream.get_state()
    new_iv1 = int(FORM.format(cur_state1)[::-1],2)
    new_iv2 = int(FORM.format(cur_state2)[::-1],2)
    new_stream = DualLFSR(new_iv1, new_iv2, tap2, tap1)

    with open('secret', 'rb') as f:
        msg = f.read()
    enc = new_stream.encrypt(msg)
    print(enc)

if __name__ == '__main__':
    main()
