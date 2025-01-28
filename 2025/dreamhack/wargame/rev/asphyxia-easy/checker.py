import subprocess

def check(inp_hex: str):
    """
    Check if input is valid.
    `inp_hex`: input, in hex string
    """
    if not all(c in '0123456789abcdef' for c in inp_hex):
        return False
    if not len(inp_hex) % 2 == 0:
        return False
    inp = bytes.fromhex(inp_hex)
    if len(inp) > 200:
        return False
    result = subprocess.check_output(['./asphyxia'], input=inp, timeout=1)
    return b"Correct\n" == result

if __name__ == "__main__":
    inp = input("Check: ")
    if check(inp):
        print("Correct!!!")
        with open("flag.txt") as f:
            print(f.read())
    else:
        print("Incorrect")